import random
from horse import Horse

class Race:
    NUM_HORSES = 3

    # TODO: initialize the horses and add them to the list
    def __init__(self):
        self.horses = []
        variance = 20
        avgProbability = 1 / self.NUM_HORSES
        minProbability = avgProbability - (variance * 0.01)
        maxProbability = avgProbability + (variance * 0.01)
        totalProbability = 1
        for i in range(self.NUM_HORSES):
            name = self.chooseName()
            if (i == self.NUM_HORSES - 1):
                horse = Horse(name, totalProbability)
                self.horses.append(horse)
            else:
                rng = random.randrange(variance * -1, variance) * 0.01
                winProbability = avgProbability + rng
                flag = 0
                while (flag == 0):
                    if (totalProbability - winProbability >= minProbability * (self.NUM_HORSES - (i + 1))):
                        horse = Horse(name, winProbability)
                        self.horses.append(horse)
                        totalProbability = totalProbability - winProbability
                        flag = 1
                    else:
                        winProbability = winProbability - 0.01
    # choose a winner based on probabilities and return winner
    def startRace(self) -> Horse:
        weights = []
        for horse in self.horses:
            weights.append(horse.winProbability)
        return random.choices(self.horses, weights)[0]
    
    def chooseName(self) -> str:
        f = open('horse names.txt')
        names = f.read()
        names = names.split()
        return random.choice(names)