"""
========================================================
題目：UVA 10812 — Beat the Spread!
來源：ZeroJudge a805
========================================================

【測試檔說明】
  本檔同時測試三種解答：
    1. solution_10812.py           — 標準版（含型別提示、英文變數名）
    2. solution_10812-easy.py      — 簡易好記版（中文變數名、步驟式寫法）
    3. solution_10812-handwrite.py — 手打版（無任何註解，乾淨程式碼）

  三版共用同一組測試案例，透過 TestStandard、TestEasy、TestHandwrite
  三個 TestCase 類別分別驗證，確保結果一致。

【測試分類】
  - 正常有解：兩隊各有整數得分的情況（10 個案例）
  - 無解     ：差大於和 / 和加差為奇數 / 出現負分（5 個案例）
  - 批次模擬 ：模擬題目多組輸入格式（2 個案例）
"""

import unittest
import importlib.util
import os

# ──────────────────────────────────────────────────────
# 動態載入解答模組
# （因 solution_10812-easy.py 檔名含連字號，無法直接 import，
#   改用 importlib 以絕對路徑載入，確保跨平台相容）
# ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename: str, module_name: str):
    """從指定檔案路徑載入 Python 模組並回傳模組物件。"""
    path = os.path.join(BASE_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# 分別載入三版解答的 solve 函式
_std       = _load_module("solution_10812.py",           "solution_10812")
_easy      = _load_module("solution_10812-easy.py",      "solution_10812_easy")
_handwrite = _load_module("solution_10812-handwrite.py", "solution_10812_handwrite")

solve_std       = _std.solve        # 標準版 solve
solve_easy      = _easy.solve       # 簡易好記版 solve
solve_handwrite = _handwrite.solve  # 手打版 solve（無任何註解）


# ──────────────────────────────────────────────────────
# 共用測試案例 Mixin
# （讓標準版與簡易版共用完全相同的測試內容，避免重複撰寫）
# ──────────────────────────────────────────────────────
class _SharedCases:
    """
    所有測試方法的共用 Mixin。
    子類別須將 self.fn 設為受測的 solve 函式。
    """

    # ── 正常有解的情況 ────────────────────────────────

    def test_01_official_example(self):
        """官方範例：S=40, D=20 → 30 10"""
        self.assertEqual(self.fn(40, 20), "30 10")

    def test_02_tie_game(self):
        """兩隊同分（差為零）：S=10, D=0 → 5 5"""
        self.assertEqual(self.fn(10, 0), "5 5")

    def test_03_one_team_zero(self):
        """其中一隊得零分：S=10, D=10 → 10 0"""
        self.assertEqual(self.fn(10, 10), "10 0")

    def test_04_typical_case(self):
        """一般情況：S=20, D=4 → 12 8"""
        self.assertEqual(self.fn(20, 4), "12 8")

    def test_05_large_values(self):
        """較大數值：S=1000, D=200 → 600 400"""
        self.assertEqual(self.fn(1000, 200), "600 400")

    def test_06_both_zero(self):
        """邊界：S=0, D=0 → 0 0（兩隊皆得零分）"""
        self.assertEqual(self.fn(0, 0), "0 0")

    def test_07_minimal(self):
        """最小有解：S=2, D=0 → 1 1"""
        self.assertEqual(self.fn(2, 0), "1 1")

    def test_08_s_equals_d(self):
        """S 等於 D：S=6, D=6 → 6 0（低分隊恰好得零分）"""
        self.assertEqual(self.fn(6, 6), "6 0")

    def test_09_odd_plus_odd_even(self):
        """S=7, D=3 → (7+3)=10 偶數 → 5 2"""
        self.assertEqual(self.fn(7, 3), "5 2")

    def test_10_small_integers(self):
        """S=3, D=1 → (3+1)=4 偶數 → 2 1"""
        self.assertEqual(self.fn(3, 1), "2 1")

    # ── 無解的情況 ───────────────────────────────────

    def test_11_official_impossible(self):
        """官方範例無解：S=20, D=40 → impossible（差大於和，小分為負）"""
        self.assertEqual(self.fn(20, 40), "impossible")

    def test_12_diff_gt_sum(self):
        """差大於和：S=10, D=20 → impossible"""
        self.assertEqual(self.fn(10, 20), "impossible")

    def test_13_odd_total(self):
        """S+D 為奇數：S=5, D=2 → impossible（無整數解）"""
        self.assertEqual(self.fn(5, 2), "impossible")

    def test_14_both_give_odd_sum(self):
        """S=5, D=4 → (5+4)=9 奇數 → impossible"""
        self.assertEqual(self.fn(5, 4), "impossible")

    def test_15_s_zero_d_nonzero(self):
        """S=0, D=2 → impossible（小分 = (0-2)/2 = -1，為負數）"""
        self.assertEqual(self.fn(0, 2), "impossible")

    # ── 批次模擬（模擬題目多組輸入）────────────────────

    def test_16_batch_official_sample(self):
        """
        官方範例批次輸入：
            第 1 組 40 20 → 30 10
            第 2 組 20 40 → impossible
        """
        cases    = [(40, 20), (20, 40)]
        expected = ["30 10", "impossible"]
        self.assertEqual([self.fn(s, d) for s, d in cases], expected)

    def test_17_batch_mixed(self):
        """
        混合批次：有解與無解交錯出現（共 5 組）
        """
        cases = [
            (10,  0),   # → 5 5
            (10, 20),   # → impossible（差大於和）
            (100, 50),  # → 75 25
            (3,   4),   # → impossible（3+4=7 奇數）
            (0,   0),   # → 0 0
        ]
        expected = ["5 5", "impossible", "75 25", "impossible", "0 0"]
        self.assertEqual([self.fn(s, d) for s, d in cases], expected)


# ──────────────────────────────────────────────────────
# 標準版測試類別
# ──────────────────────────────────────────────────────
class TestStandard(_SharedCases, unittest.TestCase):
    """測試 solution_10812.py（標準版）"""
    fn = staticmethod(solve_std)


# ──────────────────────────────────────────────────────
# 簡易好記版測試類別
# ──────────────────────────────────────────────────────
class TestEasy(_SharedCases, unittest.TestCase):
    """測試 solution_10812-easy.py（簡易好記版）"""
    fn = staticmethod(solve_easy)


# ──────────────────────────────────────────────────────
# 手打版測試類別（對應學生自行手打、無任何註解的程式碼）
# ──────────────────────────────────────────────────────
class TestHandwrite(_SharedCases, unittest.TestCase):
    """測試 solution_10812-handwrite.py（手打版，無任何註解）"""
    fn = staticmethod(solve_handwrite)


# ──────────────────────────────────────────────────────
# 執行入口
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # verbosity=2：逐條顯示每個測試方法名稱與 ok / FAIL 結果
    unittest.main(verbosity=2)
