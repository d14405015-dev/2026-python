import importlib.util
import pathlib
import subprocess
import sys
import unittest


class TestUVA10222HandVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10222-hand.py"
        cls.rows = [
            "`1234567890-=",
            "qwertyuiop[]\\",
            "asdfghjkl;'",
            "zxcvbnm,./",
        ]

    def run_solver(self, input_data: str) -> str:
        if not self.solution_path.exists():
            self.fail(f"Missing file: {self.solution_path.name}")

        spec = importlib.util.spec_from_file_location("solution_10222_hand", self.solution_path)
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

    def expected_decode(self, text: str) -> str:
        out = []

        for ch in text:
            if ch == "\n":
                out.append(ch)
                continue

            lowered = ch.lower()
            replaced = False
            for row in self.rows:
                idx = row.find(lowered)
                if idx >= 2:
                    out.append(row[idx - 2])
                    replaced = True
                    break

            if not replaced:
                out.append(ch)

        return "".join(out)

    def assert_decoded(self, input_data: str):
        actual = self.run_solver(input_data)
        expected = self.expected_decode(input_data)
        self.assertEqual(actual.rstrip("\n"), expected.rstrip("\n"))

    def test_single_char_example(self):
        self.assert_decoded("r\n")

    def test_letters_symbols_and_space(self):
        self.assert_decoded("jr;;p ypw;f [t ept;f!\n")

    def test_numbers_and_punctuation(self):
        self.assert_decoded("34567890-= []\\ ;' ,./\n")

    def test_multi_line_input(self):
        self.assert_decoded("r\nqwerty\n12345\n")

    def test_keep_unmapped_chars(self):
        self.assert_decoded("r! t?\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
