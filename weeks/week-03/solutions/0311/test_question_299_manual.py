"""Unit tests for question_299-manual.py.

This test file validates only the manual implementation,
so the generated log is clearly tied to hand-typed code.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANUAL_SCRIPT = BASE_DIR / "question_299-manual.py"

SAMPLE_INPUT = """3
3
1 3 2
4
4 3 2 1
2
2 1
"""

SAMPLE_EXPECTED_OUTPUT = """Optimal train swapping takes 1 swaps.
Optimal train swapping takes 6 swaps.
Optimal train swapping takes 1 swaps.
"""

EXTRA_CASES = [
    (
        """3
5
1 2 3 4 5
1
1
0

""",
        """Optimal train swapping takes 0 swaps.
Optimal train swapping takes 0 swaps.
Optimal train swapping takes 0 swaps.
""",
    ),
    (
        """1
5
5 1 2 4 3
""",
        """Optimal train swapping takes 5 swaps.
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


class TestManualUVA299(unittest.TestCase):
    def test_manual_script_exists(self) -> None:
        self.assertTrue(MANUAL_SCRIPT.exists(), "question_299-manual.py not found")

    def test_sample_case(self) -> None:
        actual = normalize_output(run_manual(SAMPLE_INPUT))
        expected = normalize_output(SAMPLE_EXPECTED_OUTPUT)
        self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        for case_input, case_expected in EXTRA_CASES:
            with self.subTest(input=case_input.splitlines()[0] if case_input else ""):
                actual = normalize_output(run_manual(case_input))
                expected = normalize_output(case_expected)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
