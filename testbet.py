import unittest
from player import Player
from horse import Horse 
from bet import Bet

class TestBet(unittest.TestCase):

    def setUp(self) -> None:
        player = Player('jett')
        horse = Horse('horseman', 0.5)
        self.bet = Bet(player, horse, Player.INIT_MONEY)

    def testConstructor(self):
        self.assertEqual(self.bet.player.name, 'jett')
        self.assertEqual(self.bet.horse.name, 'horseman')
        self.assertEqual(self.bet.money, Player.INIT_MONEY)
        self.assertEqual(self.bet.player.money, 0)
    
if __name__ == '__main__':
    unittest.main()