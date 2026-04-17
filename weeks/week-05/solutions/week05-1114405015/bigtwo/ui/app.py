from __future__ import annotations

import os

# Use headless mode only when explicitly requested by tests/CI.
if os.environ.get("BIGTWO_HEADLESS") == "1":
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

try:
    import pygame
except ModuleNotFoundError:  # pragma: no cover
    pygame = None

from game.game import BigTwoGame
from ui.input import InputHandler
from ui.render import Renderer


class BigTwoApp:
    def __init__(self) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for GUI")

        pygame.init()
        self.screen = pygame.display.set_mode((1024, 640))
        pygame.display.set_caption("Big Two")
        self.clock = pygame.time.Clock()

        self.game = BigTwoGame()
        self.game.setup()

        self.buttons = {
            "play": (820, 500, 120, 40),
            "pass": (820, 550, 120, 40),
        }
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler(self.renderer, self.buttons)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.game.is_game_over():
                self.input_handler.handle_event(event, self.game)
        return True

    def render(self) -> None:
        self.screen.fill(self.renderer.COLORS["background"])

        for idx, player in enumerate(self.game.players):
            y = 40 + idx * 90
            self.renderer.draw_player(player, 40, y, idx == self.game.current_player)
            if player.is_ai:
                for c in range(len(player.hand)):
                    self.renderer.draw_card(None, 180 + c * 12, y, back=True)

        human = self.game.players[0]
        self.renderer.draw_hand(human.hand, 120, 500, self.input_handler.selected_indices)

        if self.game.last_play is not None:
            cards, name = self.game.last_play
            self.renderer.draw_last_play(cards, name, 450, 260)

        self.renderer.draw_buttons(self.buttons)
        self.renderer.draw_status(
            self.game.get_rule_hint(),
            self.game.status_message,
            120,
            450,
        )

        if self.game.is_game_over():
            winner = self.game.check_winner()
            txt = self.renderer.font.render(f"Winner: {winner.name}", True, (255, 255, 0))
            self.screen.blit(txt, (420, 20))

        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            if not self.game.is_game_over() and self.game.get_current_player().is_ai:
                self.game.ai_turn()

            running = self.handle_events()
            self.render()
            self.clock.tick(30)

        pygame.quit()
