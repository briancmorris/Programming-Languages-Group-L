from Game import Game
import random

class RollingStone(Game):
    startPlayer = None
    discardPile = []

    def endCondition(self):
        for player in self.players:
            if player.noCardsLeft():
                self.winner = player
                return True
        return False

    def winMessage(self):
        print("The winner of Rolling Stone is: ")
        print(f"Player {self.winner.idNum}")

    def validPlays(self, player, lastPlayed):
        validPlays = []

        if len(self.discardPile) is 0:
            for card in player.hand:
                validPlays.append(card)
        else:
            for card in player.hand:
                if card.suit == self.discardPile[-1].suit:
                    validPlays.append(card)
        return validPlays

    def cantPlay(self, player):
        # Add discarded cards to player's hand
        for card in self.discardPile:
            player.hand.cards.append(card)

        # Reset discard pile
        self.discardPile = []

        # Set player to be the start player
        self.startPlayer = player

        # Return itself as start player
        return player

    def playerPlayed(self, player, played):
        self.discardPile.append(played)
        p = self.special_rules(player, played)
        if p is None:
            return player.next
        else:
            return p

    def dealHands(self):
        # Remove unnecessary cards (2s,3s,4s,5s,6s)
        for i in range(0, 3):
            for card in self.deck.cards:
                if card.rank == "2" or card.rank == "3" or card.rank == "4" or card.rank == "5" or card.rank == "6":
                    self.deck.cards.remove(card)

        # Deal all the cards out to players equally
        for player in self.players:
            self.deck.draw(player.hand, 8)

        # Refill the deck so the game doesn't break
        self.deck.__init__()
        self.discardPile = []
        self.startPlayer = self.players[0]

    def defineAI(self, player, allowed, prevPlay):

        # If they can play, generate a random number between 1 and 3
        # If it is odd, play the first card allowed, otherwise, play the lowest allowed card
        # The randomness is added to make the games not take as long (hopefully)
        if len(allowed) > 0:
            rand = random.randint(1, 3)
            if rand % 2 != 0:
                #played = allowed[0]
                scores = []
                for card in allowed:
                    scores.append(card.score)
                m = 0
                maxScore = 0  # TODO CHANGE TO MIN
                for i in range(0, len(scores)):
                    if scores[i] < maxScore:
                        maxScore = scores[i]
                        m = i
                played = allowed[m]
            else:
                scores = []
                for card in allowed:
                    scores.append(card.score)
                m = 0
                minScore = 100 # TODO CHANGE TO MIN
                for i in range(0, len(scores)):
                    if scores[i] < minScore:
                        minScore = scores[i]
                        m = i
                played = allowed[m]

            print("Played \n%s" % played.__repr__())
        else:
            print("Had no valid moves and took the pile.\n")
            played = None
        return played

    def defineHuman(self, player, allowed, prevPlay):
        print("Your current hand is \n{}".format(player.hand))
        #print("P1 \n{}".format(player.next.hand))
        #print("P2 \n{}".format(player.next.next.hand))
        #print("P3 \n{}".format(player.next.next.next.hand))
        if len(allowed) == 0:
            print("No valid moves, you have to take all the cards.")
            myStr = "placeholder"
            while myStr != "":
                myStr = input("Press Enter to acknowledge...")
            return None
        print("You can do the following:")

        for index, card in enumerate(allowed):
            print("Index: {}\n{}".format(index, card.__repr__()))

        tbp = None
        while tbp is None:
            try:
                selected = int(input("Enter the index of the move you make: "))
                tbp = allowed[selected] if selected >= 0 else []
            except (ValueError, IndexError):
                print("Invalid selection")
                tbp = None
        return tbp

    def special_rules(self, player, played):
        if type(played) is not None:
            player.hand.cards = [card for card in player.hand if not card == played]
        if player.next == self.startPlayer:
            # If everyone is able to play, see who played the highest card and make them
            # pick up the discard pile and start a new round.
            scores = []
            for card in self.discardPile:
                scores.append(card.score)
            m = 0
            maxScore = 0
            for i in range(0, len(scores)):
                if scores[i] > maxScore:
                    maxScore = scores[i]
                    m = i

            # Make sure that the player gets to play a card after picking up the cards
            p = player
            for x in range(0, m+1):
                p = p.next
            self.startPlayer = p

            print("Everyone went and Player {} played the highest card so they take the deck!".format(p.idNum))

            # Add cards to the players hand
            for card in self.discardPile:
                p.hand.cards.append(card)

            self.discardPile = []
            # Return the player
            return p
        return None


RollingStone(numPlayers=1, numAI=3).play()
