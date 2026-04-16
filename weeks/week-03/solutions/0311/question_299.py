"""
UVA 299 - Train Swapping

題意摘要：
給定每組火車車廂的排列，
每次只能交換「相鄰」兩節車廂，
要算出排成 1..L 遞增順序所需的最少交換次數。

核心觀念：
- 最少相鄰交換次數 = 反序對（inversion）數量。
- 這裡使用容易理解的氣泡排序計數版本：
  每做一次相鄰交換，就把計數 +1。
"""

from __future__ import annotations

import sys


def count_swaps_with_bubble(arr: list[int]) -> int:
    """以氣泡排序概念計算最少相鄰交換次數。

    說明：
    - 若 arr[i] > arr[i+1]，代表這對元素形成反序，
      透過交換把較大的元素往右推。
    - 整個排序過程中交換總次數，即為答案。

    時間複雜度：O(n^2)
    在題目 L <= 50 的限制下非常足夠。
    """
    a = arr[:]  # 複製一份，避免修改原始資料
    n = len(a)
    swaps = 0

    # 標準氣泡排序：每一輪把最大值推到右側。
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True

        # 若某輪完全沒有交換，代表已排序完成，可提早結束。
        if not swapped:
            break

    return swaps


def solve(data: str) -> str:
    """解析輸入並輸出每組測資結果。"""
    lines = [line.strip() for line in data.splitlines()]

    # 過濾掉空行，讓輸入更有彈性。
    lines = [line for line in lines if line != ""]
    if not lines:
        return ""

    t = int(lines[0])
    idx = 1
    out: list[str] = []

    for _ in range(t):
        l = int(lines[idx])
        idx += 1

        # L 可能為 0，這時下一行可能是空；依題意答案為 0 swaps。
        if l == 0:
            out.append("Optimal train swapping takes 0 swaps.")
            continue

        arr = list(map(int, lines[idx].split()))
        idx += 1

        swaps = count_swaps_with_bubble(arr)
        out.append(f"Optimal train swapping takes {swaps} swaps.")

    return "\n".join(out)


def main() -> None:
    """程式進入點：讀 stdin，計算後輸出。"""
    data = sys.stdin.read()
    result = solve(data)
    if result:
        print(result)


if __name__ == "__main__":
    main()
