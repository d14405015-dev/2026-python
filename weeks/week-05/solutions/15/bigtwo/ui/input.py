from __future__ import annotations

try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore[assignment]

from game.game import BigTwoGame


class InputHandler:
    def __init__(self, renderer, buttons):
        self.renderer = renderer
        self.selected_indices: set[int] = set()
        self.buttons = buttons

    def handle_event(self, event, game: BigTwoGame) -> bool:
        if pygame is None:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_click(event.pos, game)
        if event.type == pygame.KEYDOWN:
            return self.handle_key(event.key, game)
        return False

    def handle_click(self, pos, game: BigTwoGame) -> bool:
        if pygame is None:
            return False

        if self.buttons["play"].collidepoint(pos):
            return self.try_play(game)
        if self.buttons["pass"].collidepoint(pos):
            player = game.get_current_player()
            ok = game.pass_(player)
            if ok:
                game.next_turn()
                game.check_round_reset()
                self.selected_indices.clear()
            return ok

        player = game.get_current_player()
        if player.is_ai:
            return False

        x_start = 120
        y = 480
        overlap = 35

        for i in range(len(player.hand) - 1, -1, -1):
            rect = pygame.Rect(x_start + i * overlap, y, self.renderer.CARD_WIDTH, self.renderer.CARD_HEIGHT)
            if rect.collidepoint(pos):
                if i in self.selected_indices:
                    self.selected_indices.remove(i)
                else:
                    self.selected_indices.add(i)
                return True
        return False

    def handle_key(self, key, game: BigTwoGame) -> bool:
        if pygame is None:
            return False

        if key == pygame.K_RETURN:
            return self.try_play(game)
        if key == pygame.K_p:
            player = game.get_current_player()
            ok = game.pass_(player)
            if ok:
                game.next_turn()
                game.check_round_reset()
                self.selected_indices.clear()
            return ok
        return False

    def try_play(self, game: BigTwoGame) -> bool:
        player = game.get_current_player()
        if player.is_ai or not self.selected_indices:
            return False

        cards = [player.hand[i] for i in sorted(self.selected_indices)]
        ok = game.play(player, cards)
        if ok:
            self.selected_indices.clear()
            game.next_turn()
            game.check_round_reset()
        return ok
