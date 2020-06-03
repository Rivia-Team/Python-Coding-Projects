"""
TASK 18

 task 18 - Write a program that plays the game BlackJack with a user. For this
    exercise you can use procedural or OOP programming styles. Research the rules
    of BlackJack to ensure your game is authentic.

Completed: AP -
"""

import random


class Deck:

    """
    Provides a Class for holding a standard 52 card deck in a list of lists format.
    """

    suites = ["clubs", "hearts", "spades", "diamonds"]
    cards = []

    def __init__(self):
        """ Based off the suites being used populate a card deck. """
        for suite in self.suites:
            for card in self.gen_cards():
                self.cards.append([suite, card])

    def gen_cards(self):
        """ Generator to build a deck. """
        c = 1
        spec = {
            "11":"J",
            "12":"Q",
            "13":"K",
            "1": "A"
        }
        while True and c != 14:
            if c < 11 and c != 1:
                yield c
                c += 1
            else:
                yield spec[str(c)]
                c +=1

    def deal_card(self) -> str:
        """ From an established Deck this will return a card in list format. """
        myrand = random.randint(0, len(self.cards)-1)
        mycard = self.cards.pop(myrand)
        print("THIS CARD DEALT: {}".format(mycard))
        return mycard


class Player:

    """
    Contains information related to a player and methods to manipulate player owned variables.
    """

    def __init__(self, name, deck):
        self.cash = 50
        self.deck = deck
        self.name = name
        self.role = "NON-DEALER"
        self.won = 0
        self.lost = 0
        self.cards = []
        self.processed_cards = []
        self.total = 0
        self.done = False

    def check_hand(self) -> str:
        """ See if the player can hit for another card or not.  """
        for card in range(0,len(self.cards)):
            if self.cards[card][1] not in self.processed_cards:
                if isinstance(self.cards[card][1], int):
                    self.total += self.cards[card][1]
                elif self.cards[card][1] in ["J", "Q", "K"]:
                    self.total += 10
                elif self.cards[card][1] == "A":
                    if self.role == "DEALER":
                        myval = "11"
                        self.total += int(myval)
                    else:
                        myval = input("Would you like this to count as a 1 or 11?")
                        self.total += int(myval)
                self.processed_cards.append(self.cards[card][1])
            '''if self.role == "NON-DEALER":
                print("Total for {} is now: {}: \n".format(self.name, self.total))'''
        if self.role == "NON-DEALER":
            if self.total < 21:
                return "READY"
            elif self.total == 21:
                self.won = 1
                #print("{} WON!!!!".format(self.name))
                #sys.exit(0)
            else:
                self.lost = 1
                return "DONE"
        else:
            if self.total < 17:
                #print("Dealer pulling a new card.")
                return "READY"
            elif self.total > 20:
                self.done = True
                self.lost = 1
                print("DEALER LOST")
            else:
                print("Dealer will not deal any more cards.")
                return "DONE"

    def request_hit_card(self):
        """ Prompt player to hit for a new card or continue play. """
        if self.role == "NON-DEALER" and self.done == False:
            if self.lost == 0:
                getcard = input("Would you like to HIT for a new card?")
                if getcard.lower() in ["yes", "y"]:
                    self.cards.append(self.deck.deal_card())
                else:
                    self.done = True
                return self.done
            else:
                self.done = True
                self.lost = 1
        elif self.role == "DEALER":
            #if self.check_hand() == "READY":
                #self.cards.append(self.deck.deal_card())
            self.check_hand()
            print("MYTOTAL IS {}".format(self.total))
        else:
            return self.done


class Dealer(Player):

    """
    A type of player that deals cards to other players.
    """

    def __init__(self, myname, deck):
        """ Calls on Parent class to provide most functionality. """
        super().__init__(myname, deck)
        self.role = "DEALER"
        self.deck = deck

    def deal_cards(self, myplayers):
        """ Deal a card for each player. """
        for player in myplayers:
            player.cards.append(self.deck.deal_card())
        self.draw_card()
        print("Dealer has this cards {}.".format(self.cards))

    def draw_card(self):
        """ Deals a card for the Dealer. """
        self.cards.append(self.deck.deal_card())


class Game:

    """
    The core logic to run the game and take action on Players.  Decides who wins, controls the tempo.
    """

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.totalplayers = len(self.players)
        self.losers = []
        self.winner = []
        self.dealer = Dealer("Mr. Dealer (^_^)", self.deck)

    def register_game(self) -> object:
        """ Setup a new game and request amount of players. """
        self.newplayers = True
        print("*** Welcome to Blackjack! ***")
        while self.newplayers == True:
            myplayer = input("Enter a new player name or type in PLAY to begin the game: ")
            if myplayer.lower() == "play":
                self.newplayers = False
            else:
                self.players.append(Player(myplayer, self.deck))
        return self.players

    def check_game_status(self) -> bool:
        """ Identify if there is a winner. """
        for player in self.players:
            if player.lost == 1:
                self.losers.append(player)
        for player in self.players:
            if player.won == 1:
                print("The player {} WON!".format(player.name))
            elif len(self.losers) < len(self.players):
                return True
            else:
                print("The player {} LOST!".format(player.name))
            return False

    def end_game(self):
        """ Check if a player has a higher total than the dealer.  """
        for player in self.players:
            if player.total > self.dealer.total:
                player.won = 1
                #self.check_game_status()
            else:
                player.lost = 1

    def get_play(self):
        """ Run a play around the table. """
        for player in self.players:
            if player.done != True:
                player.request_hit_card()
                player.check_hand()
                print("Player {} has this total: {}\n".format(player.name, player.total))
                self.dealer.check_hand()
                if player.done != True:
                    self.dealer.draw_card()
                    self.dealer.check_hand()
                    print("Dealer has this total: {}\n".format(self.dealer.total))
            if player.done == True:
                print("Ending game...")
                self.end_game()

    def the_play(self):
        """ Manage the workflow for the game. """
        self.dealer.deal_cards(self.players)
        while self.check_game_status():
            self.get_play()
            if self.dealer.lost == 1:
                self.end_game()


def main():
    mygame = Game()
    mygame.register_game()
    mygame.the_play()


if __name__ == "__main__":
    main()

