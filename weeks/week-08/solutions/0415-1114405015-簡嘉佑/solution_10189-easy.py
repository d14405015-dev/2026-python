from typing import List


# 這份 -easy 版本把流程拆得更直覺：
# 1) 先把地圖做成可修改的二維陣列（地雷先保留為 *，空白先放 0）
# 2) 走訪每一顆地雷，把周圍 8 格的數字加一
# 這種寫法記憶點是「由地雷去影響鄰居」，通常比「每格回頭掃 8 格」更好記。

def solve(input_data: str) -> str:
    lines = input_data.splitlines()
    i = 0
    case_no = 1
    blocks: List[str] = []

    # 八方向位移（row, col）
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    while i < len(lines):
        header = lines[i].strip()
        i += 1

        if not header:
            # 若輸入中夾雜空行，直接略過
            continue

        n, m = map(int, header.split())
        if n == 0 and m == 0:
            break

        raw = [lines[i + r].rstrip("\n") for r in range(n)]
        i += n

        # ans 先建立為可修改結構：
        # 地雷格放 "*"，空白格放 0（整數）
        ans = [["*" if raw[r][c] == "*" else 0 for c in range(m)] for r in range(n)]

        # 每遇到一顆地雷，就把它周圍所有非地雷格 +1
        for r in range(n):
            for c in range(m):
                if raw[r][c] != "*":
                    continue

                for dr, dc in dirs:
                    nr = r + dr
                    nc = c + dc

                    # 邊界內且不是地雷才可加一
                    if 0 <= nr < n and 0 <= nc < m and ans[nr][nc] != "*":
                        ans[nr][nc] += 1

        # 把每列轉成字串，數字要轉成字元
        rows = ["".join(str(cell) for cell in ans[r]) for r in range(n)]
        blocks.append("\n".join([f"Field #{case_no}:"] + rows))
        case_no += 1

    return "\n\n".join(blocks)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
