import unittest

from robot_core import (
    RobotState,
    in_bounds,
    run_instructions,
    state_text,
    turn_left,
    turn_right,
)


class TestRobotCore(unittest.TestCase):
    def test_turn_left_from_north(self):
        self.assertEqual(turn_left("N"), "W")

    def test_turn_right_from_north(self):
        self.assertEqual(turn_right("N"), "E")

    def test_turn_right_four_times_back_to_origin(self):
        d = "N"
        for _ in range(4):
            d = turn_right(d)
        self.assertEqual(d, "N")

    def test_forward_move_inside_bounds(self):
        scents = set()
        state = run_instructions(1, 1, "E", "F", 5, 3, scents)
        self.assertEqual((state.x, state.y, state.direction, state.lost), (2, 1, "E", False))

    def test_forward_out_of_bounds_becomes_lost(self):
        scents = set()
        state = run_instructions(5, 3, "N", "F", 5, 3, scents)
        self.assertTrue(state.lost)
        self.assertEqual(state_text(state), "5 3 N LOST")

    def test_lost_robot_stops_remaining_commands(self):
        scents = set()
        state = run_instructions(5, 3, "N", "FFRFF", 5, 3, scents)
        self.assertEqual((state.x, state.y, state.direction, state.lost), (5, 3, "N", True))

    def test_invalid_command_raises(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_instructions(0, 0, "N", "FX", 5, 3, scents)

    def test_invalid_start_direction_raises(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_instructions(0, 0, "A", "F", 5, 3, scents)

    def test_invalid_start_position_raises(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_instructions(6, 0, "N", "F", 5, 3, scents)

    def test_in_bounds_helper(self):
        self.assertTrue(in_bounds(0, 0, 5, 3))
        self.assertTrue(in_bounds(5, 3, 5, 3))
        self.assertFalse(in_bounds(6, 3, 5, 3))


if __name__ == "__main__":
    unittest.main()
