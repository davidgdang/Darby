from horse import Horse
from player import Player


class Bet:

    # Assume amount <= self.money
    # And amount > 0   
    # call player.subtractMoney
    # then set fields to the given parameters
    def __init__(self, player: Player, horse: Horse, amount: int):
        self.player = player
        self.horse = horse
        self.money = amount

