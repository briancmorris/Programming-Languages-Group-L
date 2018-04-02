# List of Suits, Club, Spade, Diamond, Heart
suits = "C S D H".split(" ")

# List of ranks.  String representation.  Will be 2-10 plus J Q K A
ranks = 'A'.split(" ") + [str(i) for i in range(2, 11)] + "J Q K".split(" ")


class Card(object):
  #  Assigns value to each rank.  EX giving 2 a value of 2, and K a value of 13.
  scores = {rank: value for rank, value in zip(ranks, range(1, 14))}

  def __init__(self, rank, suit):
    self.rank = str(rank)
    self.suit = str(suit)
    self.score = Card.scores[rank]

  def __repr__(self):
    return "{} of {}".format(self.rank, self.suit)

  def __str__(self):
    self.__repr__()

  def __lt__(self, other):
    return self.score < other.score

  def __eq__(self, other):
    return self.rank == other.rank and self.suit == other.suit
