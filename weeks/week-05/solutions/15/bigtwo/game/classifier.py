from __future__ import annotations

from collections import Counter
from enum import IntEnum
from typing import Optional

from .models import Card


class CardType(IntEnum):
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


class HandClassifier:
    @staticmethod
    def _is_straight(ranks: list[int]) -> bool:
        if len(ranks) != 5 or len(set(ranks)) != 5:
            return False

        sorted_ranks = sorted(ranks)
        if sorted_ranks == [3, 4, 5, 14, 15]:
            return True

        return all(sorted_ranks[i + 1] - sorted_ranks[i] == 1 for i in range(4))

    @staticmethod
    def _is_flush(suits: list[int]) -> bool:
        return len(suits) == 5 and len(set(suits)) == 1

    @staticmethod
    def _straight_high_rank(ranks: list[int]) -> int:
        sorted_ranks = sorted(ranks)
        if sorted_ranks == [3, 4, 5, 14, 15]:
            return 5
        return sorted_ranks[-1]

    @staticmethod
    def classify(cards: list[Card]) -> Optional[tuple[CardType, int, int]]:
        if not cards:
            return None

        cards_sorted = sorted(cards, key=lambda c: c.to_sort_key())
        ranks = [c.rank for c in cards_sorted]
        suits = [c.suit for c in cards_sorted]
        counts = Counter(ranks)
        n = len(cards)

        if n == 1:
            c = cards[0]
            return (CardType.SINGLE, c.rank, c.suit)

        if n == 2 and len(counts) == 1:
            top = max(cards, key=lambda c: c.suit)
            return (CardType.PAIR, top.rank, top.suit)

        if n == 3 and len(counts) == 1:
            top = max(cards, key=lambda c: c.suit)
            return (CardType.TRIPLE, top.rank, top.suit)

        if n != 5:
            return None

        is_straight = HandClassifier._is_straight(ranks)
        is_flush = HandClassifier._is_flush(suits)

        if is_straight and is_flush:
            high_rank = HandClassifier._straight_high_rank(ranks)
            high_suit = max(c.suit for c in cards if c.rank == max(ranks))
            return (CardType.STRAIGHT_FLUSH, high_rank, high_suit)

        rank_count_values = sorted(counts.values(), reverse=True)
        if rank_count_values == [4, 1]:
            four_rank = next(rank for rank, count in counts.items() if count == 4)
            four_suit = max(c.suit for c in cards if c.rank == four_rank)
            return (CardType.FOUR_OF_A_KIND, four_rank, four_suit)

        if rank_count_values == [3, 2]:
            triple_rank = next(rank for rank, count in counts.items() if count == 3)
            triple_suit = max(c.suit for c in cards if c.rank == triple_rank)
            return (CardType.FULL_HOUSE, triple_rank, triple_suit)

        if is_flush:
            top = max(cards, key=lambda c: c.to_sort_key())
            return (CardType.FLUSH, top.rank, top.suit)

        if is_straight:
            high_rank = HandClassifier._straight_high_rank(ranks)
            candidates = [c for c in cards if c.rank == max(ranks)]
            if sorted(ranks) == [3, 4, 5, 14, 15]:
                candidates = [c for c in cards if c.rank == 5]
            high_suit = max(c.suit for c in candidates)
            return (CardType.STRAIGHT, high_rank, high_suit)

        return None

    @staticmethod
    def compare(play1: list[Card], play2: list[Card]) -> int:
        c1 = HandClassifier.classify(play1)
        c2 = HandClassifier.classify(play2)

        if c1 is None and c2 is None:
            return 0
        if c1 is None:
            return -1
        if c2 is None:
            return 1

        t1, r1, s1 = c1
        t2, r2, s2 = c2

        if t1 != t2:
            return 1 if t1 > t2 else -1
        if r1 != r2:
            return 1 if r1 > r2 else -1
        if s1 != s2:
            return 1 if s1 > s2 else -1
        return 0

    @staticmethod
    def can_play(last_play: Optional[list[Card]], cards: list[Card]) -> bool:
        if HandClassifier.classify(cards) is None:
            return False

        if last_play is None:
            return Card(3, 0) in cards

        if HandClassifier.classify(last_play) is None:
            return False

        if len(last_play) != len(cards):
            return False

        new_type = HandClassifier.classify(cards)[0]  # type: ignore[index]
        last_type = HandClassifier.classify(last_play)[0]  # type: ignore[index]

        # 5-card hands can be beaten by higher category, shorter hands must match type.
        if len(cards) != 5 and new_type != last_type:
            return False

        return HandClassifier.compare(cards, last_play) > 0
