import unittest

from game.models import Card, Deck, Hand, Player


class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card(rank=14, suit=3)
        self.assertEqual(card.rank, 14)
        self.assertEqual(card.suit, 3)

    def test_card_repr_ace(self):
        self.assertEqual(repr(Card(14, 3)), "♠A")

    def test_card_repr_three(self):
        self.assertEqual(repr(Card(3, 0)), "♣3")

    def test_card_compare_suit(self):
        self.assertGreater(Card(14, 3), Card(14, 2))

    def test_card_compare_rank(self):
        self.assertGreater(Card(15, 0), Card(14, 3))

    def test_card_sort_key(self):
        self.assertEqual(Card(14, 3).to_sort_key(), (14, 3))


class TestDeck(unittest.TestCase):
    def test_deck_has_52_cards(self):
        self.assertEqual(len(Deck().cards), 52)

    def test_deck_all_unique(self):
        deck = Deck()
        self.assertEqual(len(set(deck.cards)), 52)

    def test_deal_5_cards(self):
        deck = Deck()
        dealt = deck.deal(5)
        self.assertEqual(len(dealt), 5)
        self.assertEqual(len(deck.cards), 47)

    def test_deal_exceed(self):
        deck = Deck()
        dealt = deck.deal(60)
        self.assertEqual(len(dealt), 52)
        self.assertEqual(len(deck.cards), 0)


class TestHand(unittest.TestCase):
    def test_hand_sort_desc(self):
        hand = Hand([Card(3, 0), Card(14, 3), Card(3, 3), Card(13, 2)])
        hand.sort_desc()
        self.assertEqual(hand, [Card(14, 3), Card(13, 2), Card(3, 3), Card(3, 0)])

    def test_hand_find_3_clubs(self):
        hand = Hand([Card(14, 3), Card(3, 0), Card(3, 1)])
        self.assertEqual(hand.find_3_clubs(), Card(3, 0))

    def test_hand_find_3_clubs_none(self):
        hand = Hand([Card(14, 3), Card(3, 1)])
        self.assertIsNone(hand.find_3_clubs())

    def test_hand_remove_not_found(self):
        hand = Hand([Card(14, 3)])
        hand.remove([Card(3, 0)])
        self.assertEqual(len(hand), 1)


class TestPlayer(unittest.TestCase):
    def test_player_ai(self):
        player = Player("AI_1", True)
        self.assertTrue(player.is_ai)

    def test_player_take_and_play(self):
        player = Player("P1")
        cards = [Card(14, 3), Card(3, 0)]
        player.take_cards(cards)
        played = player.play_cards([Card(3, 0)])
        self.assertEqual(played, [Card(3, 0)])
        self.assertEqual(len(player.hand), 1)


if __name__ == "__main__":
    unittest.main()
