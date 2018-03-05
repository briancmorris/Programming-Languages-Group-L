from Card_Game_Base import *
import random

""" Set a seed for testing purposes """
random.seed(1)


class Game:
    """ Game Class.  Represents the entire game state.  Keeps track of turns and players, as well as the deck. """

    def __init__(self):
        self.deck = Deck()
        self.Num_Players = 1
        self.Players = []
        self.Dealer = Dealer("Dealer")
        self.Turn = Turn(self.Dealer)

    def print_game_state(self):
        """ Prints the current game state, including the deck, players, and the dealer"""
        print("~~~~~~ GAME STATE ~~~~~~")
        print("DECK IS CURRENTLY: \n{}".format(self.deck))
        print("\nPLAYERS:")
        for player in self.get_players():
            print(player)
        print("\nDEALER:")
        print(self.get_dealer())
        print("~~~~~~ END GAME STATE ~~~~~~")

    def add_player(self, player):
        self.Players.append(player)

    def get_players(self):
        """ Returns all players in the game (not dealer) """
        return self.Players

    def get_dealer(self):
        """ Returns the dealer in the game """
        return self.Dealer

    def start_game(self):
        print("Dealer is dealing your cards!\n")
        self.start_round()

    def start_round(self):
        # Deal out cards to all players and the Dealer
        self.Dealer.deal()
        self.Dealer.deal_self()

        # Print out deal
        print("The Dealer's Hand Is:")
        print(self.get_dealer().Hand)

        for player in game.get_players():
            print(player.Name + "'s Hand:")
            print(player.Hand)

        # Make it the first players turn
        self.Turn.advance_turn()

    def new_round(self):
        """ Reset game state but NOT deck. """
        self.Dealer.has_dealt = False
        self.Dealer.hand = []
        for player in self.get_players():
            player.Hand = []

        self.Turn = Turn(self.Dealer)
        self.start_round()

    def evaluate_state(self):
        winning_players = []
        losing_players = []
        tied_players = []
        print("~~~ Round Over! ~~~")
        print("Dealer Hand Value: " + str(self.Dealer.Hand.get_value()))
        print("Players Hand Values: ")
        for player in self.get_players():
            print(player.Name + ": " + str(player.Hand.get_value()))

        for player in self.get_players():
            if player.Hand.get_value() < self.get_dealer().Hand.get_value() or player.Hand.get_value() > 21:
                losing_players.append(player)
            elif player.Hand.get_value() < self.get_dealer().Hand.get_value():
                winning_players.append(player)
            else:
                tied_players.append(player)

        if len(winning_players) > 0:
            for player in winning_players:
                print("Congratulations " + player.Name + ", you won the round!")

        if len(losing_players) > 0:
            for player in losing_players:
                print("That's too bad " + player.Name + ", you lost the round.")

        if len(tied_players) > 0:
            for player in tied_players:
                print("You tied the dealer " + player.Name + ", nothing lost and nothing gained!")




class Hand:
    """ Hand of cards.  Belongs to a player.  In Blackjack, this will start off as only two cards. """

    def __init__(self):
        self.owner = None
        self.cards = []
        self.ace_present = False
        self.value = self.get_value()

    def set_owner(self, owner):
        self.owner = owner

    def add_card(self, card):
        """ Adds a card to the hand. """
        self.cards.append(card)
        if card.value == 'Ace':
            self.ace_present = True

    def get_value(self):
        """ Gets the current value of the hand. """
        value = 0
        if not self.ace_present:
            for card in self.cards:
                value += card.score
        else:
            """ Ace is present, we need to calculate if it should be 1 or 11."""
            for card in self.cards:
                value += card.score

            # If taking the ace as an 11 doesn't bust, use it as 11
            if value + 10 <= 21:
                value += 10

        return value

    def __getitem__(self, index):
        """ Allows the fetching of cards by index """
        return self.cards[index]

    def __repr__(self):
        """
        Determines how to print the Hand as a string.
        :return: The hand as a string in the format <value> of <suit>
        """
        hand_string = ""
        for card in self.cards:
            hand_string += card.value + " of " + card.suit + "\n"

        hand_string += "Value: " + str(self.get_value()) + "\n"

        return hand_string


