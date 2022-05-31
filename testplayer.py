import unittest

from player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.player = Player('jett')

    def testConstructor(self):
        self.assertEqual(self.player.name, 'jett')
        self.assertEqual(self.player.money, Player.INIT_MONEY)
    
    def testSubtractMoneyRegularInput(self):
        self.player.subtractMoney(Player.INIT_MONEY / 2)
        self.assertEqual(self.player.money, Player.INIT_MONEY - (Player.INIT_MONEY / 2))

    def testSubtractMoneyMaxInput(self):
        self.player.subtractMoney(Player.INIT_MONEY)
        self.assertEqual(self.player.money, 0) 
    
    def testSubtractMoneyMinInput(self):
        self.player.subtractMoney(1)
        self.assertEqual(self.player.money, Player.INIT_MONEY - 1)

    def testSubtractMoneyTwice(self):
        self.player.subtractMoney(Player.INIT_MONEY / 4)
        self.player.subtractMoney(Player.INIT_MONEY / 2)
        self.assertEqual(self.player.money, Player.INIT_MONEY - (Player.INIT_MONEY / 4) - (Player.INIT_MONEY / 2))

if __name__ == '__main__':
    unittest.main()