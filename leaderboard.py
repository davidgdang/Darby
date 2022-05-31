import string
from player import Player
import errors

class Leaderboard:
    def __init__(self, players: list[Player]):
        self.players = players
        self.sortLeaderboard()
    

    # sort leaderboard by money
    def sortLeaderboard(self):
        self.players.sort(key=lambda x: x.money, reverse=True)

    def addPlayer(self, pushinp: Player):
        # O(n)
        for x in self.players:
            if x.name == pushinp.name:
                raise errors.RedundantPlayerError()        
        #self.players.append(pushinp)
        for i in range (len(self.players)):
            # checking player money, from greatest to least
            if pushinp.money >= self.players[i].money:
                self.players.insert(i,pushinp)
                return
        self.players.append(pushinp)
    
    def removePlayer(self, name: string):
        for player in self.players:
            if (name == player.name):
                self.players.remove(player)
                return
        raise errors.PlayerDoesNotExistError()

    def findPlayer(self, name: string):
        for player in self.players:
            if(name == player.name):
                return player        
        
    
    #deez
    # def printLeaderBoard(self):