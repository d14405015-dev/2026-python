from __future__ import annotations

from itertools import combinations
from typing import Optional

from .classifier import HandClassifier
from .models import Card, Hand


class HandFinder:
    @staticmethod
    def find_singles(hand: Hand) -> list[list[Card]]:
        return [[card] for card in sorted(hand, key=lambda c: c.to_sort_key())]

    @staticmethod
    def find_pairs(hand: Hand) -> list[list[Card]]:
        pairs: list[list[Card]] = []
        by_rank: dict[int, list[Card]] = {}
        for card in hand:
            by_rank.setdefault(card.rank, []).append(card)

        for cards in by_rank.values():
            if len(cards) >= 2:
                for combo in combinations(sorted(cards, key=lambda c: c.suit), 2):
                    pairs.append(list(combo))
        return pairs

    @staticmethod
    def find_triples(hand: Hand) -> list[list[Card]]:
        triples: list[list[Card]] = []
        by_rank: dict[int, list[Card]] = {}
        for card in hand:
            by_rank.setdefault(card.rank, []).append(card)

        for cards in by_rank.values():
            if len(cards) >= 3:
                for combo in combinations(sorted(cards, key=lambda c: c.suit), 3):
                    triples.append(list(combo))
        return triples

    @staticmethod
    def _find_straight_from(hand: Hand, start_rank: int) -> Optional[list[Card]]:
        need = [start_rank + i for i in range(5)]
        if start_rank == 3:
            special = [3, 4, 5, 14, 15]
            if all(any(c.rank == r for c in hand) for r in special):
                result = [next(c for c in sorted(hand, key=lambda x: x.suit) if c.rank == r) for r in special]
                return result

        result: list[Card] = []
        for rank in need:
            found = [c for c in hand if c.rank == rank]
            if not found:
                return None
            result.append(sorted(found, key=lambda c: c.suit)[0])
        return result

    @staticmethod
    def find_fives(hand: Hand) -> list[list[Card]]:
        all_fives: list[list[Card]] = []
        seen: set[tuple[tuple[int, int], ...]] = set()

        for combo in combinations(hand, 5):
            cards = list(combo)
            if HandClassifier.classify(cards) is None:
                continue
            key = tuple(sorted((c.rank, c.suit) for c in cards))
            if key not in seen:
                seen.add(key)
                all_fives.append(cards)

        return all_fives

    @staticmethod
    def get_all_valid_plays(hand: Hand, last_play: Optional[list[Card]]) -> list[list[Card]]:
        if last_play is None:
            three_clubs = Card(3, 0)
            return [[three_clubs]] if three_clubs in hand else []

        target_len = len(last_play)
        if target_len == 1:
            candidates = HandFinder.find_singles(hand)
        elif target_len == 2:
            candidates = HandFinder.find_pairs(hand)
        elif target_len == 3:
            candidates = HandFinder.find_triples(hand)
        elif target_len == 5:
            candidates = HandFinder.find_fives(hand)
        else:
            return []

        valid: list[list[Card]] = []
        for play in candidates:
            if HandClassifier.can_play(last_play, play):
                valid.append(play)

        return valid
