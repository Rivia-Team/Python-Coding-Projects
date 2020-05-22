import random
import configparser


class Card:
    def __init__(self, value, suite):
        self.value = value
        self.suite = suite

    def __str__(self):
        return 'CARD – value: ' + self.value


class Deck:
    def __init__(self):
        self.card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.card_suites = ['spade', 'clover', 'diamond', 'heart']
        self.cards = [Card(value, suite) for value in self.card_values for suite in self.card_suites]

    def shuffle(self):
        random.shuffle(self.cards)

    def card(self):
        while self.cards:
            yield self.cards.pop()

    def __str__(self):
        return str(self.__dict__)


class Hand:
    def __init__(self):
        self.cards = []
        self.high_card_values = {'J': 10, 'Q': 10, 'K': 10}

    def add_card(self, card):
        self.cards.append(card)

    def get_total(self):
        total = 0
        aces = 0

        for card in self.cards:
            if card.value in self.high_card_values:
                total += self.high_card_values[card.value]
            elif card.value == 'A':
                aces += 1
            else:
                total += int(card.value)

        # Requires refactoring – we must find all permutations of Ace value sums
        ace_values = [1*aces, 11*aces]
        final_totals = [i + total for i in ace_values if i + total <= 21]

        if not final_totals:
            return min(ace_values) + total
        else:
            return max(final_totals)
