import unittest

from robot_core import run_instructions


class TestRobotScent(unittest.TestCase):
    def test_first_lost_leaves_scent(self):
        scents = set()
        state = run_instructions(5, 3, "N", "F", 5, 3, scents)
        self.assertTrue(state.lost)
        self.assertIn((5, 3, "N"), scents)

    def test_second_robot_ignores_same_dangerous_forward(self):
        scents = set()
        run_instructions(5, 3, "N", "F", 5, 3, scents)
        state2 = run_instructions(5, 3, "N", "F", 5, 3, scents)
        self.assertFalse(state2.lost)
        self.assertEqual((state2.x, state2.y, state2.direction), (5, 3, "N"))

    def test_same_cell_different_direction_not_shared(self):
        scents = set()
        run_instructions(5, 3, "N", "F", 5, 3, scents)
        # 同座標但不同方向不共用 scent，向東前進仍會越界並 LOST
        state = run_instructions(5, 3, "E", "F", 5, 3, scents)
        self.assertTrue(state.lost)
        self.assertEqual((state.x, state.y, state.direction), (5, 3, "E"))

    def test_scent_allows_following_commands(self):
        scents = set()
        run_instructions(5, 3, "N", "F", 5, 3, scents)
        # 第一個 F 因 scent 被忽略，仍會繼續執行後續指令。
        # 接著 R 轉向 E，再 F 越界，最終 LOST。
        state = run_instructions(5, 3, "N", "FRF", 5, 3, scents)
        self.assertTrue(state.lost)
        self.assertEqual((state.x, state.y, state.direction), (5, 3, "E"))

    def test_scent_key_contains_direction(self):
        scents = set()
        run_instructions(0, 3, "W", "F", 5, 3, scents)
        self.assertIn((0, 3, "W"), scents)
        self.assertNotIn((0, 3, "N"), scents)


if __name__ == "__main__":
    unittest.main()
