import importlib.util
import pathlib
import subprocess
import sys
import unittest


class TestUVA10190HandVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10190-hand.py"

    def run_solver(self, input_data: str) -> str:
        if not self.solution_path.exists():
            self.fail(f"Missing file: {self.solution_path.name}")

        spec = importlib.util.spec_from_file_location("solution_10190_hand", self.solution_path)
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

    def parse_output_value(self, output: str) -> float:
        text = output.strip()
        self.assertRegex(text, r"^-?\d+\.\d{2}$")
        return float(text)

    def assert_volume(self, input_data: str, expected: float):
        actual = self.parse_output_value(self.run_solver(input_data))
        self.assertAlmostEqual(actual, expected, places=2)

    def test_no_umbrella(self):
        self.assert_volume("0 10 5 3\n", 150.00)

    def test_single_stationary(self):
        self.assert_volume("1 10 5 2\n2 4 0\n", 60.00)

    def test_two_non_overlapping(self):
        self.assert_volume("2 10 4 1\n0 3 0\n6 2 0\n", 20.00)

    def test_two_overlapping(self):
        self.assert_volume("2 10 3 2\n1 5 0\n4 4 0\n", 18.00)

    def test_full_coverage(self):
        self.assert_volume("2 10 7 5\n0 4 0\n4 6 0\n", 0.00)

    def test_single_moving(self):
        self.assert_volume("1 10 5 3\n2 4 1\n", 90.00)


if __name__ == "__main__":
    unittest.main(verbosity=2)
