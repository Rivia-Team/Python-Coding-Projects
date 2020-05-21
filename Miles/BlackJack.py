import random


class Card:
    def __init__(self, value):
        self.value = value

# Format to show all cards and gives numbers over 10 facevalue
    def show(self):
        if self.value == 11:
            self.value = "J"
        if self.value == 12:
            self.value = "Q"
        if self.value == 13:
            self.value = "K"
        if self.value == 14:
            self.value = "A"
        print("{}".format(self.value))
        return "{}".format(self.value)


class Deck:
    def __init__(self):
        self.cards = []
        self.dealer_hand = []
        self.player_hand = []
        self.shuffle()
        self.show()
        self.deal_cards()

# Creates a deck of 52 cards with all suites
    def build(self):
        for s in ["Spades", "Diamonds", "Hearts", "Clubs"]:
            for v in range(2, 15):
                self.cards.append(Card(v))

    def show(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        count = 0
        while count < 6:
            self.build()
            count += 1
        random.shuffle(self.cards)

    def deal_cards(self):
        count = 0
        while count < 2:
            self.player_hand.append(self.cards.pop())
            self.dealer_hand.append(self.cards.pop())
            count += 1
        print("{} {}".format(self.dealer_hand, self.player_hand))
        return "{} {}".format(self.dealer_hand, self.player_hand)


class Player(Deck):
    def __init__(self):
        super().__init__()
        print(self.player_hand)

    def hit(self):
        print(self.player_hand)
        self.player_hand.append(self.cards.pop())


def main():
    print('Welcome to Blackjack, Get closer to 21 to beat the dealer! ')


if __name__ == '__main__':
    main()
