"""UVA 11461 的單元測試。"""

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
    "standard": load_module("question_11461.py", "q11461_standard"),
    "easy": load_module("question_11461-easy.py", "q11461_easy"),
}


class TestUVA11461(unittest.TestCase):
    """測試區間內完全平方數數量。"""

    def test_sample_case(self):
        data = "1 4\n1 10\n1 100000\n0 0\n"
        expected = "2\n3\n316"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)

    def test_edge_case(self):
        data = "2 3\n4 4\n15 15\n0 0\n"
        expected = "0\n1\n0"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
