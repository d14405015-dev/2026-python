"""Phase 3 牌型搜尋的單元測試。

這份測試依照 game_design/p3-test.md 與 p3-dev.md 撰寫，
目標是驗證 HandFinder 是否能正確找出可用牌型與合法出牌。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


def _prepare_import_path() -> None:
    """自動補上專案根目錄，讓 game 套件可以被匯入。"""

    current = Path(__file__).resolve().parent

    for candidate in [current, *current.parents]:
        if (candidate / "game").is_dir():
            sys.path.insert(0, str(candidate))
            return

        if (candidate / "bigtwo" / "game").is_dir():
            sys.path.insert(0, str(candidate / "bigtwo"))
            return


_prepare_import_path()

from game.classifier import CardType, HandClassifier
from game.finder import HandFinder
from game.models import Card, Hand


def make_card(rank: int, suit: int) -> Card:
    """建立測試用卡牌。"""

    return Card(rank, suit)


def normalize_play(play: list[Card]) -> tuple[tuple[int, int], ...]:
    """把一手牌轉成可比較的排序 key。"""

    return tuple(sorted((c.rank, c.suit) for c in play))


class TestFindSingles(unittest.TestCase):
    """測試單張搜尋。"""

    def test_find_singles(self) -> None:
        hand = Hand([make_card(14, 3), make_card(13, 2), make_card(3, 0)])
        plays = HandFinder.find_singles(hand)

        self.assertEqual(len(plays), 3)
        self.assertTrue(all(len(p) == 1 for p in plays))

    def test_find_singles_empty(self) -> None:
        hand = Hand([])
        plays = HandFinder.find_singles(hand)
        self.assertEqual(len(plays), 0)


class TestFindPairs(unittest.TestCase):
    """測試對子搜尋。"""

    def test_find_pairs_one(self) -> None:
        hand = Hand([make_card(14, 3), make_card(14, 2), make_card(3, 0)])
        plays = HandFinder.find_pairs(hand)

        self.assertEqual(len(plays), 1)
        self.assertEqual(HandClassifier.classify(plays[0]), (CardType.PAIR, 14, 0))

    def test_find_pairs_two(self) -> None:
        hand = Hand(
            [
                make_card(14, 3),
                make_card(14, 2),
                make_card(13, 3),
                make_card(13, 0),
            ]
        )
        plays = HandFinder.find_pairs(hand)

        self.assertEqual(len(plays), 2)
        self.assertTrue(all(HandClassifier.classify(p)[0] == CardType.PAIR for p in plays))

    def test_find_pairs_none(self) -> None:
        hand = Hand([make_card(14, 3), make_card(13, 2), make_card(3, 0)])
        plays = HandFinder.find_pairs(hand)
        self.assertEqual(len(plays), 0)


class TestFindTriples(unittest.TestCase):
    """測試三條搜尋。"""

    def test_find_triples_one(self) -> None:
        hand = Hand([make_card(14, 3), make_card(14, 2), make_card(14, 1), make_card(3, 0)])
        plays = HandFinder.find_triples(hand)

        self.assertEqual(len(plays), 1)
        self.assertEqual(HandClassifier.classify(plays[0]), (CardType.TRIPLE, 14, 0))

    def test_find_triples_with_extra(self) -> None:
        hand = Hand(
            [
                make_card(14, 3),
                make_card(14, 2),
                make_card(14, 1),
                make_card(13, 3),
                make_card(13, 2),
            ]
        )
        plays = HandFinder.find_triples(hand)

        self.assertEqual(len(plays), 1)
        self.assertEqual(HandClassifier.classify(plays[0]), (CardType.TRIPLE, 14, 0))


class TestFindFives(unittest.TestCase):
    """測試五張牌型搜尋。"""

    def test_find_straight(self) -> None:
        hand = Hand([make_card(3, 0), make_card(4, 1), make_card(5, 2), make_card(6, 3), make_card(7, 0)])
        plays = HandFinder.find_fives(hand)
        self.assertTrue(any(HandClassifier.classify(p)[0] == CardType.STRAIGHT for p in plays))

    def test_find_flush(self) -> None:
        hand = Hand([make_card(3, 0), make_card(5, 0), make_card(7, 0), make_card(9, 0), make_card(11, 0)])
        plays = HandFinder.find_fives(hand)
        self.assertTrue(any(HandClassifier.classify(p)[0] == CardType.FLUSH for p in plays))

    def test_find_full_house(self) -> None:
        hand = Hand([make_card(14, 3), make_card(14, 2), make_card(14, 1), make_card(13, 3), make_card(13, 2)])
        plays = HandFinder.find_fives(hand)
        self.assertTrue(any(HandClassifier.classify(p)[0] == CardType.FULL_HOUSE for p in plays))

    def test_find_four_of_a_kind(self) -> None:
        hand = Hand(
            [
                make_card(14, 3),
                make_card(14, 2),
                make_card(14, 1),
                make_card(14, 0),
                make_card(3, 1),
            ]
        )
        plays = HandFinder.find_fives(hand)
        self.assertTrue(any(HandClassifier.classify(p)[0] == CardType.FOUR_OF_A_KIND for p in plays))

    def test_find_straight_flush(self) -> None:
        hand = Hand([make_card(3, 0), make_card(4, 0), make_card(5, 0), make_card(6, 0), make_card(7, 0)])
        plays = HandFinder.find_fives(hand)
        self.assertTrue(any(HandClassifier.classify(p)[0] == CardType.STRAIGHT_FLUSH for p in plays))


class TestGetAllValidPlays(unittest.TestCase):
    """測試依照上家牌型過濾合法出牌。"""

    def test_first_turn(self) -> None:
        hand = Hand([make_card(3, 0), make_card(14, 3), make_card(13, 2)])
        plays = HandFinder.get_all_valid_plays(hand, None)

        self.assertEqual(plays, [[make_card(3, 0)]])

    def test_with_last_single(self) -> None:
        hand = Hand([make_card(6, 3), make_card(7, 0), make_card(14, 2), make_card(10, 1), make_card(10, 3)])
        last_play = [make_card(5, 1)]
        plays = HandFinder.get_all_valid_plays(hand, last_play)

        self.assertTrue(all(len(p) == 1 for p in plays))
        self.assertTrue(all(HandClassifier.can_play(last_play, p) for p in plays))

    def test_with_last_pair(self) -> None:
        hand = Hand([make_card(6, 3), make_card(6, 2), make_card(7, 1), make_card(7, 0), make_card(14, 2)])
        last_play = [make_card(5, 1), make_card(5, 0)]
        plays = HandFinder.get_all_valid_plays(hand, last_play)

        self.assertTrue(all(len(p) == 2 for p in plays))
        self.assertTrue(all(HandClassifier.can_play(last_play, p) for p in plays))

    def test_no_valid(self) -> None:
        hand = Hand([make_card(3, 0), make_card(4, 1), make_card(6, 2)])
        last_play = [make_card(14, 3)]
        plays = HandFinder.get_all_valid_plays(hand, last_play)
        self.assertEqual(plays, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)