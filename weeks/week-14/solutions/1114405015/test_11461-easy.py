"""
題目 11461（簡化版）的單元測試
驗證區間 [a, b] 內完全平方數個數的計算是否正確。
"""

import unittest
import math


# 與簡化版解題程式相同邏輯，抽成函式方便測試
# 輸入：區間左右邊界 a, b
# 輸出：[a, b] 內完全平方數的個數
def count_square_numbers(a: int, b: int) -> int:
    right = math.isqrt(b)
    left = math.isqrt(a - 1) + 1

    if right < left:
        return 0
    return right - left + 1


class TestSquareNumbersEasy(unittest.TestCase):
    """Square Numbers 簡化版測試集合。"""

    def test_sample_1(self):
        """題目範例：區間 [1, 4] 有 1, 4，共 2 個。"""
        self.assertEqual(count_square_numbers(1, 4), 2)

    def test_sample_2(self):
        """題目範例：區間 [1, 10] 有 1, 4, 9，共 3 個。"""
        self.assertEqual(count_square_numbers(1, 10), 3)

    def test_sample_3(self):
        """題目範例：區間 [1, 100000] 應為 316。"""
        self.assertEqual(count_square_numbers(1, 100000), 316)

    def test_single_square(self):
        """單點區間且為平方數。"""
        self.assertEqual(count_square_numbers(64, 64), 1)

    def test_single_non_square(self):
        """單點區間且不是平方數。"""
        self.assertEqual(count_square_numbers(65, 65), 0)

    def test_no_square(self):
        """區間內沒有平方數。"""
        self.assertEqual(count_square_numbers(2, 3), 0)

    def test_middle_range(self):
        """一般區間測試。"""
        # 16, 25, 36, 49
        self.assertEqual(count_square_numbers(10, 50), 4)

    def test_upper_boundary_close(self):
        """接近上界 100000 的測試。"""
        # 316^2 = 99856, 317^2 = 100489
        self.assertEqual(count_square_numbers(99856, 100000), 1)

    def test_upper_boundary_no_square(self):
        """接近上界且無平方數的區間。"""
        self.assertEqual(count_square_numbers(99900, 100000), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
