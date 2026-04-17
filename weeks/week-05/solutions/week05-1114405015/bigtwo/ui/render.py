from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import pygame
except ModuleNotFoundError:  # pragma: no cover
    pygame = None

from game.models import Card, RANK_SYMBOLS, SUIT_SYMBOLS


class Renderer:
    COLORS: Dict[str, Tuple[int, int, int]] = {
        "background": (45, 45, 45),
        "card_back": (74, 144, 217),
        "spade_club": (35, 35, 35),
        "heart_diamond": (231, 76, 60),
        "player": (46, 204, 113),
        "ai": (149, 165, 166),
        "selected": (241, 196, 15),
        "button": (52, 152, 219),
        "muted": (210, 210, 210),
        "warning": (255, 210, 80),
    }

    CARD_WIDTH = 60
    CARD_HEIGHT = 90

    def __init__(self, screen):
        if pygame is None:
            raise RuntimeError("pygame is required for GUI")
        self.screen = screen
        self.font = self._pick_font(24, bold=True)
        self.small_font = self._pick_font(20)
        self.suit_font = self._pick_font(30)

    def _pick_font(self, size: int, bold: bool = False):
        # Prefer fonts with full suit-symbol glyph coverage on Windows.
        font_candidates = [
            "Segoe UI Symbol",
            "Segoe UI Emoji",
            "Arial Unicode MS",
            "Noto Sans Symbols 2",
            "DejaVu Sans",
            "Arial",
        ]
        for name in font_candidates:
            path = pygame.font.match_font(name)
            if path:
                return pygame.font.Font(path, size)
        return pygame.font.SysFont(None, size, bold=bold)

    def draw_card(self, card: Optional[Card], x: int, y: int, selected: bool = False, back: bool = False):
        rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        color = self.COLORS["selected"] if selected else self.COLORS["card_back"] if back else (245, 245, 245)
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, width=2, border_radius=6)

        if card is not None and not back:
            txt_color = self.COLORS["heart_diamond"] if card.suit in (1, 2) else self.COLORS["spade_club"]
            rank = RANK_SYMBOLS[card.rank]
            suit = SUIT_SYMBOLS[card.suit]

            rank_surf = self.font.render(rank, True, txt_color)
            suit_surf = self.small_font.render(suit, True, txt_color)
            center_suit = self.suit_font.render(suit, True, txt_color)

            self.screen.blit(rank_surf, (x + 6, y + 4))
            self.screen.blit(suit_surf, (x + 7, y + 25))

            center_rect = center_suit.get_rect(center=(x + self.CARD_WIDTH // 2, y + self.CARD_HEIGHT // 2 + 6))
            self.screen.blit(center_suit, center_rect)
        return rect

    def draw_hand(self, hand: Sequence[Card], x: int, y: int, selected_indices: Iterable[int]):
        rects = []
        selected_set = set(selected_indices)
        for i, card in enumerate(hand):
            rect = self.draw_card(card, x + i * 28, y, selected=i in selected_set)
            rects.append(rect)
        return rects

    def draw_player(self, player, x: int, y: int, is_current: bool):
        color = self.COLORS["player"] if not player.is_ai else self.COLORS["ai"]
        if is_current:
            color = self.COLORS["selected"]
        surf = self.font.render(player.name, True, color)
        self.screen.blit(surf, (x, y))

    def draw_last_play(self, cards: List[Card], player_name: str, x: int, y: int):
        title = self.font.render(f"Last: {player_name}", True, (255, 255, 255))
        self.screen.blit(title, (x, y))
        for i, card in enumerate(cards):
            self.draw_card(card, x + i * 28, y + 28)

    def draw_buttons(self, buttons: Dict[str, Tuple[int, int, int, int]], x: int = 0, y: int = 0):
        for name, (bx, by, bw, bh) in buttons.items():
            rect = pygame.Rect(bx + x, by + y, bw, bh)
            pygame.draw.rect(self.screen, self.COLORS["button"], rect, border_radius=6)
            label = self.font.render(name.upper(), True, (255, 255, 255))
            self.screen.blit(label, (bx + 10, by + 10))

    def draw_status(self, hint: str, status: str, x: int, y: int):
        hint_surf = self.small_font.render(hint, True, self.COLORS["warning"])
        status_surf = self.small_font.render(status, True, self.COLORS["muted"])
        self.screen.blit(hint_surf, (x, y))
        self.screen.blit(status_surf, (x, y + 22))
