from __future__ import annotations

from typing import Optional

from .ai import AIStrategy
from .classifier import HandClassifier
from .finder import HandFinder
from .models import Card, Deck, Player


class BigTwoGame:
    def __init__(self) -> None:
        self.deck = Deck()
        self.players = [
            Player("Player", is_ai=False),
            Player("AI_1", is_ai=True),
            Player("AI_2", is_ai=True),
            Player("AI_3", is_ai=True),
        ]
        self.current_player = 0
        self.last_play: Optional[tuple[list[Card], str]] = None
        self.pass_count = 0
        self.winner: Optional[Player] = None
        self.round_number = 1
        self.first_round = True

    def setup(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        for player in self.players:
            player.hand.clear()

        for player in self.players:
            player.take_cards(self.deck.deal(13))

        for i, player in enumerate(self.players):
            if Card(3, 0) in player.hand:
                self.current_player = i
                break

        self.last_play = None
        self.pass_count = 0
        self.winner = None
        self.round_number = 1
        self.first_round = True

    def _is_current_player(self, player: Player) -> bool:
        return player is self.get_current_player()

    def _is_valid_play(self, cards: list[Card]) -> bool:
        if self.first_round:
            return Card(3, 0) in cards and HandClassifier.classify(cards) is not None

        if self.last_play is None:
            return HandClassifier.classify(cards) is not None

        return HandClassifier.can_play(self.last_play[0], cards)

    def play(self, player: Player, cards: list[Card]) -> bool:
        if not self._is_current_player(player):
            return False
        if any(card not in player.hand for card in cards):
            return False
        if not self._is_valid_play(cards):
            return False

        played = player.play_cards(cards)
        self.last_play = (played, player.name)
        self.pass_count = 0

        if self.first_round and Card(3, 0) in played:
            self.first_round = False

        self.check_winner()
        return True

    def pass_(self, player: Player) -> bool:
        if not self._is_current_player(player):
            return False
        if self.last_play is None:
            return False

        self.pass_count += 1
        return True

    def next_turn(self) -> None:
        self.current_player = (self.current_player + 1) % 4
        self.round_number += 1

    def check_round_reset(self) -> None:
        if self.pass_count >= 3:
            self.last_play = None
            self.pass_count = 0

    def check_winner(self) -> Optional[Player]:
        for player in self.players:
            if len(player.hand) == 0:
                self.winner = player
                return player
        return None

    def is_game_over(self) -> bool:
        return self.winner is not None

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def ai_turn(self) -> bool:
        player = self.get_current_player()
        if not player.is_ai:
            return False

        last_cards = self.last_play[0] if self.last_play is not None else None
        valid_plays = HandFinder.get_all_valid_plays(player.hand, last_cards)
        play = AIStrategy.select_best(valid_plays, player.hand, is_first=self.first_round)

        if play is None:
            if self.pass_(player):
                self.next_turn()
                self.check_round_reset()
                return True
            return False

        if self.play(player, play):
            self.next_turn()
            self.check_round_reset()
            return True
        return False
