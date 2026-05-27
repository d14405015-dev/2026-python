"""
題目 11461：Square Numbers
計算閉區間 [a, b] 內完全平方數的個數。
"""

import math


def count_square_numbers(a: int, b: int) -> int:
    """
    回傳區間 [a, b] 中完全平方數的個數。

    做法：
    - 小於等於 b 的最大整數平方根為 floor(sqrt(b))
    - 大於等於 a 的最小整數平方根為 ceil(sqrt(a))
    - 兩者之間的整數個數即為答案
    """
    # floor(sqrt(b))
    right = math.isqrt(b)
    # ceil(sqrt(a)) = floor(sqrt(a - 1)) + 1
    left = math.isqrt(a - 1) + 1

    if right < left:
        return 0
    return right - left + 1


def solve() -> None:
    """逐行讀入 a, b，直到 0 0，並輸出每組答案。"""
    while True:
        a, b = map(int, input().split())
        if a == 0 and b == 0:
            break
        print(count_square_numbers(a, b))


if __name__ == "__main__":
    solve()
