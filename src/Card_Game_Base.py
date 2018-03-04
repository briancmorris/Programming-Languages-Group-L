CARD_VALUES = {
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


class Card:
    """Base card class"""

    def __init__(self, value, suit):
        self.value = CARD_VALUES[str(value)]
        self.suit = suit
        self.faceUp = False

    def __repr__(self):
        return str(self.value) + " of " + self.suit


class Deck:
    def __init__(self):
        """ List of cards """
        self.cards = []
        self.suits = (['Hearts', 'Diamonds', 'Spades', 'Clubs'])
        self.initiate_deck()

    def __repr__(self):
        print("CURRENT DECK:")
        for suit in self.suits:
            print(str(suit.upper) + ": ")

    def fetch_cards_of_suit(self, suit):
        cards_of_suit = [card for card in self.cards if suit == card.suit]
        return cards_of_suit

    def initiate_deck(self):
        for suit in self.suits:
            for i in range(1, 14):
                new_card = Card(i, suit)
                self.cards.append(new_card)
