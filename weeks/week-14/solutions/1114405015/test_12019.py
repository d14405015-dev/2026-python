"""
題目 12019 的單元測試
針對 2012 年日期對應星期的邏輯進行驗證。
"""

import unittest

from solution_12019 import day_of_week_2012


class TestDoomsDay2012(unittest.TestCase):
    """Doom's Day 題目測試集合。"""

    def test_reference_dates_from_statement(self):
        """
        驗證題目敘述中列出的參考日期在 2012 年的對應星期。
        """
        reference_dates = [
            ((1, 10), "Tuesday"),
            ((2, 21), "Tuesday"),
            ((3, 7), "Wednesday"),
            ((4, 4), "Wednesday"),
            ((5, 9), "Wednesday"),
            ((6, 6), "Wednesday"),
            ((7, 11), "Wednesday"),
            ((8, 8), "Wednesday"),
            ((9, 5), "Wednesday"),
            ((10, 10), "Wednesday"),
            ((11, 7), "Wednesday"),
            ((12, 12), "Wednesday"),
        ]

        for (m, d), expected in reference_dates:
            self.assertEqual(day_of_week_2012(m, d), expected)

    def test_leap_day(self):
        """驗證閏日 2012/02/29 為 Wednesday。"""
        self.assertEqual(day_of_week_2012(2, 29), "Wednesday")

    def test_year_start(self):
        """驗證 2012/01/01 為 Sunday。"""
        self.assertEqual(day_of_week_2012(1, 1), "Sunday")

    def test_year_end(self):
        """驗證 2012/12/31 為 Monday。"""
        self.assertEqual(day_of_week_2012(12, 31), "Monday")

    def test_various_dates(self):
        """驗證多組一般日期。"""
        cases = [
            ((3, 14), "Wednesday"),
            ((4, 1), "Sunday"),
            ((6, 30), "Saturday"),
            ((10, 31), "Wednesday"),
            ((11, 30), "Friday"),
        ]

        for (m, d), expected in cases:
            self.assertEqual(day_of_week_2012(m, d), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
