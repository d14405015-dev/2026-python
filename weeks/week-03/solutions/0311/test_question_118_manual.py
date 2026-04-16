"""Unit tests for question_118-manual.py.

This test file validates only the manual implementation,
so the generated log is clearly tied to hand-typed code.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANUAL_SCRIPT = BASE_DIR / "question_118-manual.py"

SAMPLE_INPUT = """5 3
1 1 E
RFRFRFRF
3 2 N
FRRFLLFFRRFLL
0 3 W
LLFFFLFLFL
"""

SAMPLE_EXPECTED_OUTPUT = """1 1 E
3 3 N LOST
2 3 S
"""

EXTRA_CASES = [
    (
        """1 1
1 1 E
F
1 1 E
F
""",
        """1 1 E LOST
1 1 E
""",
    ),
    (
        """2 2
0 0 N
RFFLFF
""",
        """2 2 N
""",
    ),
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


class TestManualUVA118(unittest.TestCase):
    def test_manual_script_exists(self) -> None:
        self.assertTrue(MANUAL_SCRIPT.exists(), "question_118-manual.py not found")

    def test_sample_case(self) -> None:
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
