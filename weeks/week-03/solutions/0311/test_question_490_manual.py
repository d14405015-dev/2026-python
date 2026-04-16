"""Unit tests for question_490-manual.py.

This test file validates only the manual implementation,
so the generated log is clearly tied to hand-typed code.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANUAL_SCRIPT = BASE_DIR / "question_490-manual.py"

SAMPLE_INPUT = """HELLO
WORLD
"""

SAMPLE_EXPECTED_OUTPUT = """WH
OE
RL
LL
DO
"""

EXTRA_CASES = [
    (
        """ABC
DE
F
""",
        """FDA
 EB
  C
""",
    ),
    (
        """A B!
xy
""",
        """xA
y 
 B
 !
""",
    ),
]


def normalize_newline(text: str) -> str:
    return text.replace("\r\n", "\n")


def run_manual(input_data: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(MANUAL_SCRIPT)],
        input=input_data,
        text=True,
        capture_output=True,
        cwd=str(BASE_DIR),
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"Manual script failed with code {completed.returncode}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed.stdout


class TestManualUVA490(unittest.TestCase):
    def test_manual_script_exists(self) -> None:
        self.assertTrue(MANUAL_SCRIPT.exists(), "question_490-manual.py not found")

    def test_sample_case(self) -> None:
        actual = normalize_newline(run_manual(SAMPLE_INPUT))
        expected = normalize_newline(SAMPLE_EXPECTED_OUTPUT)
        self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        for case_input, case_expected in EXTRA_CASES:
            with self.subTest(input=case_input.splitlines()[0] if case_input else ""):
                actual = normalize_newline(run_manual(case_input))
                expected = normalize_newline(case_expected)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
