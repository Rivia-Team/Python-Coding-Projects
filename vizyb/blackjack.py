import re
from random import shuffle
from typing import List

import inquirer


class Card:
    """ A standard playing card comprised of a value and suit """

    def __init__(self, value: str, suit: str):
        self.suit = suit
        self.value = value

    def numerical_value(self) -> int:
        """ Return an integer value for card """
        try:
            return int(self.value)
        except Exception:
            return 10

    def __repr__(self):
        val = self.value if self.value != 1 else 'A'
        return f"{val} of {self.suit}"


class Deck:
    """ A standard deck of 52 cards """

    cards = []

    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self) -> List[Card]:
        """ Populate an array of cards """
        suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
        values = list(range(1, 11)) + ['J', 'Q', 'K']  # range 1,11 = 10 cards
        cards = [Card(value, suit) for value in values for suit in suits]
        self.cards = cards
        return cards

    def shuffle_deck(self) -> List[Card]:
        """ Randomize order of deck """
        return shuffle(self.cards)


class Player:
    """ A player within the game """
    cards_value = 0

    def __init__(self, hand: List[Card] = None):
        self.hand = hand if hand is not None else []

    def clear_hand(self):
        self.hand = []
        self.cards_value = 0


class Dealer(Player):
    """ Dealer extends Player including a deck of cards """
    def __init__(self, deck: Deck = None):
        super().__init__()
        self.deck = deck if deck is not None else Deck()


class Gambler(Player):
    """ Gambler extends Player including money to bet """

    def __init__(self, money: int = 100):
        super().__init__()
        self.money = money

    def make_a_bet(self) -> int:
        """ Make a bet; continuously re-prompt if invalid value """

        while True:  # inquirer's built-in validator insufficient
            answer = inquirer.prompt([inquirer.Text('bet_quantity',
                                                    message="How much do you want to bet?")])
            if validate_bet(self, answer["bet_quantity"]):
                break
        return int(answer["bet_quantity"])


def validate_bet(player: Gambler, bet: str):
    """ Validate an incoming bet as a valid value """

    if not re.match("\d+", bet):
        print("We only accept cash here.")
        return False
    if int(bet) < 0 or int(bet) > player.money:
        print("You can only bet the money you have.")
        return False
    return True


def count_values(player: Player) -> int:
    """ Assign values to all the cards in a player's hand """

    total_value = 0
    aces = []
    for card in player.hand:
        card_value = card.numerical_value()
        if card_value != 1:
            total_value += card_value
        else:
            aces.append(card)
    for ace in aces:
        if len(aces) > 1:
            total_value += 1
            aces.pop(aces.index(ace))  # index actually doesn't matter here
        else:
            if total_value + 11 > 21:
                total_value += 1
            else:
                total_value += 11
    return total_value


def play_a_round(dealer, gambler, wagered_amount):
    """ Play a round of blackjack """

    gambler.hand.append(dealer.deck.cards.pop())
    dealer.hand.append(dealer.deck.cards.pop())
    gambler.hand.append(dealer.deck.cards.pop())
    gambler_value = count_values(gambler)
    print("Dealer: " + str(dealer.hand))
    while gambler_value < 21:  # Player draws
        print("Gambler: " + str(gambler.hand))
        answer = inquirer.prompt([inquirer.List('draw',
                                                message='Hit or Stay?',
                                                choices=['Hit', 'Stay'])])
        if answer["draw"] == "Hit":
            gambler.hand.append(dealer.deck.cards.pop())
        if answer["draw"] == "Stay" or count_values(gambler) > 21:
            break

    gambler_value = count_values(gambler)
    dealer_value = count_values(dealer)  # calculate whether to draw

    while dealer_value < 17 and gambler_value <= 21:  # Dealer draws
        dealer.hand.append(dealer.deck.cards.pop())
        dealer_value = count_values(dealer)  # recalculate
    print("Dealer: " + str(dealer.hand))
    print("Gambler: " + str(gambler.hand))
    print(f"gamblers_hand: {gambler_value}, dealers_hand: {dealer_value}")

    if dealer_value < gambler_value < 22 or dealer_value > 21 >= gambler_value:
        gambler.money += wagered_amount
        print(f"You won! You now have ${gambler.money}")
    elif gambler_value > 21 or gambler_value < dealer_value:
        gambler.money -= wagered_amount
        print(f"You lost. You now have ${gambler.money}")
    if gambler_value == dealer_value:
        print(f"No one wins. You still have ${gambler.money}")


def blackjack():
    """ Feeling lucky? """

    dealer = Dealer()
    gambler = Gambler()
    answer = {"response": "Yes"}
    while answer["response"] == "Yes":
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        print(f"Let's play Blackjack. You have ${gambler.money}.")

        dealer.deck.shuffle_deck()
        wagered_amount = gambler.make_a_bet()
        play_a_round(dealer, gambler, wagered_amount)

        # reset everything
        dealer.deck.create_deck()
        dealer.clear_hand()
        gambler.clear_hand()

        answer = inquirer.prompt([inquirer.List('response',
                                                message='Do you want to continue?',
                                                choices=['Yes', 'No'])])


if __name__ == "__main__":
    blackjack()
