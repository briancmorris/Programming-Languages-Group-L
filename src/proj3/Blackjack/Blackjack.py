from Game import Game


class Blackjack(Game):
  def endCondition(self):
    # If all players aren't finished, this is always false
    for player in self.players:
      if not player.finished:
        return False

    for player in self.players:
      # Define Player win condition
      if not player.AI:
        if player.finished:
          if (player.calculateScore() < self.findDealer().calculateScore() <= 21) or player.calculateScore() > 21:
            self.losers.append(player)
          elif player.calculateScore() > self.findDealer().calculateScore() or self.findDealer().calculateScore() > 21:
            self.winners.append(player)
          else:
            self.tied.append(player)

    return True

  # Only defined for 1 winner at this point.
  def winMessage(self):
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

  # Defined for Blackjack
  def validPlays(self, player):
    validPlays = []
    # print (hand)
    # print (lastPlayed)

    if player.calculateScore() > 21:
      # Redundant but helps sort things out mentally
      return None
    else:
      validPlays.append("hit")
      validPlays.append("stand")
    return validPlays

  # Defined for Blackjack
  def cantPlay(self, player):
    return player.next

  def playerPlayed(self, player, played):
    self.played.append(played)
    # If the player hits, their hand must be re-evaluated so they can bust/go again
    if played == "hit":
      return player
    return player.next

  # Defined for Blackjack
  def dealHands(self):
    self.deck.shuffle()
    for player in self.players:
      player.hand = self.deck.draw(2)

  # Made for Blackjack
  def findDealer(self):
    for player in self.players:
      if player.AI:
        return player


Blackjack(numPlayers=1, numAI=1).play()
