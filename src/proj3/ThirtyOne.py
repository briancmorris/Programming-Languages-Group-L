from Game import Game

lives = []
discardPile = []

class ThirtyOne(Game):

  def restoreLives(self):
    """Restores the lives of all players in the game."""
    self.lives = []
    for player in self.players:
      self.lives.append(3)

  def endCondition(self):
    """Defines the end condition of the game, 1 player has 1 or more lives."""
    potentialWinners = [];
    for player in self.players:
      if lives[player.idNum] == 0:
        self.losers.append[player]
      else:
        potentialWinners.append(player)

    if len(potentialWinners) == 1:
      self.winner = potentialWinners[0]
      return True
    else:
      return False

  def winMessage(self):
    """Prints the win message of the game."""
    print("The winner of 31 is:")
    print(f"Player {self.winner.idNum}!")

  def cantPlay(self, player):
    return lives[player.idNum] == 0

  def validPlays(self, player):
    """Return a list of valid players for a player. Empty if player can't play."""
    if self.cantPlay(player):
      return []
    else:
      return [self.drawFromStock, self.drawFromDiscard, self.knock]

  def drawFromStock(self, player):
    """Player draws from stock, must discard any card from their hand afterward."""
    # How do we deal, with a deck that gets refilled from discard pile?
    player.drawCard()
    print("Player " + player.idNum + " drew from the deck.")

  def drawFromDiscard(self, player):
    """Player draws from discard pile, must discard a different card afterward."""
    card = discardPile.pop()
    player.hand.cards.append(card)
    print("Player " + player.idNum + " drew\n" + card)

  def knock(self, player):
    """Player knocks, each player has one round left to change their hand."""
    print("Player " + player.idNum + " knocks! Everyone has 1 chance left!")
    player.finished = True

  def dealHands(self):
    """Deals 3 cards to each player, initiates discard pile to a single card."""
    self.deck.shuffle()
    for player in self.players:
      self.deck.draw(player.hand, 3)
    self.deck.draw(discardPile, 1)

  def playerPlayed(self, player, played):
    """Appends discarded card from player to discard pile, returns the next player."""
    print("Player " + player.idNum + " discarded\n" + played)
    self.discardPile.append(played)
    return player.next

  def calculateScore(self, player):
    """Calculates the score of a player's hand. The sum of 1 suit or highest card.
        If there's a 3 of a kind, player score is 30."""
    # Clubs, Spades, Diamonds, Hearts
    scoresOfSuit = [0,0,0,0]
    # Calculate the score of each suit. (P.S. I'm sorry)
    for card in player.hand:
      if card.suit == "Clubs":
        if card.rank == "A":
          scoresOfSuit[0] += 11
        elif card.score > 10:
          scoresOfSuit[0] += 10
        else:
          scoresOfSuit[0] += card.score
      if card.suit == "Spades":
        if card.rank == "A":
          scoresOfSuit[1] += 11
        elif card.score > 10:
          scoresOfSuit[1] += 10
        else:
          scoresOfSuit[1] += card.score
      if card.suit == "Diamonds":
        if card.rank == "A":
          scoresOfSuit[2] += 11
        elif card.score > 10:
          scoresOfSuit[2] += 10
        else:
          scoresOfSuit[2] += card.score
      if card.suit == "Hearts":
        if card.rank == "A":
          scoresOfSuit[3] += 11
        elif card.score > 10:
          scoresOfSuit[3] += 10
        else:
          scoresOfSuit[3] += card.score

    # NOTE: This MUST be 1, based on the short-circuiting below.
    # Updating the high score does NOT increment this counter.
    # ONLY occurrences of score == highScore increment.
    threeOfAKindCounter = 1
    highScore = 0

    for score in scoresOfSuit:
      if score > highScore:
        highScore = score
      elif score != 0 and score == highScore:
        threeOfAKindCounter += 1

    if threeOfAKindCounter == 3:
      return 30
    else:
      return highScore

    def defineHuman(self, player, allowed, prevPlay):
      print()