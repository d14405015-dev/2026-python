"""UVA 12019 的單元測試。"""

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
    "standard": load_module("question_12019.py", "q12019_standard"),
    "easy": load_module("question_12019-easy.py", "q12019_easy"),
}


class TestUVA12019(unittest.TestCase):
    """測試 2012 年各日期的星期計算是否正確。"""

    def test_known_dates(self):
        data = "5\n1 1\n2 29\n4 4\n10 10\n12 31\n"
        expected = "Sunday\nWednesday\nWednesday\nWednesday\nMonday"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)

    def test_single_query(self):
        data = "1\n7 4\n"
        expected = "Wednesday"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
