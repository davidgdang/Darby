
import unittest
from payout import Payout
from player import Player
from horse import Horse
import errors
from race import Race

class TestPlayer(unittest.TestCase):
    
    def setUp(self) -> None:
        race = Race()
        race.horses[0].winProbability = 0.5
        race.horses[1].winProbability = 0.5
        for i in range(2, Race.NUM_HORSES):
            race.horses[i].winProbability = 0
        self.payout = Payout(race)

    def testConstructor(self):
        self.assertTrue(len(self.payout.bets) == 0)

    def testAddBetOneBet(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, Player.INIT_MONEY / 2)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY / 2)
    
    def testAddBetMinBet(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, 1)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, 1)
    
    def testAddBetMaxBet(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, Player.INIT_MONEY)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY)

    def testAddBetTwoBets(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, Player.INIT_MONEY / 2)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY / 2)

        player2 = Player('reyna')
        horse2 = self.payout.race.horses[1]
        self.payout.addBet(player2, horse2.name, Player.INIT_MONEY)
        self.assertTrue(len(self.payout.bets) == 2)
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY / 2)
        bet2 = self.payout.bets[1]
        self.assertEqual(bet2.player.name, 'reyna')
        self.assertEqual(bet2.horse.name, self.payout.race.horses[1].name)
        self.assertEqual(bet2.money, Player.INIT_MONEY)

    def testAddBetZero(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        with self.assertRaises(errors.AmountTooSmallError):
            self.payout.addBet(player, horse.name, 0)
        self.assertTrue(len(self.payout.bets) == 0)

    def testAddBetNegativeBet(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        with self.assertRaises(errors.AmountTooSmallError):
            self.payout.addBet(player, horse.name, -1)
        self.assertTrue(len(self.payout.bets) == 0)
    
    def testAddBetTooBig(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        with self.assertRaises(errors.AmountTooLargeError):
            self.payout.addBet(player, horse.name, Player.INIT_MONEY + 1)
        self.assertTrue(len(self.payout.bets) == 0)
    
    def testAddBetWayTooBig(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        with self.assertRaises(errors.AmountTooLargeError):
            self.payout.addBet(player, horse.name, Player.INIT_MONEY + 5000)
        self.assertTrue(len(self.payout.bets) == 0)
    
    def testAddBetSamePlayerTwoBets(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, Player.INIT_MONEY / 2)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY / 2)

        with self.assertRaises(errors.MultipleBetError):
            self.payout.addBet(player, horse.name, Player.INIT_MONEY / 2)
        self.assertTrue(len(self.payout.bets) == 1)

    def testPayoutPlayersOneBetOneWinner(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        betAmount = Player.INIT_MONEY / 2
        self.payout.addBet(player, horse.name, betAmount)
        balanceAfterBet = player.money
        self.payout.payoutPlayers(horse)
        self.assertEqual(player.money, balanceAfterBet + (betAmount * 2))

    def testPayoutPlayersThreeToOneOdds(self):
        player = Player('jett')
        self.payout.race.horses[0].winProbability = 0.25
        horse = self.payout.race.horses[0]
        betAmount = Player.INIT_MONEY / 2
        self.payout.addBet(player, horse.name, betAmount)
        balanceAfterBet = player.money
        self.payout.payoutPlayers(horse)
        self.assertEqual(player.money, balanceAfterBet + (betAmount * 4))

    def testPayoutPlayersOneBetNoWinners(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        betAmount = Player.INIT_MONEY / 2
        self.payout.addBet(player, horse.name, betAmount)
        balanceAfterBet = player.money
        horse2 = self.payout.race.horses[1]
        self.payout.payoutPlayers(horse2)
        self.assertEqual(player.money, balanceAfterBet)
    
    def testPayoutPlayersTwoBetsOneWinner(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        betAmount = Player.INIT_MONEY / 2
        player2 = Player('reyna')
        horse2 = self.payout.race.horses[1]
        self.payout.addBet(player, horse.name, betAmount)
        self.payout.addBet(player2, horse2.name, betAmount)
        balanceAfterBet = player.money
        self.payout.payoutPlayers(horse)
        self.assertEqual(player.money, balanceAfterBet + (betAmount * 2))
        self.assertEqual(player2.money, balanceAfterBet)

    def testPayoutPlayersTwoBetsTwoWinners(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        betAmount = Player.INIT_MONEY / 2
        player2 = Player('reyna')
        self.payout.addBet(player, horse.name, betAmount)
        self.payout.addBet(player2, horse.name, betAmount)
        balanceAfterBet = player.money
        self.payout.payoutPlayers(horse)
        self.assertEqual(player.money, balanceAfterBet + (betAmount * 2))
        self.assertEqual(player2.money, balanceAfterBet + (betAmount * 2))
    
    def testRemoveBetSuccess(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, Player.INIT_MONEY / 2)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY / 2)
        self.payout.removeBet('jett')
        self.assertEqual(len(self.payout.bets), 0)
    
    def testRemoveBetNotfound(self):
        player = Player('jett')
        horse = self.payout.race.horses[0]
        self.payout.addBet(player, horse.name, Player.INIT_MONEY / 2)
        self.assertTrue(len(self.payout.bets) == 1)
        bet = self.payout.bets[0]
        self.assertEqual(bet.player.name, 'jett')
        self.assertEqual(bet.horse.name, self.payout.race.horses[0].name)
        self.assertEqual(bet.money, Player.INIT_MONEY / 2)
        with self.assertRaises(errors.BetDoesNotExistError):
            self.payout.removeBet('reyna')
        self.assertEqual(len(self.payout.bets), 1)
    
    def testaddBetHorseMissing(self):
        player = Player('jett')
        horse = Horse('imaginary', 1)
        with self.assertRaises(errors.HorseMissingError):
            self.payout.addBet(player, horse.name, Player.INIT_MONEY)
        self.assertEqual(len(self.payout.bets), 0)



if __name__ == '__main__':
    unittest.main()