import math
import sys


def solve_one_case(start_size, target_day):
    """容易記憶版：把題目轉成一個不等式。

    口訣：
    1. 先寫總天數公式
    2. 變形成 n(n+1) >= 某個值
    3. 用 sqrt 找到 n，再做 1~2 次修正

    從 S 人團一路住到 n 人團，總天數：
      S + (S+1) + ... + n
    可改寫為：
      n(n+1)/2 - (S-1)S/2

    令它 >= D，得到：
      n(n+1) >= 2D + (S-1)S
    """
    right_value = 2 * target_day + (start_size - 1) * start_size

    # 先用整數平方根抓近似值。
    n = (math.isqrt(1 + 4 * right_value) - 1) // 2

    # 往上補到合法。
    while n * (n + 1) < right_value:
        n += 1

    # 往下檢查是否可以再小一點，確保是「最小合法 n」。
    while n > start_size and (n - 1) * n >= right_value:
        n -= 1

    if n < start_size:
        n = start_size

    return n


def solve(data):
    """逐行讀取到 EOF，每行輸出對應答案。"""
    answers = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        start_size, target_day = map(int, line.split())
        answers.append(str(solve_one_case(start_size, target_day)))

    return "\n".join(answers) + ("\n" if answers else "")


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
