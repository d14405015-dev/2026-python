import importlib.util
import pathlib
import subprocess
import sys
import unittest


class TestUVA10189HandVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10189-hand.py"

    def run_solver(self, input_data: str) -> str:
        if not self.solution_path.exists():
            self.fail(f"Missing file: {self.solution_path.name}")

        spec = importlib.util.spec_from_file_location("solution_10189_hand", self.solution_path)
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
    def normalize_output(output: str) -> str:
        lines = [line.rstrip() for line in output.strip().splitlines()]
        return "\n".join(lines)

    def assert_output_equal(self, actual: str, expected: str):
        self.assertEqual(self.normalize_output(actual), self.normalize_output(expected))

    def test_official_sample(self):
        input_data = """\
4 4
*...
....
.*..
....
3 5
**...
.....
.*...
0 0
"""
        expected = """\
Field #1:
*100
2210
1*10
1110

Field #2:
**100
33200
1*100
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_single_mine(self):
        input_data = """\
1 1
*
0 0
"""
        expected = """\
Field #1:
*
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_single_empty(self):
        input_data = """\
1 1
.
0 0
"""
        expected = """\
Field #1:
0
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_all_mines(self):
        input_data = """\
2 3
***
***
0 0
"""
        expected = """\
Field #1:
***
***
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_no_mines(self):
        input_data = """\
2 4
....
....
0 0
"""
        expected = """\
Field #1:
0000
0000
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_multiple_fields_blank_line(self):
        input_data = """\
1 2
*.
2 2
..
.*
0 0
"""
        expected = """\
Field #1:
*1

Field #2:
11
1*
"""
        self.assert_output_equal(self.run_solver(input_data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
