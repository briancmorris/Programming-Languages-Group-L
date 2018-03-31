class Card:
    """Base card class"""

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.faceUp = False


class Deck:
    def __init__(self):
        """ List of cards """
        deck = []
        suits = (['hearts', 'diamonds', 'spades', 'clubs'])
        value_matching = {
            '1': 'ace',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine',
            '10': 'ten',
            '11': 'jack',
            '12': 'queen',
            '13': 'king'
        }
        self.initiate_deck();

    def initiate_deck(self):
        for suit in self.suits:
            for i in range(1, 14):
                new_card = Card(suit, i)
                deck.append(new_card)


class Game:
    def __init__(self):
        self.start()
        deck = Deck()

    def print_game_state(self):
        print("Deck is currently: {}".format(self.deck))


game = Game()
game.print_game_state()