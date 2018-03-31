from Player import Player
from Deck import Deck
from Card import Card

"""
games need to define validPlays, cantPlay, getNext, distribute cards, winCondition, and winMessage
"""


class Game(object):
  def __init__(self, numPlayers=1, numAI=1):
    """
    basic set up for a game where:
    numPlayers = the total number of  human players
    numAI = the number of the total players that are AI
    """
    self.totPlayers = numPlayers + numAI
    # checking that there are atleast 2 players
    if (self.totPlayers) < 2:
      raise Exception('need atleast 2 players to play the game')

    self.deck = Deck()

    self.numPlayers = numPlayers
    self.numAI = numAI

    self.winners = []
    self.losers = []
    self.tied = []

    # setting up the players
    self.players = []
    [self.players.append(Player(len(self.players), game=self, AI=len(self.players) >= numPlayers)) for i in
     range(numPlayers + numAI)]

    for i in range(len(self.players)):
      self.players[i].setPrev(self.players[i - 1])
      self.players[i].setNext(self.players[(i + 1) % len(self.players)])

  def play(self):
    self.dealHands()
    self.played = [[]]
    player = self.players[0]
    while not self.endCondition():
      print("--------------------------------------")
      print("It is player " + str(player.idNum) + " turn")
      played = player.play()
      player = self.playerPlayed(player, played) if played else self.cantPlay(player)

    self.winMessage()

  def refillDeck(self):
    keep = [self.played.pop()]
    add = []
    toAdd = self.played
    for it in toAdd:
      if type(it) is Card:
        add.append(it)

    self.deck.refill(add)
    self.played = keep
    print("+++++++++++++++++++++++++++deck refilled from discarded +++++++++++++++")
    print(self.played)

  def endCondition(self):
    raise Exception("implemention must define this")

  def validPlays(self, player):
    raise Exception("implemention must define this")

  def cantPlay(self, player):
    raise Exception("implemention must define this")

  def playerPlayed(self, player, played):
    raise Exception("implemention must define this")

  def dealHands(self):
    raise Exception("implemention must define this")

  def winMessage(self):
    raise Exception("implementation must define this")

  def __str__(self):
    return str(self.players)
