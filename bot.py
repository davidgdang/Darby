
import os
from bet import Bet
from errors import AmountTooLargeError, AmountTooSmallError, BetDoesNotExistError, HorseMissingError, MultipleBetError, PlayerDoesNotExistError
import helpers
#deez
import discord
from dotenv import load_dotenv
from discord.ext import commands
from leaderboard import Leaderboard
from payout import Payout
from player import Player
from race import Race
import pickle

load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
discBot = commands.Bot(command_prefix='$', intents = intents)
leaderboard = None
payout = None
race = None
guild = None
adminRole = 975578359675371570
playerRole = 975579359660347472

@discBot.event
async def on_ready():
    global leaderboard
    global guild
    global payout
    global race
    guild = discord.utils.get(discBot.guilds, id=612511489869217805)
    print(f'{discBot.user} has connected to Discord!')
    try:
        leaderboard = pickle.load(open("leaderboard.pickle", "rb"))
    except (OSError, IOError) as e:
        members = guild.members
        players = []
        for member in members:
            roles = member.roles
            flag = 0
            for role in roles:
                if (role.id == 975579359660347472):
                    flag = 1
            if flag == 1:
                player = Player(member.name, member.id)
                players.append(player)
            else:
                pass
        leaderboard = Leaderboard(players)
        pickle.dump(leaderboard, open("leaderboard.pickle", "wb"))
    try:
        race = pickle.load(open('race.pickle', 'rb'))
        payoutPickle = pickle.load(open('payout.pickle', 'rb'))
        if not(payoutPickle is None):
            payout = Payout(race)
            for bet in payoutPickle.bets:
                for player in leaderboard.players:
                    if bet.player.id == player.id:
                        payout.bets.append(Bet(player, bet.horse, bet.money))
        else:
            payout = None

    except:
        print('sss')
    for leaderboardPlayer in leaderboard.players:
        print(leaderboardPlayer.name)

#@discBot.event
#async def on_member_join(member):
 #   player = Player(member.name, member.id)
  #  leaderboard.addPlayer(player)

@discBot.command(name='openbets', help='opens up a new race to bet on (admin only)', hidden = True)
async def openBets(ctx):
    global payout
    global race
    global adminRole
    global playerRole
    if (not(payout is None) or not(race is None)):
        message = 'There is already a game in place, if you would like to start a new game, please finish the existing one first'
    else:
        roles = ctx.author.roles
        flag = 0
        message = ''
        for role in roles:
            if (role.id == adminRole):
                flag = 1
        if flag == 1:
            race = Race()
            payout = Payout(race)
            pickle.dump(race, open('race.pickle', 'wb'))
            pickle.dump(payout, open('payout.pickle', 'wb'))
            message = guild.get_role(playerRole).mention + ' Bets are now open, you may bet on the following horses:' + helpers.generateOpenBetsMessage(race)
        else:
            message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'rank', help = 'see your rank on the leaderboard')
async def rank(ctx):
    global leaderboard
    message = ''
    for i in range (len(leaderboard.players)):
        if ctx.author.id == leaderboard.players[i].id:
            message = 'You are currently rank ' + str(i + 1) + ' with a balance of ' + str(leaderboard.players[i].money)
    await ctx.send(message)

@discBot.command(name = 'leaderboard', help = 'show leaderboard')
async def leaderboard(ctx):
    global leaderboard
    message = helpers.generateLeaderboardMessage(leaderboard)
    await ctx.send(message)

@discBot.command(name = 'bet', help = 'bet an amount on a horse, should be formatted like Ex. bet horsey 100')
async def bet(ctx):
    global payout
    global leaderboard
    if (payout is None):
        message = 'There is currently no race available to bet on, please open bets first'
    else:
        args = ctx.message.content.split()
        if len(args) != 3:
            await ctx.send('Error: invalid number of arguments')
            return
        horse: str = args[1]
        amount = args[2]
        playerID = ctx.author.id
        for player in leaderboard.players:
            if playerID == player.id:
                try:
                    payout.addBet(player, horse.capitalize(), int(amount))
                    leaderboard.sortLeaderboard()
                    pickle.dump(payout, open('payout.pickle', 'wb'))
                    pickle.dump(leaderboard, open('leaderboard.pickle', 'wb'))
                    message = 'Your bet was successfully added'
                except AmountTooSmallError:
                    message = 'Error: your bet is zero or negative'
                except AmountTooLargeError:
                    message = 'Error: your bet is too large'
                except HorseMissingError:
                    message = 'Error: this horse does not exist'
                except MultipleBetError:
                    message = 'Error: you have already placed a bet. If you would like to remove your bet, use $removebet'
                break
    await ctx.send(message)

@discBot.command(name = 'startrace', help = 'start the race (admin only)', hidden = True)
async def startRace(ctx):
    global payout
    global race
    global leaderboard
    global adminRole
    if (payout is None):
        message = 'There is currently no race, please open bets first'
    else:
        roles = ctx.author.roles
        flag = 0
        message = ''
        for role in roles:
            if (role.id == adminRole):
                flag = 1
        if flag == 1:
            winner = race.startRace()
            winners = payout.payoutPlayers(winner)
            leaderboard.sortLeaderboard()
            pickle.dump(leaderboard, open("leaderboard.pickle", "wb"))
            message = helpers.generateStartRaceMesage(winner, winners, guild)
            payout = None
            race = None
            pickle.dump(payout, open('payout.pickle', 'wb'))
            pickle.dump(race, open('race.pickle', 'wb'))
        else:
            message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'allowance', help = 'give all players their allowance (admin only)', hidden = True)
