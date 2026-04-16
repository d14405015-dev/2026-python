"""Unit tests for question_272-manual.py.

This test file validates only the manual implementation,
so the generated log is clearly tied to hand-typed code.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MANUAL_SCRIPT = BASE_DIR / "question_272-manual.py"

SAMPLE_INPUT = '"To be or not to be," quoth the Bard, "that is the question"\n'
SAMPLE_EXPECTED_OUTPUT = "``To be or not to be,'' quoth the Bard, ``that is the question''\n"

EXTRA_CASES = [
    (
        "She said, \"hello\".\nThen he replied, \"ok\".\n",
        "She said, ``hello''.\nThen he replied, ``ok''.\n",
    ),
    (
        "No quote here.\nKeep everything unchanged.\n",
        "No quote here.\nKeep everything unchanged.\n",
    ),
]


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


class TestManualUVA272(unittest.TestCase):
    def test_manual_script_exists(self) -> None:
        self.assertTrue(MANUAL_SCRIPT.exists(), "question_272-manual.py not found")

    def test_sample_case(self) -> None:
        actual = run_manual(SAMPLE_INPUT)
        self.assertEqual(actual, SAMPLE_EXPECTED_OUTPUT)

    def test_extra_cases(self) -> None:
        for case_input, case_expected in EXTRA_CASES:
            with self.subTest(input=case_input.splitlines()[0] if case_input else ""):
                actual = run_manual(case_input)
                self.assertEqual(actual, case_expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
