from Card_Game_Base import *


class Game:
    def __init__(self):
        self.deck = Deck()

    def print_game_state(self):
        print("Deck is currently: {}".format(self.deck))


game = Game()
print(game.deck.fetch_cards_of_suit('Hearts'))
# game.print_game_state()
