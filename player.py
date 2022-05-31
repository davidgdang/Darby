
from horse import Horse

class Player:
    INIT_MONEY = 100

    def __init__(self, name: str, id = 0):
        self.name = name
        self.id = id 
        self.money = Player.INIT_MONEY
        self.wins = 0
        self.games = 0
    
    # Assume amount <= self.money
    # And amount > 0
    # Subtracts amount from money
    def subtractMoney(self, amount: int):
        self.money = self.money - amount

    # if amount < 0, raise AmountTooSmallError
    # otherwise, add amount to player's money
    def addMoney(self, amount: int):
        self.money = self.money + amount
    
    def setMoney(self, amount: int):
        self.money = amount

#hi