from Game import Game

class ThirtyOne(Game):
  lives = []
  discardPile = []
  theOneWhoKnocked = None

  def restoreLives(self):
    """Restores the lives of all players in the game."""
    self.lives = []
    for player in self.players:
      self.lives.append(3)

  def endCondition(self):
    """Defines the end condition of the game, 1 player has 1 or more lives."""
    potentialWinners = []
    for player in self.players:
      if self.lives[player.idNum] == 0:
        self.losers.append(player)
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
    player.finished = self.lives[player.idNum] == 0
    return player.next

  def validPlays(self, player, lastPlayed):
    """Return a list of valid players for a player. Empty if player can't play."""
    if player.finished:
      return []
    elif self.theOneWhoKnocked is not None:
      return [self.drawFromStock, self.drawFromDiscard]
    else:
      return [self.drawFromStock, self.drawFromDiscard, self.knock]

  def drawFromStock(self, player):
    """Player draws from stock, must discard any card from their hand afterward."""
    player.drawCard()
    print("Player " + str(player.idNum) + " drew from the deck.")

  def drawFromDiscard(self, player):
    """Player draws from discard pile, must discard a different card afterward."""
    card = self.discardPile.pop()
    player.hand.cards.append(card)
    print("Player " + str(player.idNum) + " drew\n" + card.__repr__())

  def knock(self, player):
    """Player knocks, each player has one round left to change their hand."""
    print("Player " + str(player.idNum) + " knocks! Everyone has 1 chance left!")
    self.theOneWhoKnocked = player

  def dealHands(self):
    """Deals 3 cards to each player, initiates discard pile to a single card."""
    self.deck.shuffle()
    for player in self.players:
      self.deck.draw(player.hand, 3)
    self.discardPile.append(self.deck.cards.pop())
    self.restoreLives()

  def playerPlayed(self, player, played):
    """Appends discarded card from player to discard pile, returns the next player."""
    if played is not None:
      print("Player " + str(player.idNum) + " discarded\n" + played.__repr__())
      self.discardPile.append(played)
    if player.next == self.theOneWhoKnocked:
      # Get the scores of all players.
      scores = []
      for p in self.players:
        scores.append(self.calculateScore(p))

      # Find the high score for all players.
      highScore = -1
      # Used to keep track of high scoring players.
      highScoreMatches = None
      for i in range(len(scores)):
        if scores[i] > highScore:
          highScore = scores[i]
          highScoreMatches = [0 for player in self.players]
          highScoreMatches[i] = 1
        elif scores[i] == highScore:
          highScoreMatches[i] = 1

      print("--------------------------------------")
      print("        End of Round Results          ")
      print("--------------------------------------")

      numLosers = 0
      # Subtract a life from the players that do not share the high score.
      for j in range(len(highScoreMatches)):
        if highScoreMatches[j] == 0:
          self.lives[j] -= 1
          print("Player " + str(j) + " now has " + str(self.lives[j]) + " lives!")
          numLosers +=1
      if numLosers == 0:
        print("Draw! No one lost a life!")
      self.theOneWhoKnocked = None
      return player.next
    else:
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
    # Player has been eliminated.
    if len(allowed) == 0:
      print("You have already been eliminated!")
      return None

    # Display hand and prompt for input.
    print("The top of the discard pile is:\n" + self.discardPile[len(self.discardPile) - 1].__repr__())
    print("Your hand score is: " + str(self.calculateScore(player)))
    print("Your current hand is \n{}".format(player.hand))
    print("You can do the following:")

    if len(allowed) == 3:
      print("Draw a card from the stock pile (0), draw a card from the discard pile (1), or knock (2).")
    # Player can't knock, someone already did.
    else:
      print("Draw a card from the stock pile (0) or draw a card from the discard pile (1).")

    actionSelected = None
    action = None
    while action is None:
      try:
        actionSelected = int(input("Enter the index of the action you wish to take: "))
        action = allowed[actionSelected] if actionSelected >= 0 else None
      except (ValueError, IndexError):
        print("Invalid selection.")
        action = None

    action(player)

    # Prompt for discard after a draw action.
    if actionSelected < 2:
      for index, card in enumerate(player.hand.cards):
        print("Index: {}\n{}".format(index, card.__repr__()))
      print("Which card will you discard?")

      discarded = None
      while discarded is None:
        try:
          cardSelected = int(input("Enter the index of the move you make: "))
          discarded = player.hand[cardSelected] if cardSelected >= 0 else None
        except (ValueError, IndexError):
          print("Invalid selection.")
          discarded = None
      player.hand.cards.remove(discarded)
      self.playerPlayed(player, discarded)
    # Player knocked.
    else:
      self.playerPlayed(player, None)


  def defineAI(self, player, allowed, prevPlay):
    if len(allowed) == 0:
      print("Player " + str(player.idNum) + " has already been eliminated!")
      return None

    else:
      allowed[0](player)
      discarded = player.hand[0]
      player.hand.cards.remove(discarded)
      self.playerPlayed(player, discarded)

ThirtyOne(numPlayers=1, numAI=1).play()