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
    validPlays = self.game.validPlays(self.hand, prevPlay)
    # if nothing can be played return the empty list. this is lisp like because empty list is false
    if not self.AI:
      played = self.humanPlay(validPlays)
      if played is None:
        played = prevPlay


    else:
        # AI logic goes here!
        if len(validPlays) > 0:
          played = validPlays[0]
          print("played %s" % played.__repr__())
        else:
          self.drawCard()
          return prevPlay

    if type(played) is Card:
      self.hand = [card for card in self.hand if not card == played]

      if played.rank == "K":
        self.next.finished = True
        self.next.drawCard()
        self.next.drawCard()
      elif played.rank == "Q":
        self.next.finished = True
      elif played.rank == "J":
        self.next.drawCard()

    return played

    # if type(played) is list or type(played) is tuple:
    #   self.hand = [card for card in self.hand if card not in played]
    # elif type(played) is Card:
    #   print("removing cards")
    #   self.hand = [card for card in self.hand if not card == played]
    # return played

  def humanPlay(self, allowed):
    print("Your current hand is {}".format(self.hand))
    #print("Your current hand score is {}".format(self.score))
    if len(allowed) == 0:
      print("You had to draw.")
      self.drawCard()
      return None
    print("You can do the following:")

    #for action, i in zip(allowed, range(0,len(allowed))):
      #print("{} {}".format(i, action))
    for index, card in enumerate(allowed):
      print("{} {}".format(index, card.__repr__()))
    selected = 0
    tbp = None
    while tbp is None:
      try:
        selected = int(input("Enter the index of the move you make: "))
        tbp = allowed[selected] if selected >= 0 else []
      except (ValueError, IndexError):
        print("Invalid selection")
        tbp = None
    return tbp

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
