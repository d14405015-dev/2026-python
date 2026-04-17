import unittest

from game.game import BigTwoGame
from game.models import Card


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = BigTwoGame()
        self.game.setup()

    def test_game_has_4_players(self):
        self.assertEqual(len(self.game.players), 4)

    def test_each_player_13_cards(self):
        self.assertTrue(all(len(p.hand) == 13 for p in self.game.players))

    def test_total_cards_distributed(self):
        total = sum(len(p.hand) for p in self.game.players)
        self.assertEqual(total, 52)

    def test_first_player_has_3_clubs(self):
        self.assertIn(Card(3, 0), self.game.get_current_player().hand)

    def test_play_removes_cards(self):
        player = self.game.get_current_player()
        before = len(player.hand)
        ok = self.game.play(player, [Card(3, 0)])
        self.assertTrue(ok)
        self.assertEqual(len(player.hand), before - 1)

    def test_play_sets_last_play(self):
        player = self.game.get_current_player()
        self.game.play(player, [Card(3, 0)])
        self.assertIsNotNone(self.game.last_play)

    def test_invalid_play(self):
        player = self.game.get_current_player()
        self.assertFalse(self.game.play(player, [Card(15, 3)]))

    def test_pass_increments(self):
        player = self.game.get_current_player()
        self.game.play(player, [Card(3, 0)])
        self.game.next_turn()
        p2 = self.game.get_current_player()
        self.assertTrue(self.game.pass_(p2))
        self.assertEqual(self.game.pass_count, 1)

    def test_three_passes_resets(self):
        player = self.game.get_current_player()
        self.game.play(player, [Card(3, 0)])
        for _ in range(3):
            self.game.next_turn()
            self.game.pass_(self.game.get_current_player())
        self.game.check_round_reset()
        self.assertIsNone(self.game.last_play)

    def test_turn_rotates(self):
        now = self.game.current_player
        self.game.next_turn()
        self.assertEqual(self.game.current_player, (now + 1) % 4)

    def test_detect_winner(self):
        player = self.game.players[0]
        player.hand.clear()
        winner = self.game.check_winner()
        self.assertEqual(winner, player)


if __name__ == "__main__":
    unittest.main()
