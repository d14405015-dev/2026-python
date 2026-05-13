"""
========================================================
題目：UVA 10922 — 2 the 9s
來源：ZeroJudge a915
========================================================

【測試檔說明】
  本檔同時測試三種解答：
    1. solution_10922.py      — 標準版（英文變數名、型別提示）
    2. solution_10922-easy.py — 簡易好記版（中文變數名、步驟式寫法）

  兩版共用同一組測試案例，透過 TestStandard 與 TestEasy
  兩個 TestCase 類別分別驗證，確保結果一致。

【核心概念】
  - 不斷對各位數字加總，直到只剩 1 位數
  - 若最終為 9，該數是 9 的倍數，輸出加總次數（深度）
  - 否則不是 9 的倍數，輸出相應提示
"""

import unittest
import importlib.util
import os

# ──────────────────────────────────────────────────────
# 動態載入解答模組
# （solution_10922-easy.py 檔名含連字號，需用 importlib 載入）
# ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename: str, module_name: str):
    """從指定路徑載入 Python 模組並回傳模組物件。"""
    path = os.path.join(BASE_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_std  = _load_module("solution_10922.py",      "solution_10922")
_easy = _load_module("solution_10922-easy.py", "solution_10922_easy")

solve_std  = _std.solve    # 標準版
solve_easy = _easy.solve   # 簡易好記版


# ──────────────────────────────────────────────────────
# 共用測試案例 Mixin（標準版與簡易版與手打版共用）
# ──────────────────────────────────────────────────────
class _SharedCases:
    """
    共用測試用例基類。
    子類需定義 `solve_func` 屬性，指向特定版本的求解函式。
    """

    # ── 不是 9 的倍數 ─────────────────────────────────

    def test_not_multiple_1(self):
        """1 不是 9 的倍數"""
        self.assertEqual(self.solve_func("1"), "1 is not a multiple of 9.")

    def test_not_multiple_10(self):
        """10 不是 9 的倍數"""
        self.assertEqual(self.solve_func("10"), "10 is not a multiple of 9.")

    def test_not_multiple_11(self):
        """11 不是 9 的倍數（1+1=2）"""
        self.assertEqual(self.solve_func("11"), "11 is not a multiple of 9.")

    def test_not_multiple_100(self):
        """100 不是 9 的倍數（1+0+0=1）"""
        self.assertEqual(self.solve_func("100"), "100 is not a multiple of 9.")

    def test_not_multiple_8(self):
        """8 不是 9 的倍數"""
        self.assertEqual(self.solve_func("8"), "8 is not a multiple of 9.")

    # ── 是 9 的倍數：深度為 1 ─────────────────────────

    def test_degree1_nine(self):
        """9 本身：加總 0 次就是 1 位數且等於 9 → 深度 0"""
        # 注意：原數本身已經是 1 位數，while 迴圈不執行，depth=0
        self.assertEqual(self.solve_func("9"), "9-degree of 9 is 0.")

    def test_degree1_eighteen(self):
        """18：1+8=9（1 次）→ 深度 1"""
        self.assertEqual(self.solve_func("18"), "9-degree of 18 is 1.")

    def test_degree1_81(self):
        """81：8+1=9（1 次）→ 深度 1"""
        self.assertEqual(self.solve_func("81"), "9-degree of 81 is 1.")

    def test_degree1_27(self):
        """27：2+7=9（1 次）→ 深度 1"""
        self.assertEqual(self.solve_func("27"), "9-degree of 27 is 1.")

    def test_degree1_36(self):
        """36：3+6=9（1 次）→ 深度 1"""
        self.assertEqual(self.solve_func("36"), "9-degree of 36 is 1.")

    # ── 是 9 的倍數：深度為 2 ─────────────────────────

    def test_degree2_99(self):
        """99：9+9=18（1次）→1+8=9（2次）→ 深度 2"""
        self.assertEqual(self.solve_func("99"), "9-degree of 99 is 2.")

    def test_degree2_189(self):
        """189：1+8+9=18（1次）→1+8=9（2次）→ 深度 2"""
        self.assertEqual(self.solve_func("189"), "9-degree of 189 is 2.")

    def test_degree2_999(self):
        """999：9+9+9=27（1次）→2+7=9（2次）→ 深度 2"""
        self.assertEqual(self.solve_func("999"), "9-degree of 999 is 2.")

    def test_degree2_9999(self):
        """9999：9+9+9+9=36（1次）→3+6=9（2次）→ 深度 2"""
        self.assertEqual(self.solve_func("9999"), "9-degree of 9999 is 2.")

    # ── 大數試驗 ────────────────────────────────────────

    def test_degree2_large_nines(self):
        """18 個 9：162（1次）→1+6+2=9（2次）→ 深度 2"""
        n = "9" * 18
        self.assertEqual(self.solve_func(n), f"9-degree of {n} is 2.")

    def test_not_multiple_large(self):
        """大數非倍數：'1' + '0'*99，各位和 = 1"""
        n = "1" + "0" * 99
        self.assertEqual(self.solve_func(n), f"{n} is not a multiple of 9.")

    def test_large_multiple_1296(self):
        """1296（9 的 4 倍）：1+2+9+6=18（1次）→1+8=9（2次）→ 深度 2"""
        self.assertEqual(self.solve_func("1296"), "9-degree of 1296 is 2.")

    # ── 邊界與特例 ────────────────────────────────────

    def test_zero_not_multiple(self):
        """0 不是 9 的倍數（按題意理解）"""
        self.assertEqual(self.solve_func("0"), "0 is not a multiple of 9.")

    def test_single_nine(self):
        """單一 9（最小的 9 倍數）"""
        self.assertEqual(self.solve_func("9"), "9-degree of 9 is 0.")

    # ── 批次模擬 ──────────────────────────────────────

    def test_batch_mixed(self):
        """模擬多行輸入批次處理"""
        cases = ["18", "1", "9", "99", "10"]
        expected = [
            "9-degree of 18 is 1.",
            "1 is not a multiple of 9.",
            "9-degree of 9 is 0.",
            "9-degree of 99 is 2.",
            "10 is not a multiple of 9.",
        ]
        results = [self.solve_func(c) for c in cases]
        self.assertEqual(results, expected)


# ──────────────────────────────────────────────────────
# 測試類別：標準版、簡易版、手打版
# ──────────────────────────────────────────────────────

class TestStandard(unittest.TestCase, _SharedCases):
    """測試標準版解答（英文變數名、型別提示）"""
    def setUp(self):
        self.solve_func = solve_std


class TestEasy(unittest.TestCase, _SharedCases):
    """測試簡易好記版解答（中文變數名、步驟式寫法）"""
    def setUp(self):
        self.solve_func = solve_easy


class TestHandwrite(unittest.TestCase, _SharedCases):
    """測試手打版解答（無任何註解）"""
    def setUp(self):
        # 先嘗試載入 handwrite 版本
        try:
            _handwrite = _load_module("solution_10922-handwrite.py", "solution_10922_handwrite")
            self.solve_func = _handwrite.solve
        except Exception:
            # 若手打版不存在，暫時跳過此測試
            self.skipTest("solution_10922-handwrite.py 尚未建立")


class TestThe9s(unittest.TestCase, _SharedCases):
    """
    相容性測試類別（保留原名稱以支持舊版測試調用）
    預設使用標準版解答
    """
    def setUp(self):
        self.solve_func = solve_std


# ──────────────────────────────────────────────────────
# 執行入口
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # verbosity=2：逐條顯示每個測試方法名稱與 ok / FAIL 結果
    unittest.main(verbosity=2)
