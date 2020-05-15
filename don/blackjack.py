"""
Author: Don Drummond
Description: A command line game of Blackjack
Date: 12 May 2020
todos:
- implement multiple players
- implement multiple decks
- implement exit
- possible refactoring- make a superclass to handle duplicated code from house/player class
- handles any win with 21 as a blackjack paying 1.5, fix so only initial draw
- game will break if cards run out of deck, fix this
"""
# import sys
import random

# Global values for each card
# Ace is treated as 11 as when it converts to 1 is
# handled in another area
DECK_VALUES = {
    'Ace of Hearts': 11, 'Ace of Diamonds': 11, 'Ace of Spades': 11, 'Ace of Clubs': 11,
    'King of Hearts': 10, 'King of Diamonds': 10, 'King of Spades': 10, 'King of Clubs': 10,
    'Queen of Hearts': 10, 'Queen of Diamonds': 10, 'Queen of Spades': 10, 'Queen of Clubs': 10,
    'Jack of Hearts': 10, 'Jack of Diamonds': 10, 'Jack of Spades': 10, 'Jack of Clubs': 10,
    '10 of Hearts': 10, '10 of Diamonds': 10, '10 of Spades': 10, '10 of Clubs': 10,
    '9 of Hearts': 9, '9 of Diamonds': 9, '9 of Spades': 9, '9 of Clubs': 9,
    '8 of Hearts': 8, '8 of Diamonds': 8, '8 of Spades': 8, '8 of Clubs': 8,
    '7 of Hearts': 7, '7 of Diamonds': 7, '7 of Spades': 7, '7 of Clubs': 7,
    '6 of Hearts': 6, '6 of Diamonds': 6, '6 of Spades': 6, '6 of Clubs': 6,
    '5 of Hearts': 5, '5 of Diamonds': 5, '5 of Spades': 5, '5 of Clubs': 5,
    '4 of Hearts': 4, '4 of Diamonds': 4, '4 of Spades': 4, '4 of Clubs': 4,
    '3 of Hearts': 3, '3 of Diamonds': 3, '3 of Spades': 3, '3 of Clubs': 3,
    '2 of Hearts': 2, '2 of Diamonds': 2, '2 of Spades': 2, '2 of Clubs': 2,
    '1 of Hearts': 1, '1 of Diamonds': 1, '1 of Spades': 1, '1 of Clubs': 1
}

# Create number of decks for the game
NUM_DECKS = 0


def generate_deck():
    """
    Function to create a random deck of cards
    :return: A list of 52 strings representing a deck of cards
    """
    deck = []
    cards = ["Ace", "King", "Queen", "Jack", "10", "9",
             "8", "7", "6", "5", "4", "3", "2", "1"]
    for card in cards:
        deck.append(card + " of Hearts")
        deck.append(card + " of Diamonds")
        deck.append(card + " of Spades")
        deck.append(card + " of Clubs")

    random.shuffle(deck)
    return deck


# Global deck variable
GAME_DECK = generate_deck()


class Player:
    def __init__(self):
        self._bank = 1000
        self._hand = []
        self._hand_value = 0
        self._bet = 0
        self._aces_not_one = 0

    def create_bet(self, amount):
        """
        Creates a player's bet for a round, it is reset at the end of the round
        :param amount: Amount a player bets
        :return: None
        """
        self._bet = amount

    def add_card(self):
        """
        Adds a card to a player's hand, additionally increments
        aces_not_one to show how many current Aces are in the hand
        that are equal to 11
        :return: None
        """
        new_card = deal_card(GAME_DECK)
        if DECK_VALUES[new_card] == 11:
            self._aces_not_one += 1
        self._hand.append(new_card)
        self._hand_value += DECK_VALUES[new_card]

    def display_hand(self):
        """
        Prints a player's hand and current hand value to them
        :return: None
        """
        print("Your hand is: ")
        for card in self._hand:
            print(card)
        print("Your hand value is: ")
        print(self.get_hand_total())

    def reset_hand(self):
        """
        Resets a player's hand, hand_value, and bet
        :return: None
        """
        self._hand = []
        self._hand_value = 0
        self._bet = 0
        self._aces_not_one = 0

    def update_bank(self, win_condition, amount):
        """
        Updates a player's bank based on if they won a hand or not
        :param win_condition: True if a player won a hand, False if a player lost a hand
        :param amount: Amount won, handles 1.5 payout for blackjack
        :return: None
        """
        if win_condition:
            self._bank += amount
        else:
            self._bank -= amount

    def convert_ace_to_one(self):
        """
        Reduces a player's hand by 10 to convert an ace from
        value 11 to value 1
        :return: None
        """
        self._hand_value -= 10
        self._aces_not_one -= 1

    def get_bank(self):
        """
        Getter for player's bank
        :return: Player's bank
        """
        return self._bank

    def get_aces(self):
        """
        Getter for Aces that are not one
        :return: Player's aces that are not one
        """
        return self._aces_not_one

    def get_hand_total(self):
        """
        Getter for hand total
        :return: Player's hand total
        """
        return self._hand_value

    def get_bet(self):
        """
        Getter for bet total
        :return: Player's current bet
        """
        return self._bet

    def wager(self):
        while True:
            player_wager = input("How much would you like to wager? ")
            try:
                player_wager = int(player_wager)
                if player_wager <= self._bank:
                    self._bet = player_wager
                    return True
                else:
                    print("You don't have enough coin..")
                    return False
            except:
                print("This isn't an positive integer, please enter a positive, whole number.")


