"""Phase 4 AI 策略的單元測試。

這份測試依照 game_design/p4-test.md 與 p4-dev.md 撰寫，
目標是驗證 AIStrategy 的評分與最佳出牌選擇。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


def _prepare_import_path() -> None:
    """自動補上專案根目錄，讓 game 套件可被匯入。"""

    current = Path(__file__).resolve().parent

    for candidate in [current, *current.parents]:
        if (candidate / "game").is_dir():
            sys.path.insert(0, str(candidate))
            return

        if (candidate / "bigtwo" / "game").is_dir():
            sys.path.insert(0, str(candidate / "bigtwo"))
            return


_prepare_import_path()

from game.ai import AIStrategy
from game.classifier import CardType, HandClassifier
from game.finder import HandFinder
from game.models import Card, Hand


def make_card(rank: int, suit: int) -> Card:
    """建立測試用卡牌。"""

    return Card(rank, suit)


class TestScorePlay(unittest.TestCase):
    """測試 AI 的出牌評分函數。"""

    def test_score_single(self) -> None:
        # 單張 ♠A，若手牌共 2 張，基礎分數應為 1*100 + 14*10。
        hand = Hand([make_card(14, 3), make_card(3, 0)])
        play = [make_card(14, 3)]
        score = AIStrategy.score_play(play, hand)
        self.assertGreaterEqual(score, 240)

    def test_score_pair_higher(self) -> None:
        # 對子評分應高於單張。
        hand = Hand([make_card(14, 3), make_card(14, 2), make_card(13, 1)])
        single = [make_card(13, 1)]
        pair = [make_card(14, 3), make_card(14, 2)]

        self.assertGreater(AIStrategy.score_play(pair, hand), AIStrategy.score_play(single, hand))

    def test_score_triple_higher(self) -> None:
        # 三條評分應高於對子。
        hand = Hand([make_card(14, 3), make_card(14, 2), make_card(14, 1), make_card(13, 0)])
        pair = [make_card(14, 3), make_card(14, 2)]
        triple = [make_card(14, 3), make_card(14, 2), make_card(14, 1)]

        self.assertGreater(AIStrategy.score_play(triple, hand), AIStrategy.score_play(pair, hand))

    def test_score_near_empty(self) -> None:
        # 出完後手牌剩 1 張，應有很高加分（> 10000）。
        hand = Hand([make_card(14, 3), make_card(13, 2)])
        play = [make_card(14, 3)]
        score = AIStrategy.score_play(play, hand)
        self.assertGreater(score, 10000)

    def test_score_low_cards(self) -> None:
        # 出完後手牌很少（<=3 張）時，應有額外加分（> 500）。
        hand = Hand([make_card(14, 3), make_card(13, 2), make_card(12, 1), make_card(3, 0)])
        play = [make_card(3, 0)]
        score = AIStrategy.score_play(play, hand)
        self.assertGreater(score, 500)

    def test_score_spade_bonus(self) -> None:
        # 含有黑桃的出牌，分數應高於同 rank 非黑桃出牌。
        hand = Hand([make_card(10, 3), make_card(10, 2)])
        spade_play = [make_card(10, 3)]
        non_spade_play = [make_card(10, 2)]

        self.assertGreater(
            AIStrategy.score_play(spade_play, hand),
            AIStrategy.score_play(non_spade_play, hand),
        )


class TestSelectBest(unittest.TestCase):
    """測試 AI 的最佳出牌選擇。"""

    def test_select_best(self) -> None:
        # 在合法選項中，應選擇分數較高者（例如對子優於單張）。
        hand = Hand([make_card(14, 3), make_card(14, 2), make_card(13, 1)])
        valid_plays = [[make_card(13, 1)], [make_card(14, 3), make_card(14, 2)]]

        best = AIStrategy.select_best(valid_plays, hand)
        self.assertEqual(best, [make_card(14, 3), make_card(14, 2)])

    def test_select_first_turn(self) -> None:
        # 第一回合只能選 3♣。
        hand = Hand([make_card(3, 0), make_card(14, 3), make_card(13, 2)])
        valid_plays = [[make_card(3, 0)], [make_card(14, 3)]]

        best = AIStrategy.select_best(valid_plays, hand, is_first=True)
        self.assertEqual(best, [make_card(3, 0)])

    def test_select_empty(self) -> None:
        # 沒有合法出牌時，應回傳 None。
        hand = Hand([make_card(14, 3)])
        best = AIStrategy.select_best([], hand)
        self.assertIsNone(best)


class TestAIStrategyFlow(unittest.TestCase):
    """測試 AI 在完整流程中的出牌傾向。"""

    def test_ai_always_plays(self) -> None:
        # 只要有合法牌可出，AI 就應該回傳其中一手。
        hand = Hand([make_card(6, 3), make_card(7, 1), make_card(3, 0)])
        last_play = [make_card(5, 2)]
        valid_plays = HandFinder.get_all_valid_plays(hand, last_play)

        self.assertTrue(len(valid_plays) > 0)
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertIsNotNone(best)

    def test_ai_prefers_high(self) -> None:
        # 若同牌型有高低牌可選，應偏好較高者。
        hand = Hand([make_card(6, 3), make_card(12, 2), make_card(14, 0)])
        last_play = [make_card(5, 2)]
        valid_plays = HandFinder.get_all_valid_plays(hand, last_play)

        best = AIStrategy.select_best(valid_plays, hand)
        self.assertEqual(best, [make_card(14, 0)])

    def test_ai_try_empty(self) -> None:
        # 當只剩最後一張時，AI 應該直接打出該張完成清手牌。
        hand = Hand([make_card(15, 3)])
        valid_plays = [[make_card(15, 3)]]

        best = AIStrategy.select_best(valid_plays, hand)
        self.assertEqual(best, [make_card(15, 3)])


if __name__ == "__main__":
    unittest.main(verbosity=2)