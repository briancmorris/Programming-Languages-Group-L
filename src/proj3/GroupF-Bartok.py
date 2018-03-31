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
        print(self.winner)

    def validPlays(self, hand, lastPlayed):
        validPlays = []
        # print (hand)
        # print (lastPlayed)
        if lastPlayed:
            for card in hand:
                if card.rank == lastPlayed.rank or card.suit == lastPlayed.suit:
                    validPlays.append(card)
        else:
            validPlays += hand
        return validPlays

    def cantPlay(self, player):
        player.finished = True
        return player.next

    def playerPlayed(self, player, played):
        self.played.append(played)
        return player.next

    def dealHands(self):
        self.deck.shuffle()
        for player in self.players:
            player.hand = self.deck.draw(7)


Bartok(numPlayers=1, numAI=3).play()
