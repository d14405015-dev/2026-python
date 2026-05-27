"""UVA 11417 的單元測試。

此檔同時測試：
- 標準版 question_11417.py
- 好記版 question_11417-easy.py

兩個版本都必須通過相同測資，確保行為一致。
"""

from __future__ import annotations

import importlib.util
import pathlib
import unittest

BASE_DIR = pathlib.Path(__file__).resolve().parent


def load_module(filename: str, module_name: str):
    """從檔案路徑動態載入模組。

    這樣可支援檔名帶有連字號（-）的 easy 版本。
    """
    path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"無法載入模組: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "standard": load_module("question_11417.py", "q11417_standard"),
    "easy": load_module("question_11417-easy.py", "q11417_easy"),
}


class TestUVA11417(unittest.TestCase):
    """針對 UVA 11417 的題意案例與邊界案例測試。"""

    def test_sample_case(self):
        data = "10\n100\n500\n0\n"
        expected = "67\n13015\n442011"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)

    def test_small_values(self):
        data = "2\n3\n0\n"
        # G(2)=gcd(1,2)=1；G(3)=1+1+1=3
        expected = "1\n3"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.solve(data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
