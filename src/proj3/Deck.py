from Card import *
import random


class Deck(object):
  def __init__(self):
    self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
    self.shuffle()

  def shuffle(self, seed=10):
    self.seed = seed
    random.shuffle(self.cards, random.seed(self.seed))

  def __iter__(self):
    return iter(self.cards)

  def __getitem__(self, index):
    """ Allows the fetching of cards by index """
    return self.cards[index]

  def draw(self, hand, amount=1):
    for i in range(amount):
      hand.cards.append(self.cards.pop())

  def cardsLeft(self):
    return len(self.cards) > 0

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
