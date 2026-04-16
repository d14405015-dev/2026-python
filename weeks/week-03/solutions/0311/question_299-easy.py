"""
UVA 299 - easy 版本

目標：
- 更容易記憶、容易手打
- 邏輯直線化
- 保留正確輸出格式

記憶口訣：
1. 讀入一組車廂順序
2. 用雙迴圈比大小
3. 逆序就交換，交換次數 +1
4. 印出固定句型
"""

from __future__ import annotations

import sys


def main() -> None:
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip() != ""]
    if not lines:
        return

    t = int(lines[0])
    p = 1
    ans: list[str] = []

    for _ in range(t):
        l = int(lines[p])
        p += 1

        if l == 0:
            ans.append("Optimal train swapping takes 0 swaps.")
            continue

        a = list(map(int, lines[p].split()))
        p += 1

        cnt = 0

        # 簡化版氣泡排序：一旦左邊比右邊大就交換。
        for i in range(l):
            for j in range(0, l - 1 - i):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    cnt += 1

        ans.append(f"Optimal train swapping takes {cnt} swaps.")

    print("\n".join(ans))


if __name__ == "__main__":
    main()
