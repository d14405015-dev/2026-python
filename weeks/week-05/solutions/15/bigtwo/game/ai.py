from __future__ import annotations

from typing import Optional

from .classifier import CardType, HandClassifier
from .models import Card, Hand


class AIStrategy:
    TYPE_SCORES = {
        CardType.SINGLE: 1,
        CardType.PAIR: 2,
        CardType.TRIPLE: 3,
        CardType.STRAIGHT: 4,
        CardType.FLUSH: 5,
        CardType.FULL_HOUSE: 6,
        CardType.FOUR_OF_A_KIND: 7,
        CardType.STRAIGHT_FLUSH: 8,
    }

    EMPTY_HAND_BONUS = 10000
    NEAR_EMPTY_BONUS = 500
    SPADE_BONUS = 5

    @staticmethod
    def score_play(cards: list[Card], hand: Hand, is_first: bool = False) -> float:
        info = HandClassifier.classify(cards)
        if info is None:
            return float("-inf")

        card_type, rank, _ = info
        remaining = len(hand) - len(cards)
        score = AIStrategy.TYPE_SCORES[card_type] * 100 + rank * 10

        if remaining == 0:
            score += AIStrategy.EMPTY_HAND_BONUS
        elif remaining <= 3:
            score += AIStrategy.NEAR_EMPTY_BONUS

        score += sum(AIStrategy.SPADE_BONUS for c in cards if c.suit == 3)

        if is_first and Card(3, 0) in cards:
            score += 1000

        return float(score)

    @staticmethod
    def select_best(valid_plays: list[list[Card]], hand: Hand, is_first: bool = False) -> Optional[list[Card]]:
        if not valid_plays:
            return None

        if is_first:
            opening = [play for play in valid_plays if Card(3, 0) in play]
            if opening:
                return max(opening, key=lambda p: AIStrategy.score_play(p, hand, is_first=True))

        return max(valid_plays, key=lambda p: AIStrategy.score_play(p, hand, is_first=False))
