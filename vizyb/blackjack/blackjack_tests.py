from unittest import mock, TestCase, main
from vizyb.blackjack.blackjack import *


class Testing(TestCase):
    """ python3 -m unittest vizyb.blackjack.blackjack_tests.Testing """

    def setUp(self):
        self.gambler = Gambler()
        self.player = Player()
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.dealer = Dealer()
        self.dealer.deck.shuffle_deck()

    def test_card(self):
        card = Card("6", "Spades")
        self.assertEqual(card.numerical_value(), 6)
        card = Card("J", "Hearts")
        self.assertEqual(card.numerical_value(), 10)  # Assert faced values
        card = Card("1", "Jacks")
        self.assertEqual(card.numerical_value(), 1)

    def test_deck(self):
        self.assertEqual(len(self.deck.cards), 52)  # Assert full deck
        deck_cards_order = str(self.deck.cards)
        self.deck.shuffle_deck()
        self.assertNotEqual(deck_cards_order, str(self.deck.cards))  # Assert shuffle works
        self.deck.cards.pop()  # deal one card
        self.assertEqual(len(self.deck.cards), 51)
        self.deck.create_deck()  # pick up all the cards again
        self.assertEqual(len(self.deck.cards), 52)

    def test_player(self):
        self.assertEqual(self.player.hand, [])  # Assert hand not None
        card = self.deck.cards.pop()
        self.player.hand.append(card)  # Draw card
        self.assertIn(card, self.player.hand)  # Assert card in player hand
        self.player.clear_hand()  # Clear hand
        self.assertNotIn(card, self.player.hand)  # Assert card no longer in hand

    def test_dealer(self):
        self.assertEqual(len(self.dealer.deck.cards), 52)  # Assert init with full deck

    def test_gambler(self):
        self.assertEqual(self.gambler.money, 100)  # Assert start money
        # Mock interactive input module
        with mock.patch('inquirer.prompt', return_value={"bet_quantity": "50"}):
            self.assertEqual(self.gambler.make_a_bet(), 50)  # Make a bet

    def test_validate_bet(self):
        self.assertFalse(validate_bet(self.gambler, "1000"))
        self.assertTrue(validate_bet(self.gambler, "50"))
        self.assertFalse(validate_bet(self.gambler, "-1000"))
        self.assertFalse(validate_bet(self.gambler, "ABC"))
        self.gambler.money = 1500
        self.assertTrue(validate_bet(self.gambler, "1000"))

    def test_count_values(self):
        card1 = Card('J', 'Spades')
        self.player.hand.append(card1)  # Draw card
        card2 = Card('Q', 'Hearts')
        self.player.hand.append(card2)  # Draw card
        self.assertEqual(count_values(self.player), card1.numerical_value() + card2.numerical_value())
        self.player.clear_hand()
        card1 = Card('10', 'Spades')
        self.player.hand.append(card1)  # Draw card
        card2 = Card('1', 'Clubs')
        self.player.hand.append(card2)  # Draw card
        self.assertEqual(count_values(self.player), 21)

    def test_play_a_round(self):
        with mock.patch('inquirer.prompt', return_value={"draw": "Stay"}):
            play_a_round(self.dealer, self.gambler, 50)  # Player bets 50
            # We are stubbing prompt so player only drew 2 cards, therefore <= 21
            self.assertLessEqual(count_values(self.gambler), 21)
            if count_values(self.gambler) != 21:  # if the player didn't blackjack, dealer should be >17
                self.assertGreaterEqual(count_values(self.dealer), 17)
            # otherwise if the player lost, he should have forfeited his bet
            elif count_values(self.gambler) < count_values(self.dealer):
                self.assertEqual(self.gambler.money, 50)


if __name__ == '__main__':
    main()
