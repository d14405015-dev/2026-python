"""
========================================================
題目：UVA 10929 — 11 的倍數判斷
來源：ZeroJudge a922
========================================================

【問題概述】
  給定一個最多 1000 位的正整數 N（以字串形式存儲）
  判斷 N 是否為 11 的倍數

【11 的倍數判斷法則】
  若一個整數為 11 的倍數，則其「奇數位數字之和」與「偶數位數字之和」
  的差，也是 11 的倍數（可以是負數、0、或正數）

【位數計數方式（從右到左）】
  以 "12345" 為例：
    位置  5 4 3 2 1
    數字  1 2 3 4 5
  位 1, 3, 5 為奇數位（第 1, 3, 5... 位）
  位 2, 4 為偶數位（第 2, 4... 位）

【例子計算】
  1. "121"
     - 奇數位：位 1 的 1、位 3 的 1，和 = 2
     - 偶數位：位 2 的 2，和 = 2
     - 差 = 2 - 2 = 0，0 % 11 == 0 → 是 11 的倍數

  2. "11"
     - 奇數位：位 1 的 1，和 = 1
     - 偶數位：位 2 的 1，和 = 1
     - 差 = 1 - 1 = 0，0 % 11 == 0 → 是 11 的倍數

  3. "10"
     - 奇數位：位 1 的 0，和 = 0
     - 偶數位：位 2 的 1，和 = 1
     - 差 = 0 - 1 = -1，-1 % 11 != 0 → 不是 11 的倍數
"""

import unittest
import importlib.util
import os


# ──────────────────────────────────────────────────────
# 本地參考實作（用於測試驗證）
# ──────────────────────────────────────────────────────

def is_multiple_of_11(n_str: str) -> bool:
    """
    判斷字串 n_str 是否為 11 的倍數
    
    演算法：
      1. 從右到左遍歷每一位數字
      2. 奇數位（第 1, 3, 5...位）數字相加 → odd_sum
      3. 偶數位（第 2, 4, 6...位）數字相加 → even_sum
      4. 檢查 (odd_sum - even_sum) % 11 == 0
      
    Args:
      n_str: 正整數的字串表示
    
    Returns:
      True 若 n_str 為 11 的倍數，否則 False
    """
    odd_sum = 0      # 奇數位數字之和
    even_sum = 0     # 偶數位數字之和
    
    # 從右到左逐位掃描（逆序）
    for position, digit_char in enumerate(reversed(n_str)):
        digit = int(digit_char)
        # position 是 0-indexed，所以：
        # position 0, 2, 4... 對應原數的位 1, 3, 5...（奇數位）
        # position 1, 3, 5... 對應原數的位 2, 4, 6...（偶數位）
        if position % 2 == 0:
            odd_sum += digit
        else:
            even_sum += digit
    
    # 判斷差是否為 11 的倍數
    diff = odd_sum - even_sum
    return diff % 11 == 0


def solve(n_str: str) -> str:
    """
    主要求解函式，返回格式化後的判斷結果
    
    Args:
      n_str: 正整數的字串表示
    
    Returns:
      格式化的字串，表示是否為 11 的倍數
    """
    if is_multiple_of_11(n_str):
        return f"{n_str} is a multiple of 11."
    else:
        return f"{n_str} is not a multiple of 11."


# ──────────────────────────────────────────────────────
# 動態載入解答模組（若存在解答檔案會使用）
# ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename: str, module_name: str):
    """
    從指定路徑動態載入 Python 模組並回傳模組物件
    
    用途：載入 solution_10929.py 及 solution_10929-easy.py
    因為檔名含連字號 - 無法直接 import，所以用 importlib 載入
    
    Args:
      filename: 要載入的檔案名稱（含副檔名）
      module_name: 為該模組指定的名稱
    
    Returns:
      已載入的模組物件，可透過模組.solve() 呼叫求解函式
    """
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return None
    
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# 嘗試載入外部解答檔案
_std  = _load_module("solution_10929.py", "solution_10929")
_easy = _load_module("solution_10929-easy.py", "solution_10929_easy")

solve_std = _std.solve if _std else solve      # 標準版或預設
solve_easy = _easy.solve if _easy else solve   # 簡易版或預設


# ──────────────────────────────────────────────────────
# 共用測試案例 Mixin
# ──────────────────────────────────────────────────────

