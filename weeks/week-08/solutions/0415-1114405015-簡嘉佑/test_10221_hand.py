import importlib.util
import math
import pathlib
import re
import subprocess
import sys
import unittest


class TestUVA10221HandVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10221-hand.py"

    def run_solver(self, input_data: str) -> str:
        if not self.solution_path.exists():
            self.fail(f"Missing file: {self.solution_path.name}")

        spec = importlib.util.spec_from_file_location("solution_10221_hand", self.solution_path)
        if spec is None or spec.loader is None:
            self.fail("Cannot load solution file.")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "solve") and callable(module.solve):
            result = module.solve(input_data)
            self.assertIsInstance(result, str)
            return result

        completed = subprocess.run(
            [sys.executable, str(self.solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            self.fail(
                "Program failed.\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            )
        return completed.stdout

    @staticmethod
    def expected_arc_chord(s: int, a: int, unit: str) -> tuple[float, float]:
        r = 6440.0 + float(s)
        angle_deg = float(a)
        if unit == "min":
            angle_deg /= 60.0
        if angle_deg > 180.0:
            angle_deg = 360.0 - angle_deg

        theta = math.radians(angle_deg)
        arc = r * theta
        chord = 2.0 * r * math.sin(theta / 2.0)
        return arc, chord

    @staticmethod
    def parse_output_lines(output: str) -> list[tuple[float, float]]:
        lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
        parsed = []

        for line in lines:
            parts = line.split()
            if len(parts) != 2:
                raise AssertionError(f"Each line must have 2 values, got: {line}")

            if not re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", parts[0]):
                raise AssertionError(f"Invalid number: {parts[0]}")
            if not re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", parts[1]):
                raise AssertionError(f"Invalid number: {parts[1]}")

            parsed.append((float(parts[0]), float(parts[1])))

        return parsed

    def assert_case(self, s: int, a: int, unit: str, tol: float = 1e-5):
        output_rows = self.parse_output_lines(self.run_solver(f"{s} {a} {unit}\n"))
        self.assertEqual(len(output_rows), 1)

        actual_arc, actual_chord = output_rows[0]
        exp_arc, exp_chord = self.expected_arc_chord(s, a, unit)

        self.assertAlmostEqual(actual_arc, exp_arc, delta=tol)
        self.assertAlmostEqual(actual_chord, exp_chord, delta=tol)

    def test_zero_angle(self):
        self.assert_case(0, 0, "deg")

    def test_straight_angle(self):
        self.assert_case(0, 180, "deg")

    def test_over_180_degree(self):
        self.assert_case(100, 300, "deg")

    def test_minute_unit(self):
        self.assert_case(500, 60, "min")
        self.assert_case(500, 1, "deg")

        out1 = self.parse_output_lines(self.run_solver("500 60 min\n"))[0]
        out2 = self.parse_output_lines(self.run_solver("500 1 deg\n"))[0]
        self.assertAlmostEqual(out1[0], out2[0], delta=1e-5)
        self.assertAlmostEqual(out1[1], out2[1], delta=1e-5)

    def test_multiple_lines_input(self):
        input_data = """\
500 30 deg
700 60 min
200 45 deg
"""
        rows = self.parse_output_lines(self.run_solver(input_data))
        self.assertEqual(len(rows), 3)

        cases = [(500, 30, "deg"), (700, 60, "min"), (200, 45, "deg")]
        for i, (s, a, unit) in enumerate(cases):
            exp_arc, exp_chord = self.expected_arc_chord(s, a, unit)
            self.assertAlmostEqual(rows[i][0], exp_arc, delta=1e-5)
            self.assertAlmostEqual(rows[i][1], exp_chord, delta=1e-5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
