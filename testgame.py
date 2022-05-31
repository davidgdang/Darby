from game import Game
from leaderboard import Leaderboard
from payout import Payout
from race import Race
import unittest

class TestGame(unittest.Testcase):

    def setUp(self) -> None:
        self.TestGame = Game()
        TestGame.leaderboard = Leaderboard()
        TestGame.payout = Payout()

    def TestCreateGame():
        #check if game class is created
        pass

    def TestCreateLeaderboard():
        #check if leaderboard class is created
        pass
    
    def TestCreatePayout():
        #check if payout class is created
        pass


if __name__ == '__main__':
    unittest.main()
