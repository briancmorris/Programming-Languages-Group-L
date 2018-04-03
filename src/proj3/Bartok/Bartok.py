from Game import Game


class Bartok(Game):
  def endCondition(self):
    for player in self.players:
        if player.noCardsLeft():
            self.winner = player
            return True
    return False

  def winMessage(self):
      print("The winner of bartok is: ")
      print(f"Player {self.winner.idNum}")

  def validPlays(self, hand, lastPlayed):
      validPlays = []
      # print (hand)
      # print (lastPlayed)
      # print(lastPlayed.__repr__())
      #print(type(lastPlayed[-1]))

      for card in hand:
          if card.rank == lastPlayed.rank or card.suit == lastPlayed.suit:
              validPlays.append(card)

      return validPlays

  def cantPlay(self, player):
      player.finished = True
      return player.next

  def playerPlayed(self, player, played):
      self.played.append(played)
      return player.next

  def dealHands(self):
      self.deck.shuffle()
      #for i in range(1, 5):
      for player in self.players:
        player.hand = self.deck.draw(5)

  def defineAI(self, player, allowed, prevPlay):
    # AI logic goes here!
    if player.skipped:
      player.skipped = False
      print("You have been skipped")
      return None

    if len(allowed) > 0:
      played = allowed[0]
      print("played %s" % played.__repr__())
    else:
      player.drawCard()
      print("No valid moves, you have to draw.")
      return prevPlay

    self.special_rules(player, played)

    return played

  def defineHuman(self, player, allowed, prevPlay):
    if player.skipped:
      player.skipped = False
      print("You have been skipped")
      return None

    print("Your current hand is {}".format(player.hand))
    if len(allowed) == 0:
      print("No valid moves, you have to draw.")
      myStr = "placeholder"
      while myStr != "":
        myStr = input("Press Enter to acknowledge...")
      player.drawCard()
      return None
    print("You can do the following:")

    for index, card in enumerate(allowed):
      print("{} {}".format(index, card.__repr__()))
    tbp = None
    while tbp is None:
      try:
        selected = int(input("Enter the index of the move you make: "))
        tbp = allowed[selected] if selected >= 0 else []
      except (ValueError, IndexError):
        print("Invalid selection")
        tbp = None

    if tbp is None:
      tbp = prevPlay

    self.special_rules(player, tbp)

    return tbp

  def special_rules(self, player, played):
    if type(played) is not None:
      player.hand = [card for card in player.hand if not card == played]

      if played.rank == "K":
        print("Played a King, next player draws two cards and is skipped.")
        player.next.skipped = True
        player.next.drawCard()
        player.next.drawCard()
      elif played.rank == "Q":
        print("Played a Queen, next player skipped.")
        player.next.skipped = True
      elif played.rank == "J":
        print("Played a Jack, next player forced to draw a card.")
        player.next.drawCard()

Bartok(numPlayers=1, numAI=1).play()
