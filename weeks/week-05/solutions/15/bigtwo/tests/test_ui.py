import os
import unittest
from unittest.mock import MagicMock

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None

from game.models import Card, Hand


@unittest.skipIf(pygame is None, "pygame not installed")
class TestUI(unittest.TestCase):
    def setUp(self):
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.Surface((800, 600))

    def tearDown(self):
        pygame.display.quit()
        pygame.font.quit()

    def test_card_render(self):
        from ui.render import Renderer

        renderer = Renderer(self.screen)
        rect = renderer.draw_card(Card(14, 3), 20, 20)
        self.assertGreater(rect.width, 0)

    def test_hand_render(self):
        from ui.render import Renderer

        renderer = Renderer(self.screen)
        hand = Hand([Card(14, 3), Card(13, 2), Card(3, 0)])
        rects = renderer.draw_hand(hand, 20, 20, set())
        self.assertEqual(len(rects), 3)

    def test_game_init(self):
        from ui.app import BigTwoApp

        app = BigTwoApp()
        self.assertEqual(len(app.game.players), 4)

    def test_button_click(self):
        from ui.input import InputHandler
        from ui.render import Renderer
        from game.game import BigTwoGame

        game = BigTwoGame()
        game.setup()
        renderer = Renderer(self.screen)
        buttons = {
            "play": pygame.Rect(760, 500, 100, 40),
            "pass": pygame.Rect(880, 500, 100, 40),
        }
        input_handler = InputHandler(renderer, buttons)

        game.play(game.get_current_player(), [Card(3, 0)])
        game.next_turn()

        result = input_handler.handle_click((885, 505), game)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
