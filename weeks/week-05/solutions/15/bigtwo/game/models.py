from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Optional


@dataclass(frozen=True, order=True)
class Card:
    rank: int
    suit: int

    SUIT_SYMBOLS = ("♣", "♦", "♥", "♠")
    RANK_SYMBOLS = {
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
        15: "2",
    }

    def __post_init__(self) -> None:
        if not 3 <= self.rank <= 15:
            raise ValueError("rank must be in [3, 15]")
        if not 0 <= self.suit <= 3:
            raise ValueError("suit must be in [0, 3]")

    def __repr__(self) -> str:
        rank_text = self.RANK_SYMBOLS.get(self.rank, str(self.rank))
        return f"{self.SUIT_SYMBOLS[self.suit]}{rank_text}"

    def to_sort_key(self) -> tuple[int, int]:
        return (self.rank, self.suit)


class Deck:
    def __init__(self) -> None:
        self.cards = self._create_cards()

    def _create_cards(self) -> list[Card]:
        cards: list[Card] = []
        for rank in range(3, 16):
            for suit in range(4):
                cards.append(Card(rank, suit))
        return cards

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int) -> list[Card]:
        n = max(0, min(n, len(self.cards)))
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt


class Hand(list[Card]):
    def __init__(self, cards: Optional[Iterable[Card]] = None) -> None:
        super().__init__(cards or [])

    def sort_desc(self) -> None:
        self.sort(key=lambda c: (-c.rank, c.suit))

    def find_3_clubs(self) -> Optional[Card]:
        target = Card(3, 0)
        for card in self:
            if card == target:
                return card
        return None

    def remove(self, cards: Iterable[Card]) -> None:  # type: ignore[override]
        for card in cards:
            if card in self:
                super().remove(card)


class Player:
    def __init__(self, name: str, is_ai: bool = False) -> None:
        self.name = name
        self.is_ai = is_ai
        self.hand = Hand()
        self.score = 0

    def take_cards(self, cards: Iterable[Card]) -> None:
        self.hand.extend(cards)
        self.hand.sort_desc()

    def play_cards(self, cards: Iterable[Card]) -> list[Card]:
        played = list(cards)
        self.hand.remove(played)
        self.hand.sort_desc()
        return played
