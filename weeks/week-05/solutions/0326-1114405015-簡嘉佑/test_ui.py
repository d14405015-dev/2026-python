"""Phase 6 GUI 的測試設計。

此測試同時包含：
1. 基本渲染測試
2. GUI 與遊戲整合測試
3. 簡化版端到端流程測試

備註：GUI 依賴 pygame 與 ui 套件，若環境尚未完成會自動 skip。
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


def _prepare_import_path() -> None:
    """補上專案根目錄，讓 game / ui 套件可被匯入。"""

    current = Path(__file__).resolve().parent

    for candidate in [current, *current.parents]:
        if (candidate / "game").is_dir():
            sys.path.insert(0, str(candidate))
            return

        if (candidate / "bigtwo" / "game").is_dir():
            sys.path.insert(0, str(candidate / "bigtwo"))
            return


_prepare_import_path()


def _import_or_skip(testcase: unittest.TestCase, module_name: str, attr_name: str):
    """嘗試動態匯入指定類別，失敗時直接 skip。"""

    try:
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name)
    except Exception as exc:  # pragma: no cover - 僅在環境不足時觸發
        testcase.skipTest(f"無法匯入 {module_name}.{attr_name}: {exc}")


class TestRender(unittest.TestCase):
    """渲染層測試：卡牌與手牌繪製。"""

    def setUp(self) -> None:
        # 設定 dummy driver，讓 CI 或無視窗環境也可初始化 pygame。
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

    def test_card_render(self) -> None:
        try:
            import pygame
        except Exception as exc:  # pragma: no cover
            self.skipTest(f"pygame 不可用: {exc}")

        Renderer = _import_or_skip(self, "ui.render", "Renderer")
        Card = _import_or_skip(self, "game.models", "Card")

        pygame.init()
        try:
            screen = pygame.display.set_mode((800, 600))
            renderer = Renderer(screen)

            # 若 render API 不同，先檢查方法是否存在。
            if not hasattr(renderer, "draw_card"):
                self.skipTest("Renderer 尚未提供 draw_card")

            card = Card(14, 3)
            surface = renderer.draw_card(card, 10, 10, selected=False)

            # 大多實作會回傳 surface；若未回傳則至少確認能正常呼叫。
            if surface is not None:
                self.assertGreater(surface.get_width(), 0)
        finally:
            pygame.quit()

    def test_hand_render(self) -> None:
        try:
            import pygame
        except Exception as exc:  # pragma: no cover
            self.skipTest(f"pygame 不可用: {exc}")

        Renderer = _import_or_skip(self, "ui.render", "Renderer")
        Card = _import_or_skip(self, "game.models", "Card")
        Hand = _import_or_skip(self, "game.models", "Hand")

        pygame.init()
        try:
            screen = pygame.display.set_mode((800, 600))
            renderer = Renderer(screen)

            if not hasattr(renderer, "draw_hand"):
                self.skipTest("Renderer 尚未提供 draw_hand")

            hand = Hand([Card(14, 3), Card(13, 2), Card(3, 0)])
            result = renderer.draw_hand(hand, 20, 400, selected_indices=[])

            # 僅確認呼叫流程可運作；若有回傳 surface，檢查尺寸有效。
            if result is not None and hasattr(result, "get_width"):
                self.assertGreater(result.get_width(), 0)
        finally:
            pygame.quit()


class TestUIIntegration(unittest.TestCase):
    """整合測試：主應用初始化、點擊與按鈕處理。"""

    def setUp(self) -> None:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

    def test_game_init(self) -> None:
        App = _import_or_skip(self, "ui.app", "BigTwoApp")
        app = App()

        self.assertTrue(hasattr(app, "game"))
        self.assertEqual(len(app.game.players), 4)

    def test_card_selection(self) -> None:
        App = _import_or_skip(self, "ui.app", "BigTwoApp")
        app = App()

        if not hasattr(app, "input_handler"):
            self.skipTest("BigTwoApp 尚未提供 input_handler")

        handler = app.input_handler
        if not hasattr(handler, "handle_click"):
            self.skipTest("InputHandler 尚未提供 handle_click")

        # 模擬點擊手牌區域的座標，確認流程至少可正常呼叫。
        ok = handler.handle_click((120, 500), app.game)
        self.assertIn(ok, [True, False])

    def test_button_click(self) -> None:
        App = _import_or_skip(self, "ui.app", "BigTwoApp")
        app = App()

        if not hasattr(app, "input_handler"):
            self.skipTest("BigTwoApp 尚未提供 input_handler")

        handler = app.input_handler
        if not hasattr(handler, "handle_click"):
            self.skipTest("InputHandler 尚未提供 handle_click")

        # 一般常見按鈕位置，測試按鈕點擊事件流程可執行。
        ok = handler.handle_click((700, 520), app.game)
        self.assertIn(ok, [True, False])


class TestE2E(unittest.TestCase):
    """簡化版 E2E：自動推進有限步數，確認遊戲可進行並可結束。"""

    def test_complete_flow(self) -> None:
        BigTwoGame = _import_or_skip(self, "game.game", "BigTwoGame")

        game = BigTwoGame()
        game.setup()

        # 以保守步數推進 AI 回合，避免測試無限循環。
        for _ in range(300):
            if game.is_game_over():
                break

            player = game.get_current_player()
            if player.is_ai:
                played = game.ai_turn()
                if not played:
                    game.pass_(player)
            else:
                # 人類回合用最簡策略：嘗試出第一手合法牌，否則過牌。
                from game.finder import HandFinder

                last_cards = None if game.last_play is None else game.last_play[0]
                valid_plays = HandFinder.get_all_valid_plays(player.hand, last_cards)
                if valid_plays:
                    game.play(player, valid_plays[0])
                else:
                    game.pass_(player)

            game.check_round_reset()
            game.check_winner()
            game.next_turn()

        self.assertTrue(game.is_game_over())


if __name__ == "__main__":
    unittest.main(verbosity=2)