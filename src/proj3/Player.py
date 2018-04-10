from Hand import Hand


class Player(object):
  """
  object for containing data relating a to player and state machine for order of play
  """

  def __init__(self, idNum, game, AI=False):
    self.idNum = idNum
    self.game = game
    self.hand = Hand()
    self.score = 0
    self.AI = AI
    self.finished = False
    self.AIFunction = None
    self.humanFunction = None
    self.skipped = False

  def setPrev(self, prev):
    """
    this is used to set the previous player
    when player cannot play
    previous player gets to play
    """
    self.prev = prev

  def setNext(self, next):
    """
    this used to set the next player
    when player successfully plays
    the next player plays
    """
    self.next = next

  def play(self, prevPlay):
    validPlays = self.game.validPlays(self, prevPlay)
    # if nothing can be played return the empty list. this is lisp like because empty list is false
    if not self.AI:
      played = self.humanFunction(self, validPlays, prevPlay)
    else:
      played = self.AIFunction(self, validPlays, prevPlay)

    return played

  def drawCard(self):
    try:
      if not self.game.deck.cardsLeft():
        self.game.refillDeck()
      self.game.deck.draw(self.hand)
    except:
      print("No more cards left in deck and no cards to refill deck with")

  def noCardsLeft(self):
    return len(self.hand.cards) == 0

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    out = 'Player: ' + str(self.idNum)
    out += '\nHand: ' + str(self.hand.cards)
    out += '\nAI: ' + str(self.AI)
    out += '\nNext Player: ' + str(self.next.idNum)
    out += '\nPrev Player: ' + str(self.prev.idNum)
    return out
