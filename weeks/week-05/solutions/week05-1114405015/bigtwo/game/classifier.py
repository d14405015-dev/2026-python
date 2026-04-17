from __future__ import annotations

from collections import Counter
from enum import IntEnum
from typing import List, Optional, Tuple

from game.models import Card


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
    def _is_straight(ranks: List[int]) -> bool:
        uniq = sorted(set(ranks))
        if len(uniq) != 5:
            return False
        if uniq == [3, 4, 5, 14, 15]:
            return True
        return all(uniq[i + 1] - uniq[i] == 1 for i in range(4))

    @staticmethod
    def _straight_high_rank(ranks: List[int]) -> int:
        uniq = sorted(set(ranks))
        if uniq == [3, 4, 5, 14, 15]:
            return 5
        return max(uniq)

    @staticmethod
    def _is_flush(suits: List[int]) -> bool:
        return len(set(suits)) == 1

    @staticmethod
    def classify(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        if not cards:
            return None

        cards_sorted = sorted(cards, key=lambda c: (c.rank, c.suit))
        ranks = [c.rank for c in cards_sorted]
        suits = [c.suit for c in cards_sorted]
        n = len(cards_sorted)
        rank_counter = Counter(ranks)
        rank_counts = sorted(rank_counter.values(), reverse=True)

        if n == 1:
            card = cards_sorted[0]
            return (CardType.SINGLE, card.rank, card.suit)

        if n == 2 and len(rank_counter) == 1:
            return (CardType.PAIR, ranks[0], max(suits))

        if n == 3 and len(rank_counter) == 1:
            return (CardType.TRIPLE, ranks[0], max(suits))

        if n != 5:
            return None

        is_straight = HandClassifier._is_straight(ranks)
        is_flush = HandClassifier._is_flush(suits)

        if is_straight and is_flush:
            return (CardType.STRAIGHT_FLUSH, HandClassifier._straight_high_rank(ranks), suits[0])

        if rank_counts == [4, 1]:
            four_rank = max(rank_counter, key=lambda r: rank_counter[r])
            return (CardType.FOUR_OF_A_KIND, four_rank, 0)

        if rank_counts == [3, 2]:
            triple_rank = max(rank_counter, key=lambda r: rank_counter[r])
            return (CardType.FULL_HOUSE, triple_rank, 0)

        # Rule variant: plain flush is not a legal play.
        if is_flush:
            return None

        if is_straight:
            return (CardType.STRAIGHT, HandClassifier._straight_high_rank(ranks), 0)

        return None

    @staticmethod
    def compare(play1: List[Card], play2: List[Card]) -> int:
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
    def can_play(
        last_play: Optional[List[Card]], cards: List[Card], require_three_clubs: bool = True
    ) -> bool:
        if HandClassifier.classify(cards) is None:
            return False

        if last_play is None:
            if require_three_clubs:
                return any(card.rank == 3 and card.suit == 0 for card in cards)
            return True

        if len(last_play) != len(cards):
            return False

        return HandClassifier.compare(cards, last_play) == 1