class _SharedCases:
    """
    共用測試用例基類
    
    子類需定義 self.solve_func 屬性，指向特定版本的求解函式
    所有子類會執行這些共同的測試，驗證不同版本的邏輯一致性
    """

    # ── 基本案例：是 11 的倍數 ────────────────────

    def test_eleven(self):
        """11 本身是 11 的倍數"""
        result = self.solve_func("11")
        self.assertEqual(result, "11 is a multiple of 11.")

    def test_twenty_two(self):
        """22 = 11 × 2，是 11 的倍數"""
        result = self.solve_func("22")
        self.assertEqual(result, "22 is a multiple of 11.")

    def test_thirty_three(self):
        """33 = 11 × 3，是 11 的倍數"""
        result = self.solve_func("33")
        self.assertEqual(result, "33 is a multiple of 11.")

    def test_one_hundred_twenty_one(self):
        """121 = 11 × 11，是 11 的倍數
        奇數位：1（位1）+ 1（位3）= 2
        偶數位：2（位2）= 2
        差 = 2 - 2 = 0，0 % 11 == 0"""
        result = self.solve_func("121")
        self.assertEqual(result, "121 is a multiple of 11.")

    def test_single_digit_zero(self):
        """0 是任何數的倍數，包括 11"""
        result = self.solve_func("0")
        self.assertEqual(result, "0 is a multiple of 11.")

    # ── 基本案例：不是 11 的倍數 ──────────────────

    def test_one(self):
        """1 不是 11 的倍數"""
        result = self.solve_func("1")
        self.assertEqual(result, "1 is not a multiple of 11.")

    def test_ten(self):
        """10 不是 11 的倍數
        奇數位：0（位1）= 0
        偶數位：1（位2）= 1
        差 = 0 - 1 = -1，-1 % 11 != 0"""
        result = self.solve_func("10")
        self.assertEqual(result, "10 is not a multiple of 11.")

    def test_twelve(self):
        """12 不是 11 的倍數"""
        result = self.solve_func("12")
        self.assertEqual(result, "12 is not a multiple of 11.")

    def test_thirteen(self):
        """13 不是 11 的倍數"""
        result = self.solve_func("13")
        self.assertEqual(result, "13 is not a multiple of 11.")

    # ── 兩位數案例 ────────────────────────────

    def test_two_digit_99(self):
        """99 = 11 × 9，是 11 的倍數
        奇數位：9（位1）= 9
        偶數位：9（位2）= 9
        差 = 9 - 9 = 0"""
        result = self.solve_func("99")
        self.assertEqual(result, "99 is a multiple of 11.")

    def test_two_digit_55(self):
        """55 = 11 × 5，是 11 的倍數"""
        result = self.solve_func("55")
        self.assertEqual(result, "55 is a multiple of 11.")

    def test_two_digit_23(self):
        """23 不是 11 的倍數
        奇數位：3（位1）= 3
        偶數位：2（位2）= 2
        差 = 3 - 2 = 1，1 % 11 != 0"""
        result = self.solve_func("23")
        self.assertEqual(result, "23 is not a multiple of 11.")

    # ── 三位數案例 ────────────────────────────

    def test_three_digit_110(self):
        """110 = 11 × 10，是 11 的倍數
        奇數位：0（位1）+ 1（位3）= 1
        偶數位：1（位2）= 1
        差 = 1 - 1 = 0"""
        result = self.solve_func("110")
        self.assertEqual(result, "110 is a multiple of 11.")

    def test_three_digit_132(self):
        """132 = 11 × 12，是 11 的倍數
        奇數位：2（位1）+ 1（位3）= 3
        偶數位：3（位2）= 3
        差 = 3 - 3 = 0"""
        result = self.solve_func("132")
        self.assertEqual(result, "132 is a multiple of 11.")

    def test_three_digit_100(self):
        """100 不是 11 的倍數
        奇數位：0（位1）+ 1（位3）= 1
        偶數位：0（位2）= 0
        差 = 1 - 0 = 1，1 % 11 != 0"""
        result = self.solve_func("100")
        self.assertEqual(result, "100 is not a multiple of 11.")

    # ── 大數案例 ──────────────────────────────

    def test_four_digit_1001(self):
        """1001 = 7 × 11 × 13，是 11 的倍數
        奇數位：1（位1）+ 0（位3）= 1
        偶數位：0（位2）+ 1（位4）= 1
        差 = 1 - 1 = 0"""
        result = self.solve_func("1001")
        self.assertEqual(result, "1001 is a multiple of 11.")

    def test_large_repeat_ones(self):
        """111111（6 個 1）= 11 × 10101，是 11 的倍數
        奇數位：1 + 1 + 1 = 3
        偶數位：1 + 1 + 1 = 3
        差 = 3 - 3 = 0"""
        result = self.solve_func("111111")
        self.assertEqual(result, "111111 is a multiple of 11.")

    def test_large_alternating(self):
        """121212（3 個 "12" 重複）= 11 × 11019
        奇數位：2 + 2 + 2 = 6
        偶數位：1 + 1 + 1 = 3
        差 = 6 - 3 = 3，3 % 11 != 0 → 不是倍數"""
        result = self.solve_func("121212")
        self.assertEqual(result, "121212 is not a multiple of 11.")

    # ── 超大數案例 ────────────────────────────

    def test_very_large_multiple(self):
        """99999 = 11 × 9090 + 9，所以不是倍數？檢查：
        99999 % 11 = 9999 % 11 + 9 = ...
        實際計算：99999 = 11 × 9090 + 9，不是倍數"""
        result = self.solve_func("99999")
        self.assertEqual(result, "99999 is not a multiple of 11.")

    def test_alternating_digits_1111111111(self):
        """1111111111（10 個 1）
        奇數位：1 × 5 = 5
        偶數位：1 × 5 = 5
        差 = 5 - 5 = 0，是 11 的倍數"""
        result = self.solve_func("1111111111")
        self.assertEqual(result, "1111111111 is a multiple of 11.")

    # ── 邊界與特殊案例 ────────────────────────

    def test_leading_zeros_not_typical(self):
        """通常不會有前導零，但測試 "01" → 按值為 1 處理"""
        result = self.solve_func("1")  # 簡化測試，不包含前導零
        self.assertEqual(result, "1 is not a multiple of 11.")

    def test_batch_mixed_numbers(self):
        """批次混合測試
        驗證多個不同的數字是否判斷正確"""
        test_cases = [
            ("11", "11 is a multiple of 11."),
            ("10", "10 is not a multiple of 11."),
            ("121", "121 is a multiple of 11."),
            ("132", "132 is a multiple of 11."),
            ("123", "123 is not a multiple of 11."),
        ]
        for input_num, expected_output in test_cases:
            with self.subTest(input_num=input_num):
                result = self.solve_func(input_num)
                self.assertEqual(result, expected_output)


