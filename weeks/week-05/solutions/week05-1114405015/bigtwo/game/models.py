from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Optional

SUIT_SYMBOLS = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
RANK_SYMBOLS = {
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "T",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
    15: "2",
}


@dataclass(frozen=True, order=False)
class Card:
    rank: int
    suit: int

    def __repr__(self) -> str:
        return f"{SUIT_SYMBOLS[self.suit]}{RANK_SYMBOLS[self.rank]}"

    def __lt__(self, other: "Card") -> bool:
        return self.to_sort_key() < other.to_sort_key()

    def to_sort_key(self) -> tuple[int, int]:
        return (self.rank, self.suit)


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = self._create_cards()

    def _create_cards(self) -> List[Card]:
        return [Card(rank, suit) for rank in range(3, 16) for suit in range(4)]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int) -> List[Card]:
        take = min(n, len(self.cards))
        dealt = self.cards[:take]
        self.cards = self.cards[take:]
        return dealt


class Hand(list):
    def __init__(self, cards: Optional[Iterable[Card]] = None):
        super().__init__(cards or [])

    def sort_desc(self) -> None:
        self.sort(key=lambda c: (c.rank, c.suit), reverse=True)

    def find_3_clubs(self) -> Optional[Card]:
        for card in self:
            if card.rank == 3 and card.suit == 0:
                return card
        return None

    def remove(self, cards: Iterable[Card]) -> None:
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

    def play_cards(self, cards: List[Card]) -> List[Card]:
        self.hand.remove(cards)
        return list(cards)
