from Card_Game_Base import *
import random


class Hand:
    """ Hand of cards.  Belongs to a player.  In Bartok, this will start off as five cards. """

    def __init__(self):
        self.owner = None
        self.cards = []
        self.jack_present = False
        self.queen_present = False
        self.king_present = False
        self.has_bartok = False

    def set_owner(self, owner):
        """ Sets the owner of this hand. """
        self.owner = owner

    def add_card(self, card):
        """ Adds a card to the hand. """
        self.cards.append(card)

        # Check if the card is a face card.
        if card.value == 'Jack':
            self.jack_present = True
        elif card.value == 'Queen':
            self.queen_present = True
        elif card.value == 'King':
            self.king_present = True

    def remove_card(self, index):
        """ Removes a card from the hand. """
        self.cards.pop(index)

        # Check if len is 1, if so the player has Bartok.
        if len(self.cards) == 1:
            self.has_bartok = True

    def __getitem__(self, index):
        """ Allows the fetching of cards by index """
        return self.cards[index]

    def __repr__(self):
        """
        Determines how to print the Hand as a string.
        :return: The hand as a string in the format <value> of <suit>
        """
        hand_string = ""
        hand_array = []
        total_hand = ["" for i in range(9)]

        # For every card in my hand, add it's ascii version to an array.
        for card in self.cards:
            ascii_card = card.make_card()
            hand_array.append(ascii_card)

        # Add all cards row by row to the total hand.
        for i in range(9):
            for card_pic in hand_array:
                total_hand[i] += card_pic[i] + " "

        hand_string += '\n'.join(total_hand)

        # Return picture version of hand
        return hand_string


class Player:
    """ Player class.  In Blackjack, you can be a player or the dealer.  Has a Hand. """

    def __init__(self, name):
        self.Name = name
        self.Hand = Hand()

    def __repr__(self):
        """
        Returns the player as a string.
        :return: The player as a string, including their Name and Hand.
        """
        player_string = "Name:  " + self.Name + "\nHand:\n" + str(self.Hand)
        return player_string

    def draw_card(self):
        """ Draws a card from the deck and adds it to the hand. """
        self.Hand.add_card(game.deck[0])
        game.deck.remove(game.deck[0])

    def discard_card(self, index):
        """ Discards a card from the hand at the given index. """
        game.discarded.append(self.Hand.cards[index])
        self.Hand.remove_card(index)

    def reset(self):
        """ Resets the hand of the player to be empty. """
        self.Hand = Hand()


class Dealer(Player):
    """ Dealer class.  Extends Player. """

    def __init__(self, name):
        Player.__init__(self, name)

    def __repr__(self):
        """
        Returns the player as a string.
        :return: The player as a string, including their Name and Hand.
        """
        dealer_string = "Dealer Hand:\n" + str(self.Hand)
        return dealer_string

    @staticmethod
    def deal():
        """ Deals to all players in the game (INCLUDING the dealer)"""
        for i in range(5):
            for player in game.get_players():
                player.draw_card()
                player.Hand[i].faceDown = True
        game.discarded.append(game.deck[0])
        game.deck.remove(game.deck[0])

    def reset(self):
        """ Resets the hand of the dealer. """
        self.Hand = Hand()


