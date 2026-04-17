from __future__ import annotations

from typing import List, Optional, Tuple

from game.ai import AIStrategy
from game.classifier import HandClassifier
from game.finder import HandFinder
from game.models import Card, Deck, Player


class BigTwoGame:
    def __init__(self) -> None:
        self.deck = Deck()
        self.players: List[Player] = []
        self.current_player = 0
        self.last_play: Optional[Tuple[List[Card], str]] = None
        self.pass_count = 0
        self.winner: Optional[Player] = None
        self.round_number = 1
        self.first_turn_required = True
        self.status_message = "Game started"

    def setup(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        self.players = [
            Player("Player1", is_ai=False),
            Player("AI_1", is_ai=True),
            Player("AI_2", is_ai=True),
            Player("AI_3", is_ai=True),
        ]

        for player in self.players:
            player.take_cards(self.deck.deal(13))

        for idx, player in enumerate(self.players):
            if player.hand.find_3_clubs() is not None:
                self.current_player = idx
                break

        self.last_play = None
        self.pass_count = 0
        self.winner = None
        self.round_number = 1
        self.first_turn_required = True
        self.status_message = "Find and play 3♣ to start"

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def _is_valid_play(self, cards: List[Card]) -> bool:
        last_cards = self.last_play[0] if self.last_play else None
        return HandClassifier.can_play(
            last_cards,
            cards,
            require_three_clubs=(self.first_turn_required and self.last_play is None),
        )

    def get_valid_plays_for_current(self) -> List[List[Card]]:
        player = self.get_current_player()
        last_cards = self.last_play[0] if self.last_play else None
        return HandFinder.get_all_valid_plays(
            player.hand,
            last_cards,
            require_three_clubs=(self.first_turn_required and self.last_play is None),
        )

    def get_rule_hint(self) -> str:
        if self.winner is not None:
            return f"Winner: {self.winner.name}"
        if self.first_turn_required and self.last_play is None:
            return "Opening move must include 3♣"
        if self.last_play is None:
            return "Free lead: play any valid combo"
        last_cards, player_name = self.last_play
        return f"Beat {player_name}'s {len(last_cards)}-card play"

    def play(self, player: Player, cards: List[Card]) -> bool:
        if self.winner is not None:
            self.status_message = "Game is over"
            return False
        if player != self.get_current_player():
            self.status_message = "Not your turn"
            return False
        if not all(card in player.hand for card in cards):
            self.status_message = "Selected cards are invalid"
            return False
        if not self._is_valid_play(cards):
            self.status_message = "Invalid play for current rule"
            return False

        played = player.play_cards(cards)
        self.last_play = (played, player.name)
        self.pass_count = 0
        self.first_turn_required = False
        self.status_message = f"{player.name} played {len(played)} card(s)"

        if len(player.hand) == 0:
            self.winner = player
            self.status_message = f"Winner: {player.name}"
            return True

        self.next_turn()
        return True

    def pass_(self, player: Player) -> bool:
        if self.winner is not None:
            self.status_message = "Game is over"
            return False
        if player != self.get_current_player():
            self.status_message = "Not your turn"
            return False
        if self.last_play is None:
            self.status_message = "Cannot pass on an empty table"
            return False

        self.pass_count += 1
        self.status_message = f"{player.name} passed"
        self.next_turn()
        self.check_round_reset()
        return True

    def next_turn(self) -> None:
        self.current_player = (self.current_player + 1) % len(self.players)

    def check_round_reset(self) -> None:
        if self.pass_count >= 3:
            self.last_play = None
            self.pass_count = 0
            self.round_number += 1
            self.status_message = "Round reset: free lead"

    def check_winner(self) -> Optional[Player]:
        if self.winner is not None:
            return self.winner
        for player in self.players:
            if len(player.hand) == 0:
                self.winner = player
                return player
        return None

    def is_game_over(self) -> bool:
        return self.check_winner() is not None

    def ai_turn(self) -> bool:
        player = self.get_current_player()
        if not player.is_ai:
            return False

        last_cards = self.last_play[0] if self.last_play else None
        valid_plays = HandFinder.get_all_valid_plays(
            player.hand,
            last_cards,
            require_three_clubs=(self.first_turn_required and self.last_play is None),
        )
        best = AIStrategy.select_best(
            valid_plays,
            player.hand,
            is_first=(self.first_turn_required and self.last_play is None),
        )
        if best is None:
            return self.pass_(player)
        return self.play(player, best)
