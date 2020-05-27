import blackjack


def test_deck():
    mydeck = blackjack.Deck()
    assert len(mydeck.cards) == 52

def test_Player():
    mydeck = blackjack.Deck()
    myplayer = blackjack.Player("Adam", mydeck)
    assert 1 == 1