class Turn:
    """ Keeps track of whose turn it is.  Tracked in the Game Class. """

    def __init__(self, player):
        self.Turn_Number = 0
        self.Player = player
        self.player_index = 0
        self.action_table = dict(draw=self.draw, discard=self.discard, bartok=self.bartok, dr=self.draw,
                                 di=self.discard, b=self.bartok, j=self.play_jack, q=self.play_queen,
                                 k=self.play_king)

    def advance_turn(self, effect):
        # Check if we need more cards.
        game.check_deck()

        # If we are at the end of the player list, take the dealer's turn and reset index.
        if self.player_index >= len(game.get_players()):
            self.Player = game.get_players()[0]
            self.player_index = 1
            self.player_turn(effect)
        else:
            self.Player = game.get_players()[self.player_index]
            self.player_index += 1
            self.player_turn(effect)

    def player_turn(self, effect):
        if effect == "jack":
            print("You had to draw 1 card.")
            self.Player.draw_card()
        elif effect == "queen":
            print("Skipped.")
            self.advance_turn(None)
            # SKIP
        elif effect == "king":
            print("You had to draw 2 cards and got skipped.")
            self.Player.draw_card()
            self.Player.draw_card()
            self.advance_turn(None)
            # SKIP

        print("It's player " + self.Player.Name + "'s turn!")
        action = ""
        acceptable_input = False
        while not acceptable_input:
            print("The top of the discard pile is:")
            discarded_top = game.discarded.pop()
            print(discarded_top)
            game.discarded.append(discarded_top)

            print("Your hand is:")
            print(self.Player.Hand)
            action = input(
                "What would you like to do?\n(Dr)aw | (Di)scard | Play (J)ack, (Q)ueen, or (K)ing\n> ").lower()

            # Check input for validity.
            if action == "dr" or action == "draw":
                acceptable_input = True
            elif action == "di" or action == "discard":
                acceptable_input = True
            elif action == "j" or action == "jack":
                acceptable_input = True
            elif action == "q" or action == "queen":
                acceptable_input = True
            elif action == "k" or action == "king":
                acceptable_input = True
            else:
                print("\nPlease enter a valid action!\n")
            print("\n")

            # Basically a switch case.  Take an action, run dictionary functions based on action-key
            self.action_table[action]()

    def draw(self):
        """ Draws a card for the current player. """
        self.Player.draw_card();
        self.advance_turn(None)

    def discard(self):
        """ Discards a card for the current player. """
        discard = input("Which card would you like to discard? (0-" + str(len(self.Player.Hand.cards) - 1) + ")\n> ")
        discard_int = int(discard)

        # Check bounds.
        if discard_int < 0 or discard_int > len(self.Player.Hand.cards) - 1:
            print("Invalid card index, please try again!")
            self.player_turn(None)

        discard_card = self.Player.Hand.cards[discard_int]
        discard_pile_top = game.discarded.pop()
        game.discarded.append(discard_pile_top)

        # Check if the card is valid to be discarded.
        if discard_card.suit == discard_pile_top.suit:
            self.Player.discard_card(discard_int)
        elif discard_card.value == discard_pile_top.value:
            self.Player.discard_card(discard_int)
        else:
            print("This card does not share the same suit or value as the top of the discard pile!")
            print("Please try again!")
            self.player_turn(None)

        # Check if the player has Bartok or has won. Else, go to the next player.
        if len(self.Player.Hand.cards) == 1:
            self.bartok()
            self.advance_turn(None)
        elif len(self.Player.Hand.cards) == 0:
            game.evaluate_state()
        else:
            self.advance_turn(None)

    def play_jack(self):
        discard = input("What card is the jack would you like to discard? (number)")
        discard_int = int(discard)
        if discard_int < 0 or discard_int > len(self.Player.Hand.cards) - 1:
            print("Invalid card index, please try again!")
            self.player_turn(None)

        discard_card = self.Player.Hand.cards[discard_int]
        discard_pile_top = game.discarded.pop()
        game.discarded.append(discard_pile_top)

        # Check if the card is valid to be discarded.
        if discard_card.suit == discard_pile_top.suit:
            self.Player.discard_card(discard_int)
        elif discard_card.value == discard_pile_top.value:
            self.Player.discard_card(discard_int)
        else:
            print("This card does not share the same suit or value as the top of the discard pile!")
            print("Please try again!")
            self.player_turn(None)

        # Check if the player has Bartok or has won. Else, go to the next player.
        if len(self.Player.Hand.cards) == 1:
            self.bartok()
            self.advance_turn("jack")
        elif len(self.Player.Hand.cards) == 0:
            game.evaluate_state()
        else:
            self.advance_turn("jack")

    def play_queen(self):
        discard = input("What card is the queen would you like to discard? (number)")
        discard_int = int(discard)
        if discard_int < 0 or discard_int > len(self.Player.Hand.cards) - 1:
            print("Invalid card index, please try again!")
            self.player_turn(None)

        discard_card = self.Player.Hand.cards[discard_int]
        discard_pile_top = game.discarded.pop()
        game.discarded.append(discard_pile_top)

        # Check if the card is valid to be discarded.
        if discard_card.suit == discard_pile_top.suit:
            self.Player.discard_card(discard_int)
        elif discard_card.value == discard_pile_top.value:
            self.Player.discard_card(discard_int)
        else:
            print("This card does not share the same suit or value as the top of the discard pile!")
            print("Please try again!")
            self.player_turn(None)

        # Check if the player has Bartok or has won. Else, go to the next player.
        if len(self.Player.Hand.cards) == 1:
            self.bartok()
            self.advance_turn("queen")
        elif len(self.Player.Hand.cards) == 0:
            game.evaluate_state()
        else:
            self.advance_turn("queen")

    def play_king(self):
        discard = input("What card is the king would you like to discard? (number)")
        discard_int = int(discard)
        if discard_int < 0 or discard_int > len(self.Player.Hand.cards) - 1:
            print("Invalid card index, please try again!")
            self.player_turn(None)

        discard_card = self.Player.Hand.cards[discard_int]
        discard_pile_top = game.discarded.pop()
        game.discarded.append(discard_pile_top)

        # Check if the card is valid to be discarded.
        if discard_card.suit == discard_pile_top.suit:
            self.Player.discard_card(discard_int)
        elif discard_card.value == discard_pile_top.value:
            self.Player.discard_card(discard_int)
        else:
            print("This card does not share the same suit or value as the top of the discard pile!")
            print("Please try again!")
            self.player_turn(None)

        # Check if the player has Bartok or has won. Else, go to the next player.
        if len(self.Player.Hand.cards) == 1:
            self.bartok()
            self.advance_turn("king")
        elif len(self.Player.Hand.cards) == 0:
            game.evaluate_state()
        else:
            self.advance_turn("king")

    def bartok(self):
        """Claims Bartok for a Player"""
        print("" + self.Player.Name + " exclaims Bartok!")


