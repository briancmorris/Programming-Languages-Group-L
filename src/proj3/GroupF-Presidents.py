rom Card import *
import random
from player import Player




if __name__ == "__main__":
  num_players = 4
  deck = [Card(rank, suit) for suit in suits for rank in ranks]
  random.shuffle(deck)
  stack = []
  hands = [[] for _ in range(num_players)]

  ## there is probably a function that does this, but I don't know of it off hand
  ## as equally as possible, distribute cards between players
  going = True
  while going:
    for i in range(num_players):
      if deck:
        hands[i].append(deck.pop())
      else:
        going = False
        break
  players = []
  for hand in hands:
    print(len(hand), hand)
    players.append(Player(len(players) , hand))
  for i in range(len(players)):
    players[i].setPrev(players[i - 1])
    players[i].setNext(players[(i + 1) % num_players])
  
  
  pl = players[0]
  prevPl = []
  winners = []
  while len(players) > 1:
    prevPl, nextpl = pl.play(prevPl)
    if not pl.hand:
      #if player has an empty hand remove from game
      next = pl.next
      prev = pl.prev
      prev.setNext(next)
      next.setPrev(prev)
      players = [player for player in players if not player == pl]
      winners.append(pl)
      print("player {} has finished".format(pl.idNum))
    pl = nextpl
  
  winners.append(players.pop())
  
  for c, v in enumerate(winners):
print("winner number {} is player {
