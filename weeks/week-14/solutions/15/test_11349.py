"""UVA 11349 的單元測試。"""

from __future__ import annotations

import importlib.util
import pathlib
import unittest

BASE_DIR = pathlib.Path(__file__).resolve().parent


def load_module(filename: str, module_name: str):
    path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"無法載入模組: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "standard": load_module("question_11349.py", "q11349_standard"),
    "easy": load_module("question_11349-easy.py", "q11349_easy"),
}


class TestUVA11349(unittest.TestCase):
    """測試中心對稱與非負條件。"""

    def test_sample_case(self):
        data = (
            "2\n"
            "N = 3\n"
            "5 1 3\n"
            "2 0 2\n"
            "3 1 5\n"
            "N = 3\n"
            "5 1 3\n"
            "2 0 2\n"
            "0 1 5\n"
        )
        expected = "Test #1: Symmetric.\nTest #2: Non-symmetric."

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)

    def test_negative_values_and_single_cell(self):
        data = (
            "2\n"
            "N = 1\n"
            "0\n"
            "N = 2\n"
            "1 2\n"
            "-2 1\n"
        )
        expected = "Test #1: Symmetric.\nTest #2: Non-symmetric."

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
