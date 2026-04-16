"""
UVA 10035（簡單好記版）

口訣：
1. 從個位數開始加
2. 超過 9 就算一次進位
3. 繼續往高位做，直到兩數都處理完
4. 依進位次數輸出固定句型

這版把邏輯拆成「算進位」與「印句型」兩個小函式，
現場手打時更容易記。
"""

import sys


def carry_count(a: int, b: int) -> int:
    """回傳 a + b 的進位次數。"""
    c = 0      # c 表示上一位是否有進位（0 或 1）
    ans = 0    # ans 累計總進位次數

    while a > 0 or b > 0:
        s = (a % 10) + (b % 10) + c
        if s >= 10:
            c = 1
            ans += 1
        else:
            c = 0

        a //= 10
        b //= 10

    return ans


def to_sentence(k: int) -> str:
    """把進位次數轉成題目要的英文句子。"""
    if k == 0:
        return "No carry operation."
    if k == 1:
        return "1 carry operation."
    return f"{k} carry operations."


def main() -> None:
    # 逐行讀入，直到 EOF。
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        a, b = map(int, line.split())

        # 題目規定 0 0 代表輸入結束。
        if a == 0 and b == 0:
            break

        print(to_sentence(carry_count(a, b)))


if __name__ == "__main__":
    main()
