"""
========================================================
題目：UVA 10908 — Largest Square
來源：ZeroJudge a901
========================================================

【測試檔說明】
  本檔同時測試三種解答：
    1. solution_10908.py           — 標準版（英文變數名、型別提示）
    2. solution_10908-easy.py      — 簡易好記版（中文變數名、步驟式寫法）
    3. solution_10908-handwrite.py — 手打版（無任何註解，乾淨程式碼）

  三版共用同一組測試案例，透過 TestStandard、TestEasy、TestHandwrite
  三個 TestCase 類別分別驗證，確保結果一致。

【測試分類】
  - 官方範例查詢：直接對應題目給的 4 個查詢
  - 邊界限制    ：角落、邊界，無法擴張 → 邊長 1
  - 全相同網格  ：驗證最大擴張能力
  - 異色棋盤    ：完全無法擴張
  - 完整案例輸出：驗證標頭格式與多查詢行數
"""

import unittest
import importlib.util
import os

# ──────────────────────────────────────────────────────
# 動態載入解答模組
# （solution_10908-easy.py 檔名含連字號，需用 importlib 載入）
# ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename: str, module_name: str):
    """從指定路徑載入 Python 模組並回傳模組物件。"""
    path = os.path.join(BASE_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_std       = _load_module("solution_10908.py",           "solution_10908")
_easy      = _load_module("solution_10908-easy.py",      "solution_10908_easy")
_handwrite = _load_module("solution_10908-handwrite.py", "solution_10908_handwrite")

solve_query_std       = _std.solve_query        # 標準版
solve_query_easy      = _easy.solve_query       # 簡易好記版
solve_query_handwrite = _handwrite.solve_query  # 手打版（無任何註解）


# ──────────────────────────────────────────────────────
# 共用輔助函式（測試用，組合完整案例輸出字串）
# ──────────────────────────────────────────────────────
def make_case_output(solve_fn, m, n, q, grid, queries):
    """
    用指定的 solve_query 函式處理一個完整案例，
    回傳 'M N Q\\n答案1\\n答案2...' 格式的字串。
    """
    lines = [f"{m} {n} {q}"]
    for r, c in queries:
        lines.append(str(solve_fn(grid, r, c)))
    return "\n".join(lines)


# ──────────────────────────────────────────────────────
# 共用測試案例 Mixin（標準版與簡易版共用）
# ──────────────────────────────────────────────────────
class _SharedCases:
    """子類別須設定 self.fn 為受測的 solve_query 函式。"""

    OFFICIAL_GRID = [
        "abbbaaaaaa",
        "abbbaaaaaa",
        "abbbaaaaaa",
        "aaaaaaaaaa",
        "aaaaaaaaaa",
        "aaccaaaaaa",
        "aaccaaaaaa",
    ]

    # ── 官方範例查詢 ──────────────────────────────────

    def test_01_official_q1(self):
        """中心 (1,2)：3×3 全是 'b' → 邊長 3"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 1, 2), 3)

    def test_02_official_q2(self):
        """中心 (2,4)：鄰格有 'b' → 邊長 1"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 2, 4), 1)

    def test_03_official_q3(self):
        """中心 (4,6)：5×5 全是 'a' → 邊長 5"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 4, 6), 5)

    def test_04_official_q4(self):
        """中心 (5,2)：鄰格有 'a' → 邊長 1"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 5, 2), 1)

    # ── 邊界限制 ──────────────────────────────────────

    def test_05_corner_top_left(self):
        """左上角 (0,0)：無法往上/左擴張 → 邊長 1"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 0, 0), 1)

    def test_06_right_edge(self):
        """右邊界 (4,9)：無法往右擴張 → 邊長 1"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 4, 9), 1)

    def test_07_bottom_edge(self):
        """下邊界 (6,7)：無法往下擴張 → 邊長 1"""
        self.assertEqual(self.fn(self.OFFICIAL_GRID, 6, 7), 1)

    # ── 全相同網格 ────────────────────────────────────

    def test_08_single_cell(self):
        """1×1 網格 → 邊長 1"""
        self.assertEqual(self.fn(["x"], 0, 0), 1)

    def test_09_all_same_3x3_center(self):
        """3×3 全相同，中心 (1,1) → 邊長 3"""
        self.assertEqual(self.fn(["aaa","aaa","aaa"], 1, 1), 3)

    def test_10_all_same_5x5_center(self):
        """5×5 全相同，中心 (2,2) → 邊長 5"""
        self.assertEqual(self.fn(["aaaaa"]*5, 2, 2), 5)

    def test_11_all_same_5x5_off_center(self):
        """5×5 全相同，中心 (1,1)，上/左限制 → 邊長 3"""
        self.assertEqual(self.fn(["aaaaa"]*5, 1, 1), 3)

    def test_12_single_row(self):
        """1×5 單行，縱向無法擴張 → 邊長 1"""
        self.assertEqual(self.fn(["zzzzz"], 0, 2), 1)

    # ── 異色棋盤 ──────────────────────────────────────

    def test_13_checkerboard(self):
        """3×3 棋盤格，中心字元彼此相鄰不同 → 邊長 1"""
        self.assertEqual(self.fn(["aba","bab","aba"], 1, 1), 1)

    # ── 完整案例輸出格式 ──────────────────────────────

    def test_14_official_full_output(self):
        """官方範例完整輸出：標頭 + 4 個查詢答案"""
        result = make_case_output(
            self.fn, 7, 10, 4, self.OFFICIAL_GRID,
            [(1,2),(2,4),(4,6),(5,2)]
        )
        self.assertEqual(result, "7 10 4\n3\n1\n5\n1")

    def test_15_header_format(self):
        """確認標頭格式為 'M N Q'（空格分隔）"""
        result = make_case_output(self.fn, 3, 3, 1, ["aaa","aaa","aaa"], [(1,1)])
        self.assertTrue(result.startswith("3 3 1"))

    def test_16_multiple_queries_line_count(self):
        """4 個查詢 → 輸出共 5 行（標頭 + 4 查詢）"""
        grid = ["aaaaa"] * 5
        result = make_case_output(self.fn, 5, 5, 4, grid, [(2,2),(0,0),(4,4),(2,0)])
        lines = result.split("\n")
        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0], "5 5 4")
        self.assertEqual(lines[1], "5")  # (2,2) 中心完整擴 → 5
        self.assertEqual(lines[2], "1")  # (0,0) 角落 → 1
        self.assertEqual(lines[3], "1")  # (4,4) 角落 → 1
        self.assertEqual(lines[4], "1")  # (2,0) 左邊界 → 1


