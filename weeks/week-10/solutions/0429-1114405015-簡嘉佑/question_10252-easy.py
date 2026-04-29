"""
UVA 10252 - Common Permutation（Easy 版本）

說明：
- week-10/QUESTION-10252.md 的敘述文字和題號不一致。
- 這份程式依照 UVA 10252 / Common Permutation 的標準規格實作，
  也和課程清單中的題名一致。

題意簡化：
- 每次讀兩行字串。
- 找出兩行中共同出現的字元。
- 若某字元在第一行出現 3 次、第二行出現 5 次，
  那答案就要放 min(3, 5) = 3 次。
- 最後將共同字元依字典序（字元由小到大）輸出。
"""

from __future__ import annotations

import sys
from collections import Counter


def common_permutation(first: str, second: str) -> str:
    """回傳兩字串的共同字元，並依字元順序排列。"""
    count_first = Counter(first)
    count_second = Counter(second)

    pieces = []
    for ch in sorted(count_first.keys() & count_second.keys()):
        pieces.append(ch * min(count_first[ch], count_second[ch]))
    return "".join(pieces)


def solve(data: str) -> str:
    """每兩行當成一組測資，輸出共同排列。"""
    lines = data.splitlines()
    out_lines = []

    for index in range(0, len(lines), 2):
        if index + 1 >= len(lines):
            break
        out_lines.append(common_permutation(lines[index], lines[index + 1]))

    return "\n".join(out_lines)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()