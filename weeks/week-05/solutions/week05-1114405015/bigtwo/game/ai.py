from __future__ import annotations

from typing import List, Optional

from game.classifier import CardType, HandClassifier
from game.models import Card, Hand


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
    def score_play(cards: List[Card], hand: Hand, is_first: bool = False) -> float:
        classified = HandClassifier.classify(cards)
        if classified is None:
            return float("-inf")

        card_type, rank, _ = classified
        score = AIStrategy.TYPE_SCORES[card_type] * 100 + rank * 10

        remaining = len(hand) - len(cards)
        if remaining == 1:
            score += AIStrategy.EMPTY_HAND_BONUS
        elif remaining <= 3:
            score += AIStrategy.NEAR_EMPTY_BONUS

        score += sum(AIStrategy.SPADE_BONUS for card in cards if card.suit == 3)

        if is_first and any(card.rank == 3 and card.suit == 0 for card in cards):
            score += 1

        return float(score)

    @staticmethod
    def select_best(
        valid_plays: List[List[Card]], hand: Hand, is_first: bool = False
    ) -> Optional[List[Card]]:
        if not valid_plays:
            return None

        if is_first:
            first_turn_candidates = [
                play for play in valid_plays if any(card.rank == 3 and card.suit == 0 for card in play)
            ]
            if first_turn_candidates:
                valid_plays = first_turn_candidates

        return max(valid_plays, key=lambda play: AIStrategy.score_play(play, hand, is_first=is_first))
