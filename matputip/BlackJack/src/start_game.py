import inquirer

from utils import pause
from cards import Deck
from player import Player


class BlackJack:
    def __init__(self):
        self.deck = Deck()

        self.dealer = Player(True)
        self.player = Player()
        self.players = [self.dealer, self.player]

        self.turn = 1
        self.current_player = self.players[self.turn]

        self.player_choice = [
            inquirer.List(
                'player_choice',
                message="What's your move?",
                choices=["Hit", "Stand"]
            )
        ]

    def new_game(self):
        print('{:*^30}'.format(" Welcome to BlackJack! "))
        pause()
        self.deck.shuffle()
        self.deal(2)
        self.full_status()

    def deal(self, card_count=1):
        remaining = card_count

        while remaining > 0:
            for player in self.players:
                card = next(self.deck.card())
                player.hand.add_card(card)

            remaining -= 1

    def hit(self):
        card = next(self.deck.card())
        self.current_player.hand.add_card(card)
        return card

    def next_turn(self):
        self.turn += 1
        self.current_player = self.players[self.turn % 2]

    def ask_player_hit_or_stand(self):
        answer = inquirer.prompt(self.player_choice)

        return answer['player_choice'] == "Hit"

    def full_status(self):
        self.dealer_status()
        self.player_status()
        print('\n')

    def dealer_status(self):
        print('{:*^30}'.format(" Dealer's Hand "))
        self.dealer.show_hand(self.turn == 1)  # Dealer has hole card at beginning of game

    def player_status(self):
        print('{:*^30}'.format(" Player Hand "))
        self.player.show_hand()

    def results(self):
        print('{:-^30}'.format(" Game Results "))
        self.full_status()

        if self.dealer.hand_total() == self.player.hand_total():
            if len(self.dealer.hand.cards) <= len(self.player.hand.cards):
                print("Dealer wins! Better luck next time.")
            else:
                print("You win!")
        elif self.dealer.hand_total() > self.player.hand_total():
            print("Dealer wins! Better luck next time.")
        else:
            if self.player.hand_total() == 21:
                print('Winner winner chicken dinner!!!')
            else:
                print("You win!")

    def dealer_bust(self):
        self.dealer_status()
        print('Dealer busts! You win!')

    def player_bust(self):
        self.player_status()
        print('You bust! Better luck next time.')


def main():
    game = BlackJack()
    game.new_game()
    dealer_stand = False
    player_stand = False

    while True:
        if game.current_player.type == 'dealer' and not dealer_stand:
            print("Dealer's turn.")
            pause(1.5)

            if game.dealer.hand_total() < 17:
                card = game.hit()
                print("Dealer hits: {val}".format(val=card.value))
                pause()

                if game.dealer.hand_total() > 21:
                    game.dealer_bust()
                    break
                else:
                    game.dealer_status()
                    print('\n')
                    pause()
            else:
                print("Dealer stands.\n")
                dealer_stand = True
                pause(.8)

        elif not player_stand:
            print("Player's turn.")
            pause(.8)

            if game.ask_player_hit_or_stand():
                card = game.hit()
                print("Player hits: {val}".format(val=card.value))
                pause()

                if game.current_player.hand_total() > 21:
                    game.player_bust()
                    break
                else:
                    game.player_status()
                    print('\n')
                    pause()
            else:
                print("Player stands.\n")
                player_stand = True
                pause(.8)

        if player_stand and dealer_stand:
            game.results()
            break

        game.next_turn()


if __name__ == '__main__':
    main()
