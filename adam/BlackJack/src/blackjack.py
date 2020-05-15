"""K 18

 task 18 - Write a program that plays the game BlackJack with a user. For this
    exercise you can use procedural or OOP programming styles. Research the rules
    of BlackJack to ensure your game is authentic.

Completed: AP -
"""

import random
import sys

def gen_cards():
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


suites = ["clubs", "hearts", "spades", "diamonds"]
cards = []
for suite in suites:
    for card in gen_cards():
        cards.append([suite,card])


def deal_card(deck: list) -> str:
    myrand = random.randint(0, len(deck)-1)
    mycard = deck.pop(myrand)
    print("CARD DEALT! ...Cards left: {}".format(len(deck)))
    return mycard


class Player:
    def __init__(self, name):
        self.name = name
        self.role = "NON-DEALER"
        self.won = 0
        self.lost = 0
        self.cards = []
        self.processed_cards = []
        self.total = 0
        self.done = False
        print("My name is {} and I have these cards {}. I am a {}.".format(self.name, self.cards, self.role))

    def check_hand(self) -> str:
        """ See if the player can hit for another card or not.  """
        # [ "diamnond","J" ]  ["diamond","j",11]
        for card in range(0,len(self.cards)):
            if self.cards[card][1] not in self.processed_cards:
                #print(f"Trying to add {self.cards[card][1]}")
                if isinstance(self.cards[card][1], int):
                    self.total += self.cards[card][1]
                elif self.cards[card][1] in ["J", "Q", "K"]:
                    self.total += 10
                elif self.cards[card][1] == "A":
                    myval = input("Would you like this to count as a 1 or 11?")
                    self.total += int(myval)
                self.processed_cards.append(self.cards[card][1])
        print("Total for {} is now: {} with these cards: \n".format(self.name, self.total, self.processed_cards))
        if self.role == "NON-DEALER":
            if self.total < 21:
                return "READY"
            elif self.total == 21:
                self.won = 1
                print("{} WON!!!!".format(self.name))
                sys.exit(0)
            else:
                self.lost = 1
                return "DONE"
        else:
            if self.total < 17:
                print("Dealer will get a new card...")
                return "READY"
            elif self.total > 20:
                self.lost = 1
                print("DEALER LOST")
            else:
                print("Dealer will not deal any more cards.")
                return "DONE"

    def request_hit_card(self):
        """ Prompt player to hit for a new card or continue play. """
        #print("I am {}. Checking hand for a {}".format(self.name, self.role))
        if self.role == "NON-DEALER" and self.done == False:
            if self.check_hand() == "READY":
                getcard = input("Would you like to HIT for a new card?")
                if getcard.lower() in ["yes", "y"]:
                    self.cards.append(deal_card(cards))
                    self.check_hand()
                    print(self.total)
                else:
                    self.done = True
                    return self.done
            else:
                self.lost = 1
                print("You lost!")
        elif self.role == "DEALER":
            if self.check_hand() == "READY":
                print("DEALER ADDING CARD?")
                self.cards.append(deal_card(cards))
                self.check_hand()
                print(self.total)
        else:
            return self.done


class Dealer(Player):
    def __init__(self, myname):
        super().__init__(myname)
        self.role = "DEALER"
        print(f"I am the {self.role}")

    def deal_cards(self, myplayers):
        """ Deal a card for each player. """
        for player in myplayers:
            player.cards.append(deal_card(cards))
        self.cards.append(deal_card(cards))
        print("Dealer has this card {}.".format(self.cards))

    '''def check_hand(self):
        """ Check whether I can get another card or not. """
        super().check_hand()'''


class Game:

    def __init__(self):
        self.players = []
        self.totalplayers = len(self.players)
        self.losers = []
        self.winner = []
        self.dealer = Dealer("Mr. Carlos Dealer (^_^)")
        self.register_game()
        self.the_play()

    def register_game(self) -> object:
        """ Setup a new game and request amount of players. """
        self.newplayers = True
        print("*** Welcome to Blackjack! ***")
        while self.newplayers == True:
            myplayer = input("Enter a name to register a new player or type in PLAY to begin the game.\n : ")
            if myplayer.lower() == "play":
                self.newplayers = False
            else:
                self.players.append(Player(myplayer))
        return self.players

    def check_game_status(self) -> bool:
        """ Identify if there is a winner. """
        for player in self.players:
            if player.lost == 1:
                self.losers.append(player)
                print("Added a player who lost. :( \n")
                print("Losing Players: {}".format(self.losers))
                print("Original Players: {}".format(self.players))
        for player in self.players:
            if player.won == 1:
                print("The player {} WON!".format(player.name))
                sys.exit(0)
            elif len(self.losers) < len(self.players):
                return True
            else:
                return False

    def end_game(self):
        for player in self.players:
            if self.dealer.total < player.total < 22:
                player.won = 1
                self.check_game_status()

    def get_play(self):
        """ Run a play around the table. """
        for player in self.players:
            if player.done != True:
                player.request_hit_card()
            else:
                self.end_game()
        self.dealer.request_hit_card()

    def the_play(self):
        """ Manage the workflow for the game. """
        self.dealer.deal_cards(self.players)
        while self.check_game_status():
            self.get_play()
            self.dealer.check_hand()

def main():
    mygame = Game()


if __name__ == "__main__":
    main()

