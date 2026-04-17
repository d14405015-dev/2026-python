import unittest

from game.classifier import CardType, HandClassifier
from game.models import Card


class TestClassifier(unittest.TestCase):
    def test_cardtype_values(self):
        self.assertEqual(CardType.SINGLE, 1)
        self.assertEqual(CardType.STRAIGHT_FLUSH, 8)

    def test_classify_single(self):
        self.assertEqual(HandClassifier.classify([Card(14, 3)]), (CardType.SINGLE, 14, 3))

    def test_classify_pair(self):
        self.assertEqual(HandClassifier.classify([Card(14, 3), Card(14, 2)]), (CardType.PAIR, 14, 3))

    def test_classify_triple(self):
        self.assertEqual(
            HandClassifier.classify([Card(14, 3), Card(14, 2), Card(14, 1)]),
            (CardType.TRIPLE, 14, 3),
        )

    def test_classify_straight(self):
        cards = [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0)]
        self.assertEqual(HandClassifier.classify(cards), (CardType.STRAIGHT, 7, 0))

    def test_classify_straight_ace_low(self):
        cards = [Card(14, 0), Card(15, 1), Card(3, 2), Card(4, 3), Card(5, 0)]
        self.assertEqual(HandClassifier.classify(cards), (CardType.STRAIGHT, 5, 0))

    def test_classify_flush_not_allowed(self):
        cards = [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0)]
        self.assertIsNone(HandClassifier.classify(cards))

    def test_classify_full_house(self):
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(15, 0), Card(15, 1)]
        self.assertEqual(HandClassifier.classify(cards), (CardType.FULL_HOUSE, 14, 0))

    def test_classify_four_of_a_kind(self):
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(14, 0), Card(3, 1)]
        self.assertEqual(HandClassifier.classify(cards), (CardType.FOUR_OF_A_KIND, 14, 0))

    def test_classify_straight_flush(self):
        cards = [Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0), Card(7, 0)]
        self.assertEqual(HandClassifier.classify(cards), (CardType.STRAIGHT_FLUSH, 7, 0))

    def test_compare(self):
        self.assertEqual(HandClassifier.compare([Card(14, 3)], [Card(13, 3)]), 1)
        self.assertEqual(HandClassifier.compare([Card(14, 3)], [Card(14, 2)]), 1)

    def test_compare_pair_same_rank_by_suit(self):
        spade_pair = [Card(7, 3), Card(7, 1)]
        heart_pair = [Card(7, 2), Card(7, 0)]
        self.assertEqual(HandClassifier.compare(spade_pair, heart_pair), 1)

    def test_compare_triple_same_rank_by_suit(self):
        high_triple = [Card(9, 3), Card(9, 2), Card(9, 1)]
        low_triple = [Card(9, 2), Card(9, 1), Card(9, 0)]
        self.assertEqual(HandClassifier.compare(high_triple, low_triple), 1)

    def test_can_play_first(self):
        self.assertTrue(HandClassifier.can_play(None, [Card(3, 0)]))
        self.assertFalse(HandClassifier.can_play(None, [Card(14, 3)]))


if __name__ == "__main__":
    unittest.main()
