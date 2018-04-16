import random

""" Dictionary for converting Card values into names (mainly for face cards) """
NAME_BY_VALUE = {
    '1': 'Ace',
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    '10': 'Ten',
    '11': 'Jack',
    '12': 'Queen',
    '13': 'King'
}

""" Dictionary for converting Card names into values (mainly for face cards) """
VALUE_BY_NAME = {
    'Ace': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 11,
    'Queen': 12,
    'King': 13
}

""" Dictionary for converting Card values into names (mainly for face cards) """
CARD_VALUES = {
    'Ace': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10
}


class Card:
    """Base card class"""

    def __init__(self, value, suit):
        self.value = NAME_BY_VALUE[str(value)]
        self.suit = suit
        self.score = CARD_VALUES[self.value]
        self.faceDown = False
        self.symbol_dict = {'Hearts': '\u2665', 'Diamonds': '\u2666', 'Spades': '\u2660', 'Clubs': '\u2663'}

    def __repr__(self):
        ascii_card = '\n'.join(self.make_card())
        return ascii_card

    def make_card(self):
        two_digit = False
        value = VALUE_BY_NAME[self.value]

        # Formatting Boolean
        if value == 10:
            two_digit = True

        # If a face card, we want just the capital letter.
        if value > 10 or value == 1:
            value = self.value[0]
        suit = self.suit
        ascii_card = []
        space = " "
        suit_symbol = self.symbol_dict[suit]
        if two_digit:
            space = ""

        # Helps see formatting.  Prints space between quotes.
        # print('Space is: ' + "\"" + space + "\"")

        ascii_card.append('┌───────────────┐')
        ascii_card.append('│{}{}           │'.format(space, value))
        ascii_card.append('│             │')
        ascii_card.append('│             │')
        ascii_card.append('│     {}       │'.format(suit_symbol))
        ascii_card.append('│             │')
        ascii_card.append('│             │')
        ascii_card.append('│           {}{}│'.format(space, value))
        ascii_card.append('└───────────────┘')
        return ascii_card



class Deck:
    """ Base Deck Class."""

    def __init__(self):
        """ List of cards """
        self.cards = []
        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        self.initiate_deck()
        self.shuffle()

    def __repr__(self):
        """ Denotes how to print the Deck.  Prints each suit and all cards in the deck that are of that suit. """
        deck_string = ""

        for suit in self.suits:
            deck_string += suit + ":\n"
            for card in self.fetch_cards_of_suit(suit):
                deck_string += str(card.value) + " "
            deck_string += "\n"

        return deck_string

    def __getitem__(self, index):
        """ Allows the fetching of cards by index """
        return self.cards[index]

    def __len__(self):
        return len(self.cards)

    def fetch_cards_of_suit(self, suit):
        """ Fetches all the cards in the deck of a provided suit """

        def sort_by_value(card):
            """ Returns the value of the card based on it's value name """
            return VALUE_BY_NAME[card.value]

        cards_of_suit = [card for card in self.cards if suit == card.suit]

        # Sort for easy viewing.
        cards_of_suit.sort(key=sort_by_value)
        return cards_of_suit

    def initiate_deck(self):
        """ Initiates deck with all 52 cards, 13 of each suit (including Ace, Jack, Queen, and King)"""
        for suit in self.suits:
            for i in range(1, 14):
                new_card = Card(i, suit)
                self.cards.append(new_card)

    def remove(self, card):
        self.cards.remove(card)

    def shuffle(self):
        """ Shuffles the deck. """
        random.shuffle(self.cards)
