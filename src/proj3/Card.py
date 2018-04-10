# List of Suits, Club, Spade, Diamond, Heart
suits = "Clubs Spades Diamonds Hearts".split(" ")

# List of ranks.  String representation.  Will be 2-10 plus J Q K A
ranks = 'A'.split(" ") + [str(i) for i in range(2, 11)] + "J Q K".split(" ")


class Card(object):
  #  Assigns value to each rank.  EX giving 2 a value of 2, and K a value of 13.
  scores = {rank: value for rank, value in zip(ranks, range(1, 14))}

  def __init__(self, rank, suit):
    self.rank = str(rank)
    self.suit = str(suit)
    self.score = Card.scores[rank]
    self.symbol_dict = {'Hearts': '\u2665', 'Diamonds': '\u2666', 'Spades': '\u2660', 'Clubs': '\u2663'}

  def __repr__(self):
    ascii_card = '\n'.join(self.make_card())
    return ascii_card

  def __lt__(self, other):
    return self.score < other.score

  def __eq__(self, other):
    return self.rank == other.rank and self.suit == other.suit

  def make_card(self):
    two_digit = False

    # Formatting Boolean
    if self.rank == "10":
      two_digit = True

    # # If a face card, we want just the capital letter.
    # if value > 10 or value == 1:
    #   value = self.value[0]
    suit = self.suit
    ascii_card = []
    space = " "
    suit_symbol = self.symbol_dict[suit]
    if two_digit:
      space = ""

    # Helps see formatting.  Prints space between quotes.
    # print('Space is: ' + "\"" + space + "\"")

    ascii_card.append('┌───────────────┐')
    ascii_card.append('│{}{}           │'.format(space, self.rank))
    ascii_card.append('│             │')
    ascii_card.append('│             │')
    ascii_card.append('│     {}       │'.format(suit_symbol))
    ascii_card.append('│             │')
    ascii_card.append('│             │')
    ascii_card.append('│           {}{}│'.format(space, self.rank))
    ascii_card.append('└───────────────┘')
    return ascii_card
