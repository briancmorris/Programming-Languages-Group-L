from Game import Game


class ThirtyOne(Game):

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
    print("Player " + str(player.idNum) + " took:\n" + card.__repr__())

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

  def playerPlayed(self, player, played):
    """Appends discarded card from player to discard pile, returns the next player."""
    if played is not None:
      print("Player " + str(player.idNum) + " discarded\n" + played.__repr__())
      self.discardPile.append(played)
      if player.AI:
        myStr = "placeholder"
        while myStr != "":
          myStr = input("Press Enter to acknowledge...")
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
      # Redeal hands.
      for player in self.players:
        player.hand.cards = []
      self.dealHands()

      numLosers = 0
      # Subtract a life from the players that do not share the high score.
      for j in range(len(highScoreMatches)):
        if highScoreMatches[j] == 0:
          self.lives[j] -= 1
          print("Player " + str(j) + " now has " + str(self.lives[j]) + " lives!")
          numLosers += 1
      if numLosers == 0:
        print("Draw! No one lost a life!")
      self.theOneWhoKnocked = None
      myStr = "placeholder"
      while myStr != "":
        myStr = input("Press Enter to acknowledge...")
      return player.next
    else:
      return player.next

  def calculateScore(self, player):
    """Calculates the score of a player's hand. The sum of 1 suit or highest card.
        If there's a 3 of a kind, player score is 30."""
    # Clubs, Spades, Diamonds, Hearts
    scoresOfSuit = {'Clubs': 0, 'Spades': 0, 'Diamonds': 0, 'Hearts': 0}
    # Calculate the score of each suit. (P.S. I'm sorry)
    for card in player.hand.cards:
      tmpScore = 0
      if card.rank == "A":
        tmpScore += 11
      elif card.score > 10:
        tmpScore += 10
      else:
        tmpScore += card.score

      scoresOfSuit[card.suit] += tmpScore

    # NOTE: This MUST be 1, based on the short-circuiting below.
    # Updating the high score does NOT increment this counter.
    # ONLY occurrences of score == highScore increment.
    threeOfAKindCounter = 1
    highScore = 0

    for key, value in scoresOfSuit.items():
      if value > highScore:
        highScore = value
      elif value != 0 and value == highScore:
        threeOfAKindCounter += 1
    if threeOfAKindCounter == 3:
      return 30
    else:
      return highScore

  def defineHuman(self, player, allowed, prevPlay):
    """Defines the actions a human can take."""
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
      print("Draw a card from the stock pile (0), draw the top card from the discard pile (1), or knock (2).")
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
          cardSelected = int(input("Enter the index of the card to discard: "))
          if cardSelected == 3 and action == allowed[1]:
            print("Invalid selection. You cannot discard the card you just took from the discard pile!")
            continue
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
    """Defines basic AI behavior. Knocks if score is >= 28, draws from discard pile if it will
       provide the player with a better hand, and draws from the deck if not."""
    # Player eliminated.
    if len(allowed) == 0:
      print("Player " + str(player.idNum) + " has already been eliminated!")
      return None

    # Handle possible options.
    else:
      # Current hand's score.
      currentScore = self.calculateScore(player)
      # If the current score is reasonably high, knock.
      if currentScore >= 24 and len(allowed) > 2:
        allowed[2](player)
        self.playerPlayed(player, None)
        return None
      # Time to check for potentially better scores on the discard pile.
      else:
        currentHand = player.hand.cards
        topDiscarded = self.discardPile.pop()
        for card in player.hand.cards:
          player.hand.cards.remove(card)
          player.hand.cards.append(topDiscarded)
          tempScore = self.calculateScore(player)

          # Remove the discard pile card from hand.
          player.hand.cards.remove(topDiscarded)

          # If the score is better than before, take the discarded card.
          if tempScore > currentScore:
            # Call the drawFromDiscard function.
            self.discardPile.append(topDiscarded)
            allowed[1](player)
            self.discardPile.append(card)
            self.playerPlayed(player, card)
            return None

        # The discarded card did not provide a higher score, add it back to the pile.
        self.discardPile.append(topDiscarded)
        # Reset player hand.
        player.hand.cards = currentHand

        # Draw from deck and discard the first card in hand.
        allowed[0](player)
        discarded = player.hand.cards[0]
        player.hand.cards.remove(discarded)
        self.playerPlayed(player, discarded)


ThirtyOne(numPlayers=1, numAI=1).play()
