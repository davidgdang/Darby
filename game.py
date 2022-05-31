from leaderboard import Leaderboard
from payout import Payout
from race import Race

class Game:

    def __init__(self, race: Race, leaderboard: Leaderboard, payout: Payout):
        self.race = race
        self.leaderboard = leaderboard
        self.payout = payout

    # Start race, then payout players, then update leaderboard
    def startGame(self):
        pass