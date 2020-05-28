import blackjack
import pytest

# Initialize some instances of the classes to test methods.

mygame = blackjack.Game()
myplayer = blackjack.Player("Adam", mygame.deck)
mydealer = blackjack.Dealer("Dealer", mygame.deck)
mygame.players.append(myplayer)


def test_deck_size():
    """ Check that deck is populated with cards. """
    assert len(mygame.deck.cards) == 52


def test_deck_deal_card_type():
    """ Check if a card is returned of type list."""
    assert type(mygame.deck.deal_card()) == list


def test_deck_deal_card_value():
    """ Check that the dealed card does not exist in the deck. """
    assert mygame.deck.deal_card() not in mygame.deck.cards


def test_Player_role():
    """ Check that a player starts as a non-dealer."""
    assert myplayer.role == "NON-DEALER"


def test_Dealer_role():
    """ Check that a Dealer is properly identified. """
    assert mydealer.role == "DEALER"


def test_Player_check_win():
    """ Test that a player total of 21 triggers a WIN condition. """
    myplayer.total = 21
    myplayer.check_hand()
    assert myplayer.won == 1


def test_Player_check_loss():
    """ Test that a player total of 22 triggers a LOSS condition. """
    myplayer.total = 22
    myplayer.check_hand()
    assert myplayer.lost == 1


def test_Game_status():
    """ Check that the game ends if 21 is reached.  """
    myplayer.total = 21
    myplayer.check_hand()
    assert mygame.check_game_status() == True
