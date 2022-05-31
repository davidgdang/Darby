import unittest
from horse import Horse
from race import Race

class TestRace(unittest.TestCase):

    def setUp(self) -> None:
        self.race = Race()

    def testConstructor(self):
        self.assertEqual(len(self.race.horses), Race.NUM_HORSES)
        sumProbability = 0
        horse: Horse
        for horse in self.race.horses:
            sumProbability = sumProbability + horse.winProbability
        self.assertAlmostEqual(sumProbability, 1)
    
    def testStartRace(self):
        winner = self.race.startRace()
        self.assertIsInstance(winner, Horse)
    
    def testRiggedRace(self):
        self.race.horses[0].winProbability = 1
        for i in range(1, len(self.race.horses) - 1):
            self.race.horses[i].winProbability = 0
        winner = self.race.startRace()
        self.assertEqual(winner.name, self.race.horses[0].name)


if __name__ == '__main__':
    unittest.main()