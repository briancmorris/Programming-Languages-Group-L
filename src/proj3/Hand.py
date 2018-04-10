class Hand:
  """ Hand of cards.  Belongs to a player.  In Blackjack, this will start off as only two cards. """

  def __init__(self):
    self.cards = []

  def __repr__(self):
    """
    Determines how to print the Hand as a string.
    :return: The hand as a string in the format <value> of <suit>
    """
    hand_string = ""
    hand_array = []
    total_hand = ["" for _ in range(9)]

    # For every card in my hand, add it's ascii version to an array.
    for card in self.cards:
      ascii_card = card.make_card()
      hand_array.append(ascii_card)

    # Add all cards row by row to the total hand.
    for i in range(9):
      for card_pic in hand_array:
        total_hand[i] += card_pic[i] + "\t"

    hand_string += '\n'.join(total_hand)

    # Return picture version of hand
    return hand_string
