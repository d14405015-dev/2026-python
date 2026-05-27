"""
題目 11461：Square Numbers（簡化版）
計算區間 [a, b] 內完全平方數的個數。
"""

import math


# 計算區間 [a, b] 內完全平方數的個數
# 觀念：
# 1. 小於等於 b 的最大整數平方根是 floor(sqrt(b))
# 2. 大於等於 a 的最小整數平方根是 ceil(sqrt(a))
# 3. 兩者相減再加 1，就是平方數的個數
while True:
    a, b = map(int, input().split())

    # 結束條件
    if a == 0 and b == 0:
        break

    # 右邊界：最大的平方根整數
    right = math.isqrt(b)

    # 左邊界：最小的平方根整數（用 isqrt(a - 1) + 1 取得 ceil(sqrt(a))）
    left = math.isqrt(a - 1) + 1

    # 若沒有平方數落在區間中，答案是 0
    if right < left:
        print(0)
    else:
        print(right - left + 1)
