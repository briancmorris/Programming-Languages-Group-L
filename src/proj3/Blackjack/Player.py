from Card import Card


class Player(object):
  """
  object for containing data relating a to player and state machine for order of play
  """

  def __init__(self, idNum, game, AI=False):
    self.idNum = idNum
    self.game = game
    self.hand = []
    self.score = 0
    self.AI = AI
    self.finished = False
    self.AIFunction = None
    self.humanFunction = None

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

  def play(self):
    validPlays = self.game.validPlays(self)
    # if nothing can be played return the empty list. this is lisp like because empty list is false
    if not validPlays:
      return validPlays
    if not self.AI:
      played = self.humanFunction(self, validPlays)
    else:
      played = self.AIFunction(self, validPlays)

    return played

  def drawCard(self):
    try:
      if not self.game.deck.cardsLeft():
        self.game.refillDeck()
      self.hand += self.game.deck.draw()
    except:
      print("No more cards left in deck and no cards to refill deck with")

  def noCardsLeft(self):
    return len(self.hand) == 0

  def calculateScore(self):
    def containsAce(hand):
      """ Helper method, determines if an Ace is present """
      for card in hand:
        if card.rank == 'A':
          return True
      return False

    self.score = 0

    for card in self.hand:
      if card.score > 10:
        self.score += 10
      else:
        self.score += card.score

    if containsAce(self.hand):
      if self.score + 10 <= 21:
        self.score += 10

    return self.score

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    out = 'Player: ' + str(self.idNum)
    out += '\nHand: ' + str(self.hand)
    out += '\nAI: ' + str(self.AI)
    out += '\nNext Player: ' + str(self.next.idNum)
    out += '\nPrev Player: ' + str(self.prev.idNum)
    return out
