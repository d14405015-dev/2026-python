import math
import sys


def find_group_size(start_size, target_day):
    """回傳第 target_day 天入住的旅行團人數。

    令起始團人數為 S，目標人數為 n（n >= S）。
    從 S 到 n 的總住宿天數為：

        S + (S + 1) + ... + n
      = n(n + 1)/2 - (S - 1)S/2

    我們要找最小的 n，使上式 >= D。
    轉換後可得：

        n(n + 1) >= 2D + (S - 1)S

    設 R = 2D + (S - 1)S，
    先用整數平方根估計 n，再做微調，確保得到最小合法解。
    """
    required = 2 * target_day + (start_size - 1) * start_size

    # n(n+1) >= required，先用二次式近似求下界。
    candidate = (math.isqrt(1 + 4 * required) - 1) // 2

    # 微調到最小可行 n。
    while candidate * (candidate + 1) < required:
        candidate += 1
    while candidate > start_size and (candidate - 1) * candidate >= required:
        candidate -= 1

    # 題目保證 n 不會小於 S，但仍保底處理。
    if candidate < start_size:
        candidate = start_size

    return candidate


def solve(data):
    """處理多筆輸入直到 EOF，每筆輸出一行答案。"""
    lines = []

    for raw in data.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        start_size, target_day = map(int, raw.split())
        answer = find_group_size(start_size, target_day)
        lines.append(str(answer))

    return "\n".join(lines) + ("\n" if lines else "")


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