class House:
    def __init__(self):
        self._hand = []
        self._hand_value = 0
        self._soft_hit = 17
        self._aces_not_one = 0

    def add_card(self):
        """
        Deals a card to the House's hand
        :return: None
        """
        new_card = deal_card(GAME_DECK)
        if DECK_VALUES[new_card] == 11:
            self._aces_not_one += 1
        self._hand.append(new_card)
        self._hand_value += DECK_VALUES[new_card]


    def display_hidden_hand(self):
        """
        Shows the 'face card' of the dealer
        :return: None
        """
        print("The dealer currently has " + self._hand[0] + " showing.")

    def get_hand_total(self):
        """
        Getter for hand total
        :return: Houses's hand total
        """
        return self._hand_value

    def convert_ace_to_one(self):
        """
        Reduces a player's hand by 10 to convert an ace from
        value 11 to value 1
        :return: None
        """
        self._hand_value -= 10
        self._aces_not_one -= 1

    def display_final_hand(self):
        """
        Prints Houses's final hand and current hand value to the user
        :return: None
        """
        print("House cards: ")
        for card in self._hand:
            print(card)
        print("House has: ")
        print(self.get_hand_total())

    def reset_hand(self):
        """
        Resets a player's hand, hand_value, and bet
        :return: None
        """
        self._hand = []
        self._hand_value = 0
        self._aces_not_one = 0

    def get_aces(self):
        """
        Getter for Aces that are not one
        :return: Player's aces that are not one
        """
        return self._aces_not_one


def welcome():
    """
    Intro to the user
    :return: None
    """
    print("Welcome to terminal Blackjack.")
    print("You start with 1000 coins, continue play until you run out of coins.")



def deal_card(deck):
    card = deck.pop()
    return card


def game_turn(player, house):
    """
    Game engine to play a turn
    :param player: Player Object
    :param house: House Object
    :return: None
    """
    print("Your current Bank is:")
    print(player.get_bank())
    if player.wager():
        # Generate House and Player starting cards
        house.add_card()
        player.add_card()
        house.add_card()
        player.add_card()
        while True:
            # Handle converting Aces from 11 to 1 in point value
            house.display_hidden_hand()
            player.display_hand()
            if player.get_hand_total() > 21:
                if player.get_aces() > 0:
                    player.convert_ace_to_one()
                else:
                    print("You busted!")
                    player.update_bank(False, player.get_bet())
                    player.reset_hand()
                    break
            elif player.get_hand_total() == 21:
                print("Winner Winner Chicken Dinner, you hit BLACKJACK!")
                player.update_bank(True, (player.get_bet() * 1.5))
                player.reset_hand()
                break

            response = input("Would you like to hit y/n? ")
            if response == "y":
                player.add_card()
            elif response == "n":
                while house.get_hand_total() < 17:
                    house.add_card()
                print("\n")
                house.display_final_hand()
                if house.get_hand_total() > 21:
                    if house.get_aces() > 0:
                        house.convert_ace_to_one()
                        if house.get_hand_total() > 21:
                            print("House Busted!")
                            print("Player win!")
                            player.update_bank(True, player.get_bet())
                            player.reset_hand()
                            house.reset_hand()
                            break
                    else:
                        print("House Busted!")
                        print("Player win!")
                        player.update_bank(True, player.get_bet())
                        player.reset_hand()
                        house.reset_hand()
                        break
                elif house.get_hand_total() < player.get_hand_total():
                    print("Player win!")
                    player.update_bank(True, player.get_bet())
                    player.reset_hand()
                    house.reset_hand()
                    break
                else:
                    player.update_bank(False, player.get_bet())
                    print("Player loss.")
                    player.reset_hand()
                    house.reset_hand()
                    break
            else:
                print("You didn't follow directions, no hit for you.")
                # handle House getting cards
                pass
    else:
        player.wager()

    """
    Code to handle split/double down.. 
    if GAME_DECK[player._hand[0]] == GAME_DECK[player._hand[1]]:
        response = input("Would you like to split y/n? ")
        if response != "y" or response != "n":
            print("Not valid response, I'll take that as a no.")
        elif response == "y":
    """


def main():
    welcome()
    new_deck = generate_deck()
    player = Player()
    house = House()
    # run the game loop
    while player.get_bank() > 0:
        game_turn(player, house)
    print("Game Over!")


if __name__ == "__main__":
    main()
