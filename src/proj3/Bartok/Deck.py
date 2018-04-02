from Card import *
import random


class Deck(object):
  def __init__(self):
    self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
    print("DEBUG")
    print (self.cards)
    self.cards = self.cards[0:53]
    self.shuffle()
# was 10
  def shuffle(self, seed=10):
    self.seed = seed
    random.shuffle(self.cards, random.seed(self.seed))

  def draw(self, amount=1):
    return [self.cards.pop() for _ in range(amount)]

  def cardsLeft(self):
    return len(self.cards) != 0

  def refill(self, discarded):
    self.cards = self.cards + discarded
    self.shuffle()

  def __str__(self):
    out = ''
    out += 'The current seed is %d\n' % (self.seed)
    out += 'The cards in the the deck are:\n'
    for c in self.cards:
      out += '\t%s\n' % (c)
    return out
