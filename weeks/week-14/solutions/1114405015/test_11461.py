"""
題目 11461 的 Unit Test
測試區間內完全平方數個數的計算邏輯。
"""

import unittest

from solution_11461 import count_square_numbers


class TestSquareNumbers(unittest.TestCase):
    """Square Numbers 測試集合。"""

    def test_sample_case_1(self):
        """題目範例：區間 [1, 4] 內有 1, 4 共 2 個。"""
        self.assertEqual(count_square_numbers(1, 4), 2)

    def test_sample_case_2(self):
        """題目範例：區間 [1, 10] 內有 1, 4, 9 共 3 個。"""
        self.assertEqual(count_square_numbers(1, 10), 3)

    def test_sample_case_3(self):
        """題目範例：區間 [1, 100000] 內應有 316 個。"""
        self.assertEqual(count_square_numbers(1, 100000), 316)

    def test_single_square(self):
        """只有一個數字且為完全平方數。"""
        self.assertEqual(count_square_numbers(49, 49), 1)

    def test_single_non_square(self):
        """只有一個數字且非完全平方數。"""
        self.assertEqual(count_square_numbers(50, 50), 0)

    def test_no_square_in_range(self):
        """區間內沒有任何完全平方數。"""
        self.assertEqual(count_square_numbers(2, 3), 0)

    def test_range_between_squares(self):
        """跨多個平方數的區間。"""
        # 16, 25, 36, 49, 64, 81, 100 -> 共 7 個
        self.assertEqual(count_square_numbers(10, 100), 7)

    def test_large_boundary(self):
        """接近題目上限的邊界測試。"""
        # 316^2 = 99856, 317^2 = 100489
        self.assertEqual(count_square_numbers(99900, 100000), 0)

    def test_include_upper_square(self):
        """上界剛好是完全平方數。"""
        # 10000 = 100^2
        self.assertEqual(count_square_numbers(9900, 10000), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
