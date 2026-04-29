"""
UVA 10235 - Simply Emirp（Easy 版本）

說明：
- week-10/QUESTION-10235.md 的敘述文字與題名不一致，
  這裡依據題號 10235（ZeroJudge a228）標準規格實作。

題意（Emirp）：
- 讀入多個整數 n（直到 EOF）。
- 若 n 不是質數：輸出 "n is not prime."。
- 若 n 是質數，但反轉數 reverse(n) 不是質數，或 reverse(n) == n：
  輸出 "n is prime."。
- 若 n 與 reverse(n) 都是質數，且兩者不同：
  輸出 "n is emirp."。
"""

from __future__ import annotations

import math
import sys


def is_prime(num: int) -> bool:
    """判斷是否為質數（簡單好記版）。"""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    limit = int(math.isqrt(num))
    d = 3
    while d <= limit:
        if num % d == 0:
            return False
        d += 2
    return True


def classify_number(n: int) -> str:
    """回傳單一數字對應的輸出句子。"""
    if not is_prime(n):
        return f"{n} is not prime."

    rev = int(str(n)[::-1])
    if rev != n and is_prime(rev):
        return f"{n} is emirp."
    return f"{n} is prime."


def solve(data: str) -> str:
    """解析整份輸入並組合輸出。"""
    out_lines = []

    for token in data.split():
        n = int(token)
        out_lines.append(classify_number(n))

    return "\n".join(out_lines)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
