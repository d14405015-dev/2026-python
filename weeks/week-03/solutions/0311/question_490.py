"""
UVA 490 - Rotating Sentences

題目要求：
- 將輸入的多行文字，做 90 度順時針旋轉。
- 輸出的每一行長度要一致（等於輸入最大寬度），
  缺的部分要用空白補齊。

本版本特色：
- 函式化寫法，邏輯清楚。
- 以繁體中文詳細註解說明每一步。
"""

from __future__ import annotations

import sys


def rotate_90_clockwise(lines: list[str]) -> list[str]:
    """把多行字串順時針旋轉 90 度。

    觀念：
    - 假設輸入有 R 列，最大寬度是 C。
    - 旋轉後會有 C 列，每列長度是 R。
    - 新矩陣的第 col 列，來自原矩陣的該欄，
      但列的順序要由下往上讀。

    例如：
    原本 (row, col) 的字元，會移到旋轉後的 (col, R-1-row)。
    """
    if not lines:
        return []

    row_count = len(lines)
    col_count = max(len(line) for line in lines)

    # 先把每一行補到同樣長度，方便用「矩陣」概念索引。
    padded = [line.ljust(col_count, " ") for line in lines]

    result: list[str] = []

    # 旋轉後的每一行對應原本的一個欄位 col。
    for col in range(col_count):
        chars: list[str] = []

        # 由下往上取字元，形成順時針旋轉後的橫列。
        for row in range(row_count - 1, -1, -1):
            chars.append(padded[row][col])

        result.append("".join(chars))

    return result


def solve(data: str) -> str:
    """解析整份輸入並回傳旋轉後字串。"""
    # splitlines() 會保留每行內容（不含換行符號本身）。
    lines = data.splitlines()

    rotated = rotate_90_clockwise(lines)

    # 題目輸出是逐行印出，所以以 \n 串接；
    # 若有內容，最後補一個換行，符合一般 UVA 輸出習慣。
    if not rotated:
        return ""
    return "\n".join(rotated) + "\n"


def main() -> None:
    """程式進入點：讀 stdin，輸出結果。"""
    data = sys.stdin.read()
    output = solve(data)
    print(output, end="")


if __name__ == "__main__":
    main()
