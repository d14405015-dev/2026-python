"""
UVA 10252 - Common Permutation（Optimized 版本）

優化重點：
1. 改用固定大小的 ASCII 計數陣列，避免 Counter 與 set 建立成本。
2. 直接走訪 0..255 的字元編碼，輸出共同字元。
3. 對大量短字串測資來說，固定陣列版本通常更輕量。
"""

from __future__ import annotations

import sys


ASCII_SIZE = 256


def common_permutation(first: str, second: str) -> str:
    count_first = [0] * ASCII_SIZE
    count_second = [0] * ASCII_SIZE

    for ch in first:
        code = ord(ch)
        if code < ASCII_SIZE:
            count_first[code] += 1

    for ch in second:
        code = ord(ch)
        if code < ASCII_SIZE:
            count_second[code] += 1

    pieces = []
    for code in range(ASCII_SIZE):
        common_count = min(count_first[code], count_second[code])
        if common_count:
            pieces.append(chr(code) * common_count)
    return "".join(pieces)


def solve(data: str) -> str:
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