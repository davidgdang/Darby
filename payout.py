from bet import Bet
from errors import AmountTooLargeError, AmountTooSmallError, BetDoesNotExistError, HorseMissingError, MultipleBetError
from horse import Horse
from player import Player
from race import Race


class Payout:
    def __init__(self, race: Race):
        self.bets = []
        self.race = race

    # call Bet.makeBet and use the bet returned to add it to bets
    # if amount <= 0 raise BetTooSmallError
    # if amount > player.money raise BetTooLargeError
    # if player has already made a bet, raise MultipleBetError
    # TODO: account for when the horse does exist 
    def addBet(self, player: Player, horseName: str, amount: int):
        if (amount <= 0):
            raise AmountTooSmallError()
        if (amount > player.money):
            raise AmountTooLargeError()
        raceHorse: Horse
        flag = 0
        horse: Horse
        for raceHorse in self.race.horses:
            if raceHorse.name == horseName:
                flag = 1
                horse = raceHorse
        if flag == 0:
            raise HorseMissingError()
        bet: Bet
        for bet in self.bets:
            if bet.player.name == player.name:
                raise MultipleBetError()
        player.subtractMoney(amount)
        newBet = Bet(player, horse, amount)
        self.bets.append(newBet)

    # pay out every player that bet on the winner
    # according to the winners odds
    def payoutPlayers(self, winner: Horse) -> list:
        bet: Bet
        winners = []
        for bet in self.bets:
            bet.player.games = bet.player.games + 1
            if bet.horse.name == winner.name:
                payoutMultiplier = (1 - winner.winProbability) / winner.winProbability
                winnings = round(bet.money +  (bet.money * payoutMultiplier))
                winners.append([bet.player, winnings])
                bet.player.addMoney(round(bet.money + (bet.money * payoutMultiplier)))
                bet.player.wins = bet.player.wins + 1
                print(bet.player.money)
        return winners

    # remove given bet from bets
    # give bet money back to player
    # if bet does not exist, raise BetDoesNotExistError
    def removeBet(self, playerName: str):
        found = 0
        bet: Bet
        for bet in self.bets:
            if bet.player.name == playerName:
                bet.player.addMoney(bet.money)
                self.bets.remove(bet)
                found = 1
        if found == 0:
            raise BetDoesNotExistError()