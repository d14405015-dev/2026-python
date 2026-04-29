"""
UVA 10235 - Simply Emirp（Optimized 版本）

優化重點：
1. 用 lru_cache 記住已檢查過的質數判斷結果，避免重複試除。
2. 質數判斷改成 6k +/- 1 方式，減少不必要的除法次數。
3. 反轉數字改用整數運算，不必額外建立反轉字串。
"""

from __future__ import annotations

import math
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def is_prime(num: int) -> bool:
    if num < 2:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    limit = int(math.isqrt(num))
    divisor = 5
    while divisor <= limit:
        if num % divisor == 0 or num % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def reverse_number(num: int) -> int:
    reversed_num = 0
    while num > 0:
        reversed_num = reversed_num * 10 + (num % 10)
        num //= 10
    return reversed_num


def classify_number(num: int) -> str:
    if not is_prime(num):
        return f"{num} is not prime."

    reversed_num = reverse_number(num)
    if reversed_num != num and is_prime(reversed_num):
        return f"{num} is emirp."
    return f"{num} is prime."


def solve(data: str) -> str:
    return "\n".join(classify_number(int(token)) for token in data.split())


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()