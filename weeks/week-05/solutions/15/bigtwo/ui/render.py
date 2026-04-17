from __future__ import annotations

from typing import Iterable

try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore[assignment]

from game.models import Card, Hand, Player


class Renderer:
    COLORS = {
        "background": (45, 45, 45),
        "card_back": (74, 144, 217),
        "spade_club": (255, 255, 255),
        "heart_diamond": (231, 76, 60),
        "player": (46, 204, 113),
        "ai": (149, 165, 166),
        "selected": (241, 196, 15),
        "button": (52, 152, 219),
    }

    CARD_WIDTH = 60
    CARD_HEIGHT = 90

    def __init__(self, screen: "pygame.Surface") -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for UI")
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 16)

    def draw_card(self, card: Card, x: int, y: int, selected: bool = False) -> "pygame.Rect":
        if pygame is None:
            raise RuntimeError("pygame is required for UI")

        rect = pygame.Rect(x, y - (10 if selected else 0), self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, (250, 250, 250), rect, border_radius=6)
        border_color = self.COLORS["selected"] if selected else (30, 30, 30)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=6)

        color = self.COLORS["heart_diamond"] if card.suit in (1, 2) else self.COLORS["spade_club"]
        text_surface = self.font.render(repr(card), True, color)
        self.screen.blit(text_surface, (rect.x + 6, rect.y + 8))
        return rect

    def draw_hand(self, hand: Hand, x: int, y: int, selected_indices: set[int]) -> list["pygame.Rect"]:
        rects: list["pygame.Rect"] = []
        overlap = 35
        for i, card in enumerate(hand):
            rects.append(self.draw_card(card, x + i * overlap, y, selected=i in selected_indices))
        return rects

    def draw_player(self, player: Player, x: int, y: int, is_current: bool) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for UI")

        color = self.COLORS["player"] if not player.is_ai else self.COLORS["ai"]
        if is_current:
            color = self.COLORS["selected"]

        text = f"{player.name}: {len(player.hand)} cards"
        surface = self.small_font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_last_play(self, cards: Iterable[Card], player_name: str, x: int, y: int) -> None:
        label = self.small_font.render(f"Last: {player_name}", True, (230, 230, 230))
        self.screen.blit(label, (x, y - 26))

        for i, card in enumerate(cards):
            self.draw_card(card, x + i * 42, y)

    def draw_buttons(self, buttons: dict[str, "pygame.Rect"], x: int, y: int) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required for UI")

        for name, rect in buttons.items():
            pygame.draw.rect(self.screen, self.COLORS["button"], rect, border_radius=6)
            label = self.small_font.render(name.upper(), True, (255, 255, 255))
            self.screen.blit(label, (rect.x + 12, rect.y + 8))
