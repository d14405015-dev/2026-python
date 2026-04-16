"""
UVA 272 - easy 版本

目標：
- 更容易手打
- 更容易記憶
- 仍保證輸入輸出格式正確

記憶口訣：
1. 用一個布林值記錄「下一個雙引號是開還是關」
2. 每遇到一次 ", 就輸出 `` 或 ''，然後切換布林值
3. 其他字元照抄
"""

from __future__ import annotations

import sys


def main() -> None:
    s = sys.stdin.read()

    ans: list[str] = []
    is_open = True

    for c in s:
        if c == '"':
            if is_open:
                ans.append("``")
            else:
                ans.append("''")
            is_open = not is_open
        else:
            ans.append(c)

    print("".join(ans), end="")


if __name__ == "__main__":
    main()