# ──────────────────────────────────────────────────────
# 標準版測試類別
# ──────────────────────────────────────────────────────
class TestStandard(_SharedCases, unittest.TestCase):
    """測試 solution_10908.py（標準版）"""
    fn = staticmethod(solve_query_std)


# ──────────────────────────────────────────────────────
# 簡易好記版測試類別
# ──────────────────────────────────────────────────────
class TestEasy(_SharedCases, unittest.TestCase):
    """測試 solution_10908-easy.py（簡易好記版）"""
    fn = staticmethod(solve_query_easy)


# ──────────────────────────────────────────────────────
# 手打版測試類別（對應學生自行手打、無任何註解的程式碼）
# ──────────────────────────────────────────────────────
class TestHandwrite(_SharedCases, unittest.TestCase):
    """測試 solution_10908-handwrite.py（手打版，無任何註解）"""
    fn = staticmethod(solve_query_handwrite)


# ──────────────────────────────────────────────────────
# （保留舊版 TestLargestSquare 名稱，改呼叫 import 的標準版函式）
# ──────────────────────────────────────────────────────
class TestLargestSquare(unittest.TestCase):

    OFFICIAL_GRID = [
        "abbbaaaaaa",
        "abbbaaaaaa",
        "abbbaaaaaa",
        "aaaaaaaaaa",
        "aaaaaaaaaa",
        "aaccaaaaaa",
        "aaccaaaaaa",
    ]

    def test_query_center_3x3_block(self):
        """中心 (1,2)：周圍 3×3 全是 'b' → 邊長 3"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 1, 2), 3)

    def test_query_mixed_neighbor(self):
        """中心 (2,4)：周圍立刻出現不同字元 → 邊長 1"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 2, 4), 1)

    def test_query_large_open_area(self):
        """中心 (4,6)：周圍 5×5 全是 'a' → 邊長 5"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 4, 6), 5)

    def test_query_edge_of_block(self):
        """中心 (5,2)：周圍立刻出現 'a' → 邊長 1"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 5, 2), 1)

    def test_query_corner_cell(self):
        """左上角 (0,0)：無法往負方向擴張 → 邊長 1"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 0, 0), 1)

    def test_query_right_edge(self):
        """右邊邊界 (4,9)：不能往右擴張 → 邊長 1"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 4, 9), 1)

    def test_query_bottom_edge(self):
        """下邊邊界 (6,7)：不能往下擴張 → 邊長 1"""
        self.assertEqual(solve_query_std(self.OFFICIAL_GRID, 6, 7), 1)

    def test_single_cell_grid(self):
        """1×1 網格 → 邊長 1"""
        self.assertEqual(solve_query_std(["x"], 0, 0), 1)

    def test_all_same_3x3(self):
        """3×3 全相同，中心 (1,1) → 邊長 3"""
        self.assertEqual(solve_query_std(["aaa","aaa","aaa"], 1, 1), 3)

    def test_all_same_5x5_center(self):
        """5×5 全相同，中心 (2,2) → 邊長 5"""
        self.assertEqual(solve_query_std(["aaaaa"]*5, 2, 2), 5)

    def test_all_same_5x5_off_center(self):
        """5×5 全相同，中心 (1,1)，上/左限制 → 邊長 3"""
        self.assertEqual(solve_query_std(["aaaaa"]*5, 1, 1), 3)

    def test_different_chars_no_expand(self):
        """棋盤格，中心字元無法擴張 → 邊長 1"""
        self.assertEqual(solve_query_std(["aba","bab","aba"], 1, 1), 1)

    def test_official_full_case(self):
        """官方完整輸出驗證"""
        result = make_case_output(
            solve_query_std, 7, 10, 4, self.OFFICIAL_GRID,
            [(1,2),(2,4),(4,6),(5,2)]
        )
        self.assertEqual(result, "7 10 4\n3\n1\n5\n1")

    def test_single_row_grid(self):
        """1×5 單行，縱向無法擴 → 邊長 1"""
        self.assertEqual(solve_query_std(["zzzzz"], 0, 0), 1)

    def test_case_header_format(self):
        """標頭格式為 'M N Q'"""
        result = make_case_output(solve_query_std, 3, 3, 1, ["aaa","aaa","aaa"], [(1,1)])
        self.assertTrue(result.startswith("3 3 1"))

    def test_case_multiple_queries(self):
        """多查詢行數與各查詢結果驗證"""
        grid = ["aaaaa"] * 5
        result = make_case_output(solve_query_std, 5, 5, 4, grid, [(2,2),(0,0),(4,4),(2,0)])
        lines = result.split("\n")
        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0], "5 5 4")
        self.assertEqual(lines[1], "5")
        self.assertEqual(lines[2], "1")
        self.assertEqual(lines[3], "1")
        self.assertEqual(lines[4], "1")


# ──────────────────────────────────────────────────────
# 執行入口
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # verbosity=2：逐條顯示每個測試方法名稱與 ok / FAIL 結果
    unittest.main(verbosity=2)

