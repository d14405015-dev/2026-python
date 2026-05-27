"""
題目 12019：Doom's Day Algorithm（簡化版）
給定 2012 年的月份與日期，輸出該日期的星期英文全名。
"""

from datetime import date

# Python 的 weekday()：Monday=0 ... Sunday=6
WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# 讀取測試資料筆數
t = int(input().strip())

# 逐筆處理
for _ in range(t):
    # 讀取月份 m 與日期 d
    m, d = map(int, input().split())

    # 建立 2012/m/d 的日期並取得星期索引
    idx = date(2012, m, d).weekday()

    # 輸出星期英文全名
    print(WEEKDAY_NAMES[idx])
