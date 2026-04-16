"""
UVA 10035 - Primary Arithmetic

題目重點
- 每行輸入兩個非負整數 a, b。
- 模擬直式加法，統計「進位」總共發生幾次。
- 當讀到 0 0 時，輸入結束，不輸出該行結果。

輸出句型
- 0 次：No carry operation.
- 1 次：1 carry operation.
- 2 次以上：X carry operations.
"""

import sys


def count_carry_operations(a: int, b: int) -> int:
    """計算 a 與 b 相加時，總共會發生幾次進位。"""
    carry = 0
    carry_count = 0

    # 只要任一數字還有位數，或前一位仍有 carry，都要繼續處理。
    while a > 0 or b > 0:
        digit_sum = (a % 10) + (b % 10) + carry

        if digit_sum >= 10:
            carry = 1
            carry_count += 1
        else:
            carry = 0

        a //= 10
        b //= 10

    return carry_count


def format_result(carry_count: int) -> str:
    """依照題目指定句型格式化答案字串。"""
    if carry_count == 0:
        return "No carry operation."
    if carry_count == 1:
        return "1 carry operation."
    return f"{carry_count} carry operations."


def main() -> None:
    """逐行讀入直到 EOF，遇到 0 0 終止。"""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            # 防禦性寫法：若有空行則跳過。
            continue

        a, b = map(int, line.split())

        if a == 0 and b == 0:
            break

        carry_count = count_carry_operations(a, b)
        print(format_result(carry_count))


if __name__ == "__main__":
    main()
