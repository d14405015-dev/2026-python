"""
UVA 10038 - Jolly Jumpers

題意整理
- 每行資料格式：n a1 a2 ... an
- 若相鄰數字差的絕對值集合，剛好是 1..(n-1)，則輸出 "Jolly"
- 否則輸出 "Not jolly"

關鍵觀念
- 長度為 n 的序列共有 n-1 個相鄰差。
- 要成為 Jolly，必須同時滿足：
  1) 每個差值都在 [1, n-1]
  2) 差值不能重複
  3) 最後剛好收集到 n-1 個合法差值
"""

import sys


def is_jolly(sequence: list[int]) -> bool:
    """判斷一個整數序列是否為 Jolly Jumper。"""
    n = len(sequence)

    # n=1 時沒有相鄰差，依題意視為 Jolly。
    if n <= 1:
        return True

    seen = set()  # 用來記錄已出現的差值

    for i in range(1, n):
        diff = abs(sequence[i] - sequence[i - 1])

        # 差值必須落在 1..n-1 範圍內，且不能重複。
        if diff < 1 or diff > n - 1 or diff in seen:
            return False

        seen.add(diff)

    # 能收齊 1..n-1 共 n-1 個不同差值才是 Jolly。
    return len(seen) == n - 1


def main() -> None:
    """逐行讀到 EOF，對每一行輸出 Jolly / Not jolly。"""
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        nums = list(map(int, line.split()))
        n = nums[0]
        seq = nums[1:1 + n]

        # 題目理論上保證輸入合法；此處保留防禦性處理。
        if len(seq) != n:
            print("Not jolly")
            continue

        print("Jolly" if is_jolly(seq) else "Not jolly")


if __name__ == "__main__":
    main()
