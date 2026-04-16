"""Unit tests for question_100-manual.py.

This test file targets only the manual version so the test log
is clearly tied to the hand-typed submission.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANUAL_SCRIPT = BASE_DIR / "question_100-manual.py"

SAMPLE_INPUT = """1 10
100 200
201 210
900 1000
"""

SAMPLE_EXPECTED_OUTPUT = """1 10 20
100 200 125
201 210 89
900 1000 174
"""

EXTRA_CASES = [
    ("1 1\n", "1 1 1\n"),
    ("10 1\n", "10 1 20\n"),
]


def normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


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


class TestManualUVA100(unittest.TestCase):
    def test_manual_script_exists(self) -> None:
        self.assertTrue(MANUAL_SCRIPT.exists(), "question_100-manual.py not found")

    def test_sample_cases(self) -> None:
        actual = normalize_output(run_manual(SAMPLE_INPUT))
        expected = normalize_output(SAMPLE_EXPECTED_OUTPUT)
        self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        for case_input, case_expected in EXTRA_CASES:
            with self.subTest(input=case_input.strip()):
                actual = normalize_output(run_manual(case_input))
                expected = normalize_output(case_expected)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
