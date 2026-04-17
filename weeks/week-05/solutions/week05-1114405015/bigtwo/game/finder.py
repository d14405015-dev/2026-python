from __future__ import annotations

from itertools import combinations
from typing import Dict, List, Optional

from game.classifier import CardType, HandClassifier
from game.models import Card, Hand


class HandFinder:
    @staticmethod
    def find_singles(hand: Hand) -> List[List[Card]]:
        return [[card] for card in sorted(hand, key=lambda c: (c.rank, c.suit))]

    @staticmethod
    def _group_by_rank(hand: Hand) -> Dict[int, List[Card]]:
        groups: Dict[int, List[Card]] = {}
        for card in hand:
            groups.setdefault(card.rank, []).append(card)
        return groups

    @staticmethod
    def find_pairs(hand: Hand) -> List[List[Card]]:
        result: List[List[Card]] = []
        for cards in HandFinder._group_by_rank(hand).values():
            if len(cards) >= 2:
                result.extend([list(pair) for pair in combinations(sorted(cards, key=lambda c: c.suit), 2)])
        return result

    @staticmethod
    def find_triples(hand: Hand) -> List[List[Card]]:
        result: List[List[Card]] = []
        for cards in HandFinder._group_by_rank(hand).values():
            if len(cards) >= 3:
                result.extend([list(triple) for triple in combinations(sorted(cards, key=lambda c: c.suit), 3)])
        return result

    @staticmethod
    def _find_straight_from(hand: Hand, start_rank: int) -> Optional[List[Card]]:
        need = [start_rank + i for i in range(5)]
        by_rank = HandFinder._group_by_rank(hand)
        if all(rank in by_rank for rank in need):
            return [sorted(by_rank[rank], key=lambda c: c.suit)[0] for rank in need]
        return None

    @staticmethod
    def find_fives(hand: Hand) -> List[List[Card]]:
        result: List[List[Card]] = []
        for cards in combinations(hand, 5):
            card_list = list(cards)
            classified = HandClassifier.classify(card_list)
            if classified and classified[0] in {
                CardType.STRAIGHT,
                CardType.FULL_HOUSE,
                CardType.FOUR_OF_A_KIND,
                CardType.STRAIGHT_FLUSH,
            }:
                result.append(card_list)
        return result

    @staticmethod
    def get_all_valid_plays(
        hand: Hand, last_play: Optional[List[Card]], require_three_clubs: bool = True
    ) -> List[List[Card]]:
        if last_play is None:
            if require_three_clubs:
                first = hand.find_3_clubs()
                return [[first]] if first is not None else []

            candidates: List[List[Card]] = []
            candidates.extend(HandFinder.find_singles(hand))
            candidates.extend(HandFinder.find_pairs(hand))
            candidates.extend(HandFinder.find_triples(hand))
            candidates.extend(HandFinder.find_fives(hand))
            return candidates

        count = len(last_play)
        if count == 1:
            candidates = HandFinder.find_singles(hand)
        elif count == 2:
            candidates = HandFinder.find_pairs(hand)
        elif count == 3:
            candidates = HandFinder.find_triples(hand)
        elif count == 5:
            candidates = HandFinder.find_fives(hand)
        else:
            candidates = []

        return [cards for cards in candidates if HandClassifier.can_play(last_play, cards, require_three_clubs=False)]
