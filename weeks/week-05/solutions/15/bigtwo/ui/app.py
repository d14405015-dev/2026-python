from __future__ import annotations

try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore[assignment]

from game.game import BigTwoGame
from .input import InputHandler
from .render import Renderer


class BigTwoApp:
    def __init__(self) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required to run the app")

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 640))
        pygame.display.set_caption("Big Two")
        self.clock = pygame.time.Clock()

        self.game = BigTwoGame()
        self.game.setup()

        self.renderer = Renderer(self.screen)
        self.buttons = {
            "play": pygame.Rect(760, 500, 100, 40),
            "pass": pygame.Rect(880, 500, 100, 40),
        }
        self.input_handler = InputHandler(self.renderer, self.buttons)

    def handle_events(self) -> bool:
        if pygame is None:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.game.is_game_over():
                continue

            player = self.game.get_current_player()
            if player.is_ai:
                self.game.ai_turn()
                continue

            self.input_handler.handle_event(event, self.game)

        return True

    def render(self) -> None:
        if pygame is None:
            return

        self.screen.fill(Renderer.COLORS["background"])

        positions = [(60, 40), (420, 40), (760, 40), (60, 120)]
        for i, player in enumerate(self.game.players):
            x, y = positions[i]
            self.renderer.draw_player(player, x, y, is_current=(i == self.game.current_player))

        human = self.game.players[0]
        self.renderer.draw_hand(human.hand, 120, 480, self.input_handler.selected_indices)

        if self.game.last_play is not None:
            cards, player_name = self.game.last_play
            self.renderer.draw_last_play(cards, player_name, 360, 260)

        self.renderer.draw_buttons(self.buttons, 760, 500)

        if self.game.is_game_over() and self.game.winner is not None:
            msg = self.renderer.font.render(f"Winner: {self.game.winner.name}", True, (255, 225, 100))
            self.screen.blit(msg, (380, 320))

    def run(self) -> None:
        if pygame is None:
            return

        running = True
        while running:
            running = self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