class Turn:
    """ Keeps track of whose turn it is.  Tracked in the Game Class. """

    def __init__(self, player):
        self.Turn_Number = 0
        self.Player = player
        self.player_index = 0
        self.action_table = {
            "hit": self.hit,
            "stand": self.stand
        }

    def advance_turn(self):
        if isinstance(self.Player, Dealer):
            self.Player = game.get_players()[self.player_index]

        self.player_index += 1
        # If we are at the end of the player list, set the index back to zero and make it Dealer turn.
        if self.player_index > len(game.get_players()):
            self.player_index = 0
            self.Player = game.get_dealer()
            self.dealer_turn()
        else:
            self.player_turn()

    def dealer_turn(self):
        print("It's the dealer's turn")
        # Just in case
        # assert(self.Player is Dealer, "Not a dealer in dealer_turn.  What?")
        if self.Player.Hand.get_value() >= 17:
            self.stand()

    def player_turn(self):
        print("It's player " + self.Player.Name + "'s turn!")
        action = ""
        acceptable_input = False
        while not acceptable_input:
            action = input("What would you like to do?\nHit  |  Stand\n>  ").lower()
            if action == "hit" or action == "stand":
                acceptable_input = True
            else:
                print("\nPlease enter a valid action!\n")

        print("\n")

        # Basically a switch case.  Take an action, run dictionary functions based on action-key
        self.action_table[action]()

    def hit(self):
        """ A player or the Dealer hits.  Draw a card from deck, add to their hand."""
        print(self.Player.Name + " Hits")
        self.Player.draw_card()
        print(self.Player.Name + "'s New Hand:")
        print(self.Player.Hand)

        # If under 21, allow player to take another turn.  Otherwise, they bust or have 21.
        if self.Player.Hand.get_value() < 21:
            self.player_turn()
        elif self.Player.Hand.get_value() > 21:
            print("BUST")
            self.advance_turn()
        else:
            print("BLACKJACK!!!!")

    def stand(self):
        """ A player or the Dealer stands.  Advance to next turn. """
        print(self.Player.Name + " Stands")
        if not isinstance(self.Player, Dealer):
            self.advance_turn()
        else:
            game.evaluate_state()


class Player:
    """ Player class.  In Blackjack, you can be a player or the dealer.  Has a Hand. """

    def __init__(self, name):
        self.Name = name
        self.Hand = Hand()
        # Just putting this in for now, unused.
        self.Money = 0

    def __repr__(self):
        """
        Returns the player as a string.
        :return: The player as a string, including their Name and Hand.
        """
        player_string = "Name:  " + self.Name + "\nHand:\n" + str(self.Hand) + "Hand Value: " + str(
            self.Hand.get_value())
        return player_string

    def draw_card(self):
        self.Hand.add_card(game.deck[0])
        game.deck.remove(game.deck[0])


class Dealer(Player):
    """ Dealer class.  Extends Player. """

    def __init__(self, name):
        Player.__init__(self, name)
        self.has_dealt = False

    def __repr__(self):
        """
        Returns the player as a string.
        :return: The player as a string, including their Name and Hand.
        """
        dealer_string = "Dealer Hand:\n" + str(self.Hand) + "Hand Value: " + str(
            self.Hand.get_value())
        return dealer_string

    @staticmethod
    def deal():
        """ Deals to all players in the game (NOT the dealer)"""
        for i in range(2):
            for player in game.get_players():
                player.draw_card()

                # print("Current deck length is : {}".format(len(game.deck)))

    def deal_self(self):
        """ Deals to all players in the game (NOT the dealer)"""
        for i in range(2):
            self.draw_card()

        self.Hand[1].faceDown = True

        self.has_dealt = True

        # print("Current deck length is : {}".format(len(game.deck)))


print("Welcome to Blackjack!\n")
game = Game()
Player1 = Player("Alex")
game.add_player(Player1)
game.start_game()
# print(game.deck.fetch_cards_of_suit('Hearts'))
# game.print_game_state()
# game.print_game_state()
