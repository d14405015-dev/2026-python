"""
題目 12019：UVA Doom's Day Algorithm
給定 2012 年的月份與日期，輸出對應的星期英文全名。
"""

from datetime import date


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
    """
    回傳 2012 年指定日期的星期英文全名。

    參數：
        month: 月份（1~12）
        day: 日期（依月份合法範圍）
    """
    weekday_index = date(2012, month, day).weekday()
    return WEEKDAY_NAMES[weekday_index]


def solve() -> None:
    """讀取輸入並輸出每組日期的星期。"""
    t = int(input().strip())
    for _ in range(t):
        m, d = map(int, input().split())
        print(day_of_week_2012(m, d))


if __name__ == "__main__":
    solve()
