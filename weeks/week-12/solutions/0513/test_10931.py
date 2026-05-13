"""
========================================================
題目：UVA 10931 — Parity（奇偶性）
來源：ZeroJudge a924
========================================================

【問題概述】
  給定一個整數 I（1 ≤ I ≤ 2,147,483,647）
  計算其二進位表示中 1 的個數（即「奇偶性」或「漢明重量」）

【奇偶性定義】
  整數 N 的「奇偶性（Parity）」定義為其二進位表示中，1 的個數

【解題步驟】
  1. 將十進位整數 I 轉換為二進位表示（字串形式）
  2. 去掉 "0b" 前綴，得到純二進位字串 B
  3. 計算字串 B 中 '1' 的個數 P
  4. 輸出格式："The parity of {B} is {P} (mod 2)."

【例子計算】
  I = 1
    二進位 = 1
    1 的個數 = 1
    輸出 = "The parity of 1 is 1 (mod 2)."

  I = 2
    二進位 = 10
    1 的個數 = 1
    輸出 = "The parity of 10 is 1 (mod 2)."

  I = 10
    二進位 = 1010
    1 的個數 = 2
    輸出 = "The parity of 1010 is 2 (mod 2)."

  I = 21
    二進位 = 10101
    1 的個數 = 3
    輸出 = "The parity of 10101 is 3 (mod 2)."
"""

import unittest
import importlib.util
import os


# ──────────────────────────────────────────────────────
# 本地參考實作（用於測試驗證）
# ──────────────────────────────────────────────────────

def get_binary_representation(n: int) -> str:
    """
    將十進位整數 n 轉換為二進位字串表示
    
    Args:
      n (int): 十進位整數
    
    Returns:
      str: 二進位表示（不含 "0b" 前綴，無前導零）
    
    例子：
      1 → "1"
      2 → "10"
      10 → "1010"
      21 → "10101"
      255 → "11111111"
    """
    return bin(n)[2:]  # bin() 返回 "0b..." 格式，去掉前 2 個字元


def count_ones_in_binary(n: int) -> int:
    """
    計算整數 n 的二進位表示中 1 的個數（漢明重量）
    
    也稱為「Hamming Weight」或「Population Count」
    
    Args:
      n (int): 十進位整數
    
    Returns:
      int: 二進位表示中 1 的個數
    
    例子：
      1 → 1（"1" 有 1 個 1）
      2 → 1（"10" 有 1 個 1）
      3 → 2（"11" 有 2 個 1）
      10 → 2（"1010" 有 2 個 1）
      21 → 3（"10101" 有 3 個 1）
    """
    # 方法 1：使用 bin() 轉換後計算 '1' 的個數（簡潔易懂）
    return bin(n).count('1')


def solve(n: int) -> str:
    """
    主要求解函式，返回格式化後的奇偶性判斷結果
    
    Args:
      n (int): 十進位整數
    
    Returns:
      str: 格式化的字串，表示該數的奇偶性
           格式: "The parity of {二進位} is {1的個數} (mod 2)."
    
    例子：
      1 → "The parity of 1 is 1 (mod 2)."
      10 → "The parity of 1010 is 2 (mod 2)."
    """
    # 取得二進位表示
    binary_str = get_binary_representation(n)
    
    # 計算 1 的個數
    parity = count_ones_in_binary(n)
    
    # 格式化輸出
    return f"The parity of {binary_str} is {parity} (mod 2)."


