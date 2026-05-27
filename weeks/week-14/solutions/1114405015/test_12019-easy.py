"""
題目 12019（簡化版）單元測試
測試 2012 年日期對應星期的正確性。
"""

import unittest
from datetime import date


# 與簡化版相同邏輯，抽成函式方便測試
WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def day_of_week_2012(month: int, day: int) -> str:
    """回傳 2012 年指定日期的星期英文全名。"""
    return WEEKDAY_NAMES[date(2012, month, day).weekday()]


class TestDoomsDayEasy(unittest.TestCase):
    """12019 簡化版測試集合。"""

    def test_reference_dates_from_statement(self):
        """
        測試題目敘述中的參考日期。
        """
        cases = [
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
        for (m, d), expected in cases:
            self.assertEqual(day_of_week_2012(m, d), expected)

    def test_year_start(self):
        """測試 2012/01/01。"""
        self.assertEqual(day_of_week_2012(1, 1), "Sunday")

    def test_leap_day(self):
        """測試閏日 2012/02/29。"""
        self.assertEqual(day_of_week_2012(2, 29), "Wednesday")

    def test_year_end(self):
        """測試 2012/12/31。"""
        self.assertEqual(day_of_week_2012(12, 31), "Monday")

    def test_various_dates(self):
        """測試多組一般日期。"""
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
