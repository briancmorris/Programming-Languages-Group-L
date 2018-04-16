from Game import Game


class Blackjack(Game):
  def endCondition(self):
    """ The conditions as to which the game will end.  Defined by game implementer. """
    # If all players aren't finished, this is always false
    for player in self.players:
      if not player.finished:
        return False

    for player in self.players:
      # Define Player win condition
      if not player.AI:
        if player.finished:
          if (self.calculateScore(player) < self.calculateScore(self.findDealer()) <= 21) or self.calculateScore(
            player) > 21:
            self.losers.append(player)
          elif self.calculateScore(player) > self.calculateScore(self.findDealer()) or self.calculateScore(
            self.findDealer()) > 21:
            self.winners.append(player)
          else:
            self.tied.append(player)

    return True

  def winMessage(self):
    """ Message to display upon end game conditions being met.  Defined by game implementer. """
    if len(self.winners) > 0:
      for player in self.winners:
        print("Congratulations Player " + str(player.idNum) + ", you won the round!")
    else:
      print("No one won this round!")

    if len(self.losers) > 0:
      for player in self.losers:
        print("That's too bad Player " + str(player.idNum) + ", you lost the round.")
    else:
      print("No one lost this round!")

    if len(self.tied) > 0:
      for player in self.tied:
        print("You tied the dealer Player " + str(player.idNum) + ", nothing lost and nothing gained!")
    else:
      print("No one tied this round!")

  def validPlays(self, player, lastPlayed):
    """ List of valid plays a player can make.  Defined by game implementer. """
    validPlays = []

    if self.calculateScore(player) >= 21:
      # Redundant but helps sort things out mentally
      return None
    else:
      validPlays.append("hit")
      validPlays.append("stand")
    return validPlays

  def cantPlay(self, player):
    """ What to do if a player cannot play.  Defined by game implementer. """
    return player.next

  def playerPlayed(self, player, played):
    """ What the player (AI or Human) did.  Records it and returns the next player to go.
    Defined by game implementer. """
    self.played.append(played)
    # If the player hits, their hand must be re-evaluated so they can bust/go again
    if played == "hit":
      return player
    return player.next

  def dealHands(self):
    """ Deals hands to all the players, including the AI.  Defined by game implementer. """
    self.deck.shuffle()
    for player in self.players:
      self.deck.draw(player.hand, 2)

  def findDealer(self):
    """ Blackjack only method, finds the 'dealer', aka the only AI in the game. """
    for player in self.players:
      if player.AI:
        return player

  def defineAI(self, player, allowed, prevPlay):
    """ The AI players turn.  What they can do.  Defined by game implementer. """
    # AI logic goes here!
    print("Dealer's hand is:\n{}".format(player.hand))
    print("Dealer's current hand score is {}".format(player.score))
    if self.calculateScore(player) >= 17:
      played = "stand"
    else:
      played = "hit"

    print("Dealer {}s".format(played))
    if played == "hit":
      player.drawCard()
    else:
      player.finished = True

    myStr = "placeholder"
    while myStr != "":
      myStr = input("Press Enter to acknowledge...")
    return played

  def defineHuman(self, player, allowed, prevPlay):
    """ The human players turn.  What they can do.  Defined by game implementer. """
    print("Your current hand is :\n{}".format(player.hand))
    print("Your current hand score is {}".format(player.score))
    if allowed is not None:
      print("You can do the following:")
      for action, i in zip(allowed, range(0, len(allowed))):
        print("{} {}".format(i, action))
      # for index, card in enumerate(allowed):
      #   print("{} {}".format(index, card))
      tbp = None
      while tbp is None:
        try:
          selected = int(input("Enter the index of the move you make: "))
          tbp = allowed[selected] if selected >= 0 else []
        except (ValueError, IndexError):
          print("Invalid selection")
          tbp = None

      print("Player {}s".format(tbp))
      if tbp == "hit":
        player.drawCard()
      else:
        player.finished = True

      return tbp
    else:
      if self.calculateScore(player) > 21:
        print("You busted, sorry!")
      else:
        print("BLACKJACK!!!")
      player.finished = True
      return None

  def calculateScore(self, player):
    """ Calculates a players score.  Defined by writer of card game."""
    def containsAce(hand):
      """ Helper method, determines if an Ace is present """
      for card in hand:
        if card.rank == 'A':
          return True
      return False

    player.score = 0

    for card in player.hand:
      if card.score > 10:
        player.score += 10
      else:
        player.score += card.score

    if containsAce(player.hand):
      if player.score + 10 <= 21:
        player.score += 10

    return player.score


Blackjack(numPlayers=1, numAI=1).play()