# ──────────────────────────────────────────────────────
# 動態載入解答模組（若存在解答檔案會使用）
# ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename: str, module_name: str):
    """
    從指定路徑動態載入 Python 模組
    
    用途：載入 solution_10931.py 及 solution_10931-easy.py
    因為檔名含連字號 - 無法直接 import，所以用 importlib 載入
    
    Args:
      filename (str): 要載入的檔案名稱（含副檔名）
      module_name (str): 為該模組指定的名稱
    
    Returns:
      module 或 None: 已載入的模組物件，或 None 若檔案不存在
    """
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return None
    
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# 嘗試載入外部解答檔案
_std  = _load_module("solution_10931.py", "solution_10931")
_easy = _load_module("solution_10931-easy.py", "solution_10931_easy")

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

    # ── 單位數（1 位二進位）────────────────────────

    def test_one(self):
        """1 的二進位是 1，有 1 個 1"""
        result = self.solve_func(1)
        self.assertEqual(result, "The parity of 1 is 1 (mod 2).")

    # ── 2 的冪次（單一 1）─────────────────────────

    def test_two(self):
        """2 的二進位是 10，有 1 個 1"""
        result = self.solve_func(2)
        self.assertEqual(result, "The parity of 10 is 1 (mod 2).")

    def test_four(self):
        """4 的二進位是 100，有 1 個 1"""
        result = self.solve_func(4)
        self.assertEqual(result, "The parity of 100 is 1 (mod 2).")

    def test_eight(self):
        """8 的二進位是 1000，有 1 個 1"""
        result = self.solve_func(8)
        self.assertEqual(result, "The parity of 1000 is 1 (mod 2).")

    def test_power_of_two_large(self):
        """1024 = 2^10，二進位是 10000000000，有 1 個 1"""
        result = self.solve_func(1024)
        self.assertEqual(result, "The parity of 10000000000 is 1 (mod 2).")

    # ── 全 1 數字（2^n - 1）───────────────────────

    def test_three(self):
        """3 = 2^2 - 1，二進位是 11，有 2 個 1"""
        result = self.solve_func(3)
        self.assertEqual(result, "The parity of 11 is 2 (mod 2).")

    def test_seven(self):
        """7 = 2^3 - 1，二進位是 111，有 3 個 1"""
        result = self.solve_func(7)
        self.assertEqual(result, "The parity of 111 is 3 (mod 2).")

    def test_fifteen(self):
        """15 = 2^4 - 1，二進位是 1111，有 4 個 1"""
        result = self.solve_func(15)
        self.assertEqual(result, "The parity of 1111 is 4 (mod 2).")

    def test_thirty_one(self):
        """31 = 2^5 - 1，二進位是 11111，有 5 個 1"""
        result = self.solve_func(31)
        self.assertEqual(result, "The parity of 11111 is 5 (mod 2).")

    # ── 交替 1 和 0────────────────────────────────

    def test_ten(self):
        """10 的二進位是 1010，有 2 個 1"""
        result = self.solve_func(10)
        self.assertEqual(result, "The parity of 1010 is 2 (mod 2).")

    def test_twenty_one(self):
        """21 的二進位是 10101，有 3 個 1"""
        result = self.solve_func(21)
        self.assertEqual(result, "The parity of 10101 is 3 (mod 2).")

    def test_forty_two(self):
        """42 的二進位是 101010，有 3 個 1"""
        result = self.solve_func(42)
        self.assertEqual(result, "The parity of 101010 is 3 (mod 2).")

    def test_eighty_five(self):
        """85 的二進位是 1010101，有 4 個 1"""
        result = self.solve_func(85)
        self.assertEqual(result, "The parity of 1010101 is 4 (mod 2).")

    # ── 特定數字測試─────────────────────────────

    def test_five(self):
        """5 的二進位是 101，有 2 個 1"""
        result = self.solve_func(5)
        self.assertEqual(result, "The parity of 101 is 2 (mod 2).")

    def test_six(self):
        """6 的二進位是 110，有 2 個 1"""
        result = self.solve_func(6)
        self.assertEqual(result, "The parity of 110 is 2 (mod 2).")

    def test_nine(self):
        """9 的二進位是 1001，有 2 個 1"""
        result = self.solve_func(9)
        self.assertEqual(result, "The parity of 1001 is 2 (mod 2).")

    def test_sixteen(self):
        """16 的二進位是 10000，有 1 個 1"""
        result = self.solve_func(16)
        self.assertEqual(result, "The parity of 10000 is 1 (mod 2).")

    def test_thirty_two(self):
        """32 的二進位是 100000，有 1 個 1"""
        result = self.solve_func(32)
        self.assertEqual(result, "The parity of 100000 is 1 (mod 2).")

    # ── 邊界與大數值────────────────────────────

    def test_max_int_limit(self):
        """2147483647 = 2^31 - 1，全是 1，有 31 個 1"""
        result = self.solve_func(2147483647)
        self.assertEqual(result, "The parity of 1111111111111111111111111111111 is 31 (mod 2).")

    def test_large_mixed(self):
        """1000 的二進位是 1111101000，有 6 個 1"""
        result = self.solve_func(1000)
        self.assertEqual(result, "The parity of 1111101000 is 6 (mod 2).")

    # ── 批次模擬──────────────────────────────────

    def test_batch_official_examples(self):
        """
        官方範例集合測試
        確保所有官方測試案例都通過
        """
        test_cases = [
            (1, "The parity of 1 is 1 (mod 2)."),
            (2, "The parity of 10 is 1 (mod 2)."),
            (10, "The parity of 1010 is 2 (mod 2)."),
            (21, "The parity of 10101 is 3 (mod 2)."),
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
      - 英文變數名稱
      - 型別提示
      - 邏輯清晰
    """
    def setUp(self):
        """setUp 在每個測試方法執行前被呼叫"""
        self.solve_func = solve_std


class TestEasy(unittest.TestCase, _SharedCases):
    """
    測試簡易好記版解答
    
    簡易版特徵：
      - 中文變數名稱
      - 詳細的步驟式註解
      - 邏輯易於理解
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
            _handwrite = _load_module("solution_10931-handwrite.py", "solution_10931_handwrite")
            self.solve_func = _handwrite.solve
        except Exception:
            self.skipTest("solution_10931-handwrite.py 尚未建立")


class TestParity(unittest.TestCase, _SharedCases):
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
