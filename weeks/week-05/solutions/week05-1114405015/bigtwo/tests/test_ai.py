import unittest

from game.ai import AIStrategy
from game.models import Card, Hand


class TestAI(unittest.TestCase):
    def test_score_single(self):
        hand = Hand([Card(14, 3), Card(3, 0), Card(5, 1), Card(6, 2)])
        score = AIStrategy.score_play([Card(14, 3)], hand)
        self.assertEqual(score, 745.0)

    def test_score_pair_higher(self):
        hand = Hand([Card(14, 3), Card(14, 2), Card(3, 0), Card(4, 0)])
        single = AIStrategy.score_play([Card(14, 3)], hand)
        pair = AIStrategy.score_play([Card(14, 3), Card(14, 2)], hand)
        self.assertGreater(pair, single)

    def test_near_empty_bonus(self):
        hand = Hand([Card(14, 3), Card(3, 0)])
        score = AIStrategy.score_play([Card(14, 3)], hand)
        self.assertGreater(score, 10000)

    def test_select_best(self):
        hand = Hand([Card(14, 3), Card(14, 2), Card(3, 0)])
        valid = [[Card(14, 3)], [Card(14, 3), Card(14, 2)]]
        best = AIStrategy.select_best(valid, hand)
        self.assertEqual(best, [Card(14, 3), Card(14, 2)])

    def test_select_first_turn(self):
        hand = Hand([Card(3, 0), Card(14, 3)])
        valid = [[Card(14, 3)], [Card(3, 0)]]
        best = AIStrategy.select_best(valid, hand, is_first=True)
        self.assertEqual(best, [Card(3, 0)])


if __name__ == "__main__":
    unittest.main()
