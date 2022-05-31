from horse import Horse
from leaderboard import Leaderboard
from payout import Payout
from race import Race
from decimal import Decimal
from tabulate import tabulate
import discord

def generateOpenBetsMessage(race: Race) -> str:
    message = ''
    for horse in race.horses:
        odds = (1 - horse.winProbability) / horse.winProbability
        odds = round(odds, 2)
        odds = str(odds)
        winPercentage = str(round(horse.winProbability * 100))
        message = message + '\n' + horse.name + ': ' + winPercentage + '% chance to win, ' + odds + ':1 payout'
    return message

def generateLeaderboardMessage(leaderboard: Leaderboard) -> str:
    array = []
    for i in range(len(leaderboard.players)):
        if leaderboard.players[i].games == 0:
            winPercentage = '0%'
        else:
            winPercentage = str(round((leaderboard.players[i].wins / leaderboard.players[i].games) * 100)) + '%'
        array.append([i + 1, leaderboard.players[i].name, leaderboard.players[i].money, winPercentage])
    message = '```' + tabulate(array, headers=['rank', 'name', 'money', 'win rate']) + '```'
    return message

def generateStartRaceMesage(winner: Horse, winners: list, guild: discord.Guild) -> str:
    message = 'The race is over! The fastest horse today was ' + winner.name + '. congratulations to the winners today:'
    for tuple in winners:
        message = message + '\n' + guild.get_member(tuple[0].id).mention + ': $' + str(tuple[1])
    return message

def generateShowBetsMessage(payout: Payout) -> str:
    array = []
    for bet in payout.bets:
        array.append([bet.player.name, bet.horse.name, bet.money])
    message = '```' + tabulate(array, headers=['player', 'horse', 'amount']) + '```'
    return message
