from __future__ import annotations

from typing import Dict, List, Tuple

try:
    import pygame
except ModuleNotFoundError:  # pragma: no cover
    pygame = None


class InputHandler:
    def __init__(self, renderer, buttons: Dict[str, Tuple[int, int, int, int]]):
        self.renderer = renderer
        self.selected_indices: List[int] = []
        self.buttons = buttons

    def handle_event(self, event, game) -> bool:
        if pygame is None:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_click(event.pos, game)
        if event.type == pygame.KEYDOWN:
            return self.handle_key(event.key, game)
        return False

    def handle_click(self, pos, game) -> bool:
        x, y = pos
        for name, (bx, by, bw, bh) in self.buttons.items():
            if bx <= x <= bx + bw and by <= y <= by + bh:
                if name == "play":
                    return self.try_play(game)
                if name == "pass":
                    return game.pass_(game.get_current_player())

        player = game.get_current_player()
        if player.is_ai:
            return False

        card_y = 500
        if not (card_y <= y <= card_y + self.renderer.CARD_HEIGHT):
            return False

        for idx in range(len(player.hand) - 1, -1, -1):
            card_x = 120 + idx * 28
            if card_x <= x <= card_x + self.renderer.CARD_WIDTH:
                if idx in self.selected_indices:
                    self.selected_indices.remove(idx)
                else:
                    self.selected_indices.append(idx)
                self.selected_indices.sort()
                return True
        return False

    def handle_key(self, key, game) -> bool:
        if pygame is None:
            return False
        if key == pygame.K_RETURN:
            return self.try_play(game)
        if key == pygame.K_p:
            return game.pass_(game.get_current_player())
        if key == pygame.K_c:
            self.selected_indices.clear()
            game.status_message = "Selection cleared"
            return True
        if key == pygame.K_h:
            valid = game.get_valid_plays_for_current()
            game.status_message = f"Hint: {len(valid)} valid play(s)"
            return True
        return False

    def try_play(self, game) -> bool:
        player = game.get_current_player()
        if player.is_ai:
            game.status_message = "Wait for AI turn"
            return False
        cards = [player.hand[idx] for idx in self.selected_indices if idx < len(player.hand)]
        if not cards:
            game.status_message = "Select card(s) first"
            return False
        success = game.play(player, cards)
        if success:
            self.selected_indices.clear()
        return success