async def allowance(ctx):
    global leaderboard
    global adminRole
    allowance = 100
    roles = ctx.author.roles
    flag = 0
    message = ''
    for role in roles:
        if (role.id == adminRole):
            flag = 1
    if flag == 1:
        for player in leaderboard.players:
            player.addMoney(allowance + round(0.05 * player.money))
        message = 'Allowance of ' + str(allowance) + ' + 5 percent interest has been given to all players'
    else:
        message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'addplayer', help = 'add a player to the leaderboard (admin only)', hidden = True)
async def addPlayer(ctx):
    global leaderboard
    global adminRole
    roles = ctx.author.roles
    flag = 0
    message = ''
    for role in roles:
        if (role.id == adminRole):
            flag = 1
    if flag == 1:
        args = ctx.message.content.split()
        if len(args) != 2:
            await ctx.send('Error: invalid number of arguments')
            return
        name = args[1]
        for member in guild.members:
            if (name == member.name):
                player = Player(member.name, member.id)
                leaderboard.addPlayer(player)
                pickle.dump(leaderboard, open('leaderboard.pickle', 'wb'))
                message = name + ' has been added to the leaderboard'
                break
    else:
        message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'removebet', help = 'remove your bet from the pool')
async def removeBet(ctx):
    global payout
    global leaderboard
    try:
        payout.removeBet(ctx.author.name)
        pickle.dump(leaderboard, open('leaderboard.pickle', 'wb'))
        pickle.dump(payout, open('payout.pickle', 'wb'))
        message = 'Your bet has been successfully removed'
    except BetDoesNotExistError:
        message = 'Error: You have not placed a bet yet, cannot remove'
    await ctx.send(message)

@discBot.command(name = 'horses', help = 'show all horses currently in the race')
async def horses(ctx):
    global race
    if (race is None):
        message = 'There is currently no race right now'
    else:
        message = helpers.generateOpenBetsMessage(race)
    await ctx.send(message)

@discBot.command(name = 'removeplayer', help = 'add a player to the leaderboard (admin only)', hidden = True)
async def removePlayer(ctx):
    global leaderboard
    global adminRole
    roles = ctx.author.roles
    flag = 0
    message = ''
    for role in roles:
        if (role.id == adminRole):
            flag = 1
    if flag == 1:
        args = ctx.message.content.split()
        if len(args) != 2:
            await ctx.send('Error: invalid number of arguments')
            return
        name = args[1]
        try:
            leaderboard.removePlayer(name)
            message = 'Player has been successfully removed'
            pickle.dump(leaderboard, open('leaderboard.pickle', 'wb'))
        except:
            message = 'Error: player does not exist'
    else:
        message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'setmoney', help = 'set a players money (admin only)', hidden = True)
async def setMoney(ctx):
    global leaderboard
    global adminRole
    roles = ctx.author.roles
    flag = 0
    message = ''
    for role in roles:
        if (role.id == adminRole):
            flag = 1
    if flag == 1:
        args = ctx.message.content.split()
        if len(args) != 3:
            await ctx.send('Error: invalid number of arguments')
            return
        name = args[1]
        amount = int(args[2])
        try:
            player = leaderboard.findPlayer(name)
            player.setMoney(amount)
            leaderboard.sortLeaderboard()
            message = name + " money set to " + str(amount)
            pickle.dump(leaderboard, open('leaderboard.pickle', 'wb'))
        except PlayerDoesNotExistError:
            message = 'Error: player does not exist'
    else:
        message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'savebackup', help = 'save a backup of the leaderboard (admin only)', hidden = True)
async def saveBackup(ctx):
    global leaderboard
    global adminRole
    roles = ctx.author.roles
    flag = 0
    message = ''
    for role in roles:
        if (role.id == adminRole):
            flag = 1
    if flag == 1:
        pickle.dump(leaderboard, open('backup.pickle', 'wb'))
        message = 'Backup has been saved'
    else:
        message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'loadbackup', help = 'load existing backup (admin only)', hidden = True)
async def loadBackup(ctx):
    global leaderboard
    global adminRole
    roles = ctx.author.roles
    flag = 0
    message = ''
    for role in roles:
        if (role.id == adminRole):
            flag = 1
    if flag == 1:
        try:
            leaderboard = pickle.load(open('backup.pickle', 'rb'))
            pickle.dump(leaderboard, open('leaderboard.pickle', 'wb'))
            message = 'Backup has been loaded'
        except (OSError, IOError) as e:
            message = 'No backup saved currently'    
    else:
        message = 'You are not permitted to use this command'
    await ctx.send(message)

@discBot.command(name = 'showbets', help = 'show list of existing bets')
async def showBets(ctx):
    global payout
    message = helpers.generateShowBetsMessage(payout)
    await ctx.send(message)
                    
discBot.run(TOKEN)

