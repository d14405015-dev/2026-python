import unittest

from game.finder import HandFinder
from game.models import Card, Hand


class TestFinder(unittest.TestCase):
    def test_find_singles(self):
        hand = Hand([Card(14, 3), Card(13, 2), Card(3, 0)])
        singles = HandFinder.find_singles(hand)
        self.assertEqual(len(singles), 3)

    def test_find_pairs(self):
        hand = Hand([Card(14, 3), Card(14, 2), Card(3, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 1)

    def test_find_triples(self):
        hand = Hand([Card(14, 3), Card(14, 2), Card(14, 1), Card(3, 0)])
        triples = HandFinder.find_triples(hand)
        self.assertEqual(len(triples), 1)

    def test_find_fives_straight(self):
        hand = Hand([Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0), Card(9, 0)])
        fives = HandFinder.find_fives(hand)
        self.assertGreaterEqual(len(fives), 1)

    def test_first_turn(self):
        hand = Hand([Card(3, 0), Card(14, 3)])
        plays = HandFinder.get_all_valid_plays(hand, None)
        self.assertEqual(plays, [[Card(3, 0)]])

    def test_with_last_single(self):
        hand = Hand([Card(5, 0), Card(6, 0), Card(7, 0)])
        plays = HandFinder.get_all_valid_plays(hand, [Card(5, 0)])
        self.assertEqual(plays, [[Card(6, 0)], [Card(7, 0)]])


if __name__ == "__main__":
    unittest.main()
