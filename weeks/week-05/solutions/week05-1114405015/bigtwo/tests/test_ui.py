import unittest

try:
    import pygame
except ModuleNotFoundError:
    pygame = None

from game.models import Card, Hand


@unittest.skipIf(pygame is None, "pygame not installed")
class TestUI(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((400, 300))

    def tearDown(self):
        pygame.quit()

    def test_card_render(self):
        from ui.render import Renderer

        renderer = Renderer(self.screen)
        rect = renderer.draw_card(Card(14, 3), 10, 10)
        self.assertGreater(rect.width, 0)

    def test_hand_render(self):
        from ui.render import Renderer

        renderer = Renderer(self.screen)
        hand = Hand([Card(14, 3), Card(13, 2), Card(3, 0)])
        rects = renderer.draw_hand(hand, 10, 10, selected_indices=[])
        self.assertEqual(len(rects), 3)


if __name__ == "__main__":
    unittest.main()
