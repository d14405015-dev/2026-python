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
        self.assertIsNotNone(self.game.get_current_player().hand.find_3_clubs())

    def test_one_human_three_ai(self):
        ai_count = sum(1 for p in self.game.players if p.is_ai)
        self.assertEqual(ai_count, 3)

    def test_play_removes_cards(self):
        player = self.game.get_current_player()
        card = player.hand.find_3_clubs() if self.game.last_play is None else player.hand[0]
        before = len(player.hand)
        success = self.game.play(player, [card])
        self.assertTrue(success)
        self.assertEqual(len(player.hand), before - 1)

    def test_pass_increments(self):
        player = self.game.get_current_player()
        self.game.play(player, [player.hand.find_3_clubs()])
        self.game.pass_(self.game.get_current_player())
        self.assertEqual(self.game.pass_count, 1)

    def test_three_passes_resets(self):
        p1 = self.game.get_current_player()
        self.game.play(p1, [p1.hand.find_3_clubs()])
        self.game.pass_(self.game.get_current_player())
        self.game.pass_(self.game.get_current_player())
        self.game.pass_(self.game.get_current_player())
        self.assertIsNone(self.game.last_play)
        self.assertEqual(self.game.pass_count, 0)

    def test_detect_winner(self):
        player = self.game.players[0]
        player.hand.clear()
        winner = self.game.check_winner()
        self.assertEqual(winner, player)


if __name__ == "__main__":
    unittest.main()