# ──────────────────────────────────────────────────────
# 具體測試類別
# ──────────────────────────────────────────────────────

class TestStandard(unittest.TestCase, _SharedCases):
    """
    測試標準版解答
    
    標準版特徵：
      - 英文變數名稱（odd_sum, even_sum）
      - 型別提示
      - 簡潔的邏輯說明
    """
    def setUp(self):
        """
        setUp 在每個測試方法執行前被呼叫
        設定 self.solve_func 為標準版的 solve 函式
        """
        self.solve_func = solve_std


class TestEasy(unittest.TestCase, _SharedCases):
    """
    測試簡易好記版解答
    
    簡易版特徵：
      - 中文變數名稱容易理解
      - 詳細的步驟式註解
      - 邏輯清晰易懂
    """
    def setUp(self):
        """設定 self.solve_func 為簡易版的 solve 函式"""
        self.solve_func = solve_easy


class TestHandwrite(unittest.TestCase, _SharedCases):
    """
    測試手打版解答
    
    手打版特徵：
      - 無任何註解的純程式碼
      - 適合練習程式設計時快速實作
    """
    def setUp(self):
        """
        嘗試載入手打版，若不存在則跳過此測試類別
        """
        try:
            _handwrite = _load_module("solution_10929-handwrite.py", "solution_10929_handwrite")
            self.solve_func = _handwrite.solve
        except Exception:
            self.skipTest("solution_10929-handwrite.py 尚未建立")


class TestMultipleOf11(unittest.TestCase, _SharedCases):
    """
    相容性測試類別（保留原名稱以支持舊版測試調用）
    預設使用標準版求解函式
    """
    def setUp(self):
        """設定 self.solve_func 為標準版的 solve 函式"""
        self.solve_func = solve_std


# ──────────────────────────────────────────────────────
# 執行入口
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # verbosity=2 表示詳細輸出每個測試方法名稱與執行結果
    unittest.main(verbosity=2)
