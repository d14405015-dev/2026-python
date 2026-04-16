"""
UVA 10038（簡單好記版）

口訣：
1. 算每一對相鄰數字的差絕對值
2. 檢查差值要在 1..n-1
3. 差值不能重複
4. 最後收集到 n-1 個差值就是 Jolly

這版重點是流程直覺，方便考場手打。
"""

import sys


def check_jolly(arr: list[int]) -> bool:
    """回傳 arr 是否為 Jolly Jumper。"""
    n = len(arr)
    if n <= 1:
        return True

    diffs = set()

    for i in range(1, n):
        d = abs(arr[i] - arr[i - 1])

        # 差值超界或重複都直接失敗
        if d < 1 or d > n - 1 or d in diffs:
            return False

        diffs.add(d)

    return len(diffs) == n - 1


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        vals = list(map(int, line.split()))
        n = vals[0]
        arr = vals[1:1 + n]

        if len(arr) != n:
            print("Not jolly")
            continue

        if check_jolly(arr):
            print("Jolly")
        else:
            print("Not jolly")


if __name__ == "__main__":
    main()
