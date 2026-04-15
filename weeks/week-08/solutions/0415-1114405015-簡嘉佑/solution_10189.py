from typing import List


def _count_adjacent_mines(grid: List[str], row: int, col: int, n: int, m: int) -> int:
    """計算某一格周圍 8 個方向的地雷數量。"""
    count = 0

    # 8 個方向：上、下、左、右、左上、右上、左下、右下
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for dr, dc in directions:
        nr = row + dr
        nc = col + dc

        # 先檢查是否越界，再判斷是否為地雷
        if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == "*":
            count += 1

    return count


def solve(input_data: str) -> str:
    """
    UVA 10189 Minesweeper 主解函式。

    參數:
        input_data: 完整輸入字串（可能含多組測資）

    回傳:
        題目要求格式的完整輸出字串
    """
    lines = input_data.splitlines()
    idx = 0
    field_number = 1
    output_blocks: List[str] = []

    while idx < len(lines):
        line = lines[idx].strip()
        idx += 1

        # 跳過可能存在的空白行，避免因格式雜訊造成解析錯誤
        if not line:
            continue

        n, m = map(int, line.split())

        # 0 0 代表輸入結束，不需要再處理
        if n == 0 and m == 0:
            break

        # 讀取目前這一組地圖
        grid = [lines[idx + r].rstrip("\n") for r in range(n)]
        idx += n

        result_rows: List[str] = []

        # 逐格產生答案
        for r in range(n):
            row_chars: List[str] = []
            for c in range(m):
                if grid[r][c] == "*":
                    # 地雷格維持星號不變
                    row_chars.append("*")
                else:
                    # 空白格改成相鄰地雷數
                    mines = _count_adjacent_mines(grid, r, c, n, m)
                    row_chars.append(str(mines))
            result_rows.append("".join(row_chars))

        # 每個 Field 區塊都獨立組成，最後再用空行串接
        block = "\n".join([f"Field #{field_number}:"] + result_rows)
        output_blocks.append(block)
        field_number += 1

    # 題目要求不同 Field 之間要有一個空行
    return "\n\n".join(output_blocks)


def main() -> None:
    """命令列入口：讀 stdin、印 stdout。"""
    import sys

    input_data = sys.stdin.read()
    print(solve(input_data))


if __name__ == "__main__":
    main()
