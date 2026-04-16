"""
UVA 490 - easy 版本

目標：
- 更容易記憶與手打
- 用最直線的方式完成 90 度順時針旋轉

記憶口訣：
1. 先找最長行 max_len
2. 每行補空白到 max_len
3. 新的一行 i = 舊矩陣第 i 欄，從下往上抓
"""

from __future__ import annotations

import sys


def main() -> None:
    lines = sys.stdin.read().splitlines()
    if not lines:
        return

    max_len = max(len(s) for s in lines)

    # 補空白讓每行等長，避免索引越界。
    pad = [s.ljust(max_len, " ") for s in lines]

    out: list[str] = []

    for c in range(max_len):
        row_chars: list[str] = []
        for r in range(len(pad) - 1, -1, -1):
            row_chars.append(pad[r][c])
        out.append("".join(row_chars))

    print("\n".join(out) + "\n", end="")


if __name__ == "__main__":
    main()
