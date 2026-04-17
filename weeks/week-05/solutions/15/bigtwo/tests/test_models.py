import unittest

from game.models import Card, Deck, Hand, Player


class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card(14, 3)
        self.assertEqual(card.rank, 14)
        self.assertEqual(card.suit, 3)

    def test_card_repr(self):
        self.assertEqual(repr(Card(14, 3)), "♠A")
        self.assertEqual(repr(Card(3, 0)), "♣3")

    def test_card_compare(self):
        self.assertGreater(Card(14, 3), Card(14, 2))
        self.assertGreater(Card(15, 0), Card(14, 3))

    def test_card_sort_key(self):
        self.assertEqual(Card(14, 3).to_sort_key(), (14, 3))


class TestDeck(unittest.TestCase):
    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_all_unique(self):
        deck = Deck()
        self.assertEqual(len(set(deck.cards)), 52)

    def test_deal(self):
        deck = Deck()
        cards = deck.deal(5)
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(deck.cards), 47)

    def test_deal_exceed(self):
        deck = Deck()
        cards = deck.deal(60)
        self.assertEqual(len(cards), 52)
        self.assertEqual(len(deck.cards), 0)


class TestHand(unittest.TestCase):
    def test_hand_sort_desc(self):
        hand = Hand([Card(3, 0), Card(14, 3), Card(3, 3), Card(13, 2)])
        hand.sort_desc()
        self.assertEqual(hand, [Card(14, 3), Card(13, 2), Card(3, 0), Card(3, 3)])

    def test_find_3_clubs(self):
        hand = Hand([Card(14, 3), Card(3, 0)])
        self.assertEqual(hand.find_3_clubs(), Card(3, 0))

    def test_remove(self):
        hand = Hand([Card(14, 3), Card(3, 0), Card(13, 2)])
        hand.remove([Card(3, 0), Card(7, 1)])
        self.assertEqual(len(hand), 2)


class TestPlayer(unittest.TestCase):
    def test_player_take_and_play(self):
        player = Player("P1")
        cards = [Card(14, 3), Card(3, 0)]
        player.take_cards(cards)
        self.assertEqual(len(player.hand), 2)
        played = player.play_cards([Card(3, 0)])
        self.assertEqual(played, [Card(3, 0)])
        self.assertEqual(len(player.hand), 1)


if __name__ == "__main__":
    unittest.main()