class Game:
    """ Game Class.  Represents the entire game state.  Keeps track of turns and players, as well as the deck. """

    def __init__(self):
        self.deck = Deck()
        self.discarded = []
        self.Num_Players = 1
        self.Players = []
        self.Dealer = Dealer("Dealer")
        self.Players.append(self.Dealer)
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
        """ Adds a player to the game. """
        self.Players.append(player)

    def get_players(self):
        """ Returns all players in the game (including dealer) """
        return self.Players

    def get_dealer(self):
        """ Returns the dealer in the game """
        return self.Dealer

    def start_game(self):
        """ Start the game. """
        print("Dealer is dealing your cards!\n")
        self.start_round()

    def start_round(self):
        # Deal out cards to all players and the Dealer
        self.Dealer.deal()

        # Print out deal
        print("The Dealer's Hand Is:")
        print(self.get_dealer().Hand)

        for player in game.get_players():
            print(player.Name + "'s Hand:")
            print(player.Hand)

        # Make it the dealer's turn
        self.Turn.advance_turn(None)

    def reset(self):
        """ Reset game state. """
        self.deck = Deck()
        self.get_dealer().reset()
        for player in self.get_players():
            player.reset()
        self.Turn = Turn(self.Dealer)
        self.start_round()

    def evaluate_state(self):
        """ Evaluate the game state.  Says who won and who lost.  Prompts for a new round. """
        winning_players = []
        losing_players = []
        print("~~~ Game Over! ~~~")

        for player in self.get_players():
            if len(player.Hand.cards) > 0:
                losing_players.append(player)
            else:
                winning_players.append(player)

        if len(winning_players) > 0:
            for player in winning_players:
                print("Congratulations " + player.Name + ", you won the game!")

        if len(losing_players) > 0:
            for player in losing_players:
                print("That's too bad " + player.Name + ", you lost the game.")

        again = input("Do you want to play another game?  ((Y)es | (N)o)\n> ").lower()
        if again == 'yes' or again == 'y':
            self.reset()
        elif again == 'no' or again == 'n':
            print("Thanks for playing!")
        else:
            print("Please enter a valid option.")

    def check_deck(self):
        """ If we start to run out of cards, just grab a new deck...basically reshuffle."""
        if len(self.deck) < 10:
            self.deck = Deck()


print("Welcome to Bartok!\n")
game = Game()
Player1 = Player("Brian")
game.add_player(Player1)
game.start_game()
