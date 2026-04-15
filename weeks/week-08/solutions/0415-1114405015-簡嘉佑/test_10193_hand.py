import importlib.util
import math
import pathlib
import re
import subprocess
import sys
import unittest


class TestUVA10193HandVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10193-hand.py"

    def run_solver(self, input_data: str) -> str:
        if not self.solution_path.exists():
            self.fail(f"Missing file: {self.solution_path.name}")

        spec = importlib.util.spec_from_file_location("solution_10193_hand", self.solution_path)
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
    def parse_output_value(output: str) -> int:
        text = output.strip()
        if not re.fullmatch(r"-?\d+", text):
            raise AssertionError(f"Output must be an integer, got: {text}")
        return int(text)

    @staticmethod
    def expected_min_sum(a: int) -> int:
        n = a * a + 1
        best = 10**30
        root = math.isqrt(n)
        for d in range(1, root + 1):
            if n % d == 0:
                e = n // d
                best = min(best, 2 * a + d + e)
        return best

    def assert_answer(self, a: int, expected: int):
        actual = self.parse_output_value(self.run_solver(f"{a}\n"))
        self.assertEqual(actual, expected)

    def test_a_1(self):
        self.assert_answer(1, 5)

    def test_a_3(self):
        self.assert_answer(3, 13)

    def test_a_7(self):
        self.assert_answer(7, 29)

    def test_a_8(self):
        self.assert_answer(8, 34)

    def test_a_10(self):
        self.assert_answer(10, 122)

    def test_small_range_exhaustive(self):
        for a in range(1, 51):
            expected = self.expected_min_sum(a)
            actual = self.parse_output_value(self.run_solver(f"{a}\n"))
            self.assertEqual(actual, expected, f"wrong answer at a={a}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
