"""UVA 12019 - Doom's Day Algorithm

標準版解法：
- 這題固定在 2012 年（閏年）。
- 只要知道 2012/01/01 是 Sunday，計算日期與 1/1 相差幾天，
  再對 7 取餘數就能得到星期幾。
"""

from __future__ import annotations

# 2012 年每月天數（閏年，2 月是 29 天）
MONTH_DAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 題目要求的英文全名，索引 0 對應 Monday
WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# 2012/01/01 是 Sunday；若 Monday=0，則 Sunday 的索引是 6
JAN_1_WEEKDAY_INDEX = 6


def weekday_2012(month: int, day: int) -> str:
    """回傳 2012 年指定日期的星期英文名稱。"""
    days_passed = sum(MONTH_DAYS[: month - 1]) + (day - 1)
    weekday_index = (JAN_1_WEEKDAY_INDEX + days_passed) % 7
    return WEEKDAY_NAMES[weekday_index]


def solve(data: str) -> str:
    """處理多筆 (m, d) 查詢。"""
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    out = []

    for i in range(1, t + 1):
        m, d = map(int, lines[i].split())
        out.append(weekday_2012(m, d))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
