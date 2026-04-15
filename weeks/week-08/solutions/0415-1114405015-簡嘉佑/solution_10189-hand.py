from typing import List


def solve(input_data: str) -> str:
    lines = input_data.splitlines()
    i = 0
    field_no = 1
    blocks: List[str] = []

    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    while i < len(lines):
        header = lines[i].strip()
        i += 1

        if not header:
            continue

        n, m = map(int, header.split())
        if n == 0 and m == 0:
            break

        grid = [lines[i + r].rstrip("\n") for r in range(n)]
        i += n

        out = [["*" if grid[r][c] == "*" else 0 for c in range(m)] for r in range(n)]

        for r in range(n):
            for c in range(m):
                if grid[r][c] != "*":
                    continue
                for dr, dc in dirs:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < n and 0 <= nc < m and out[nr][nc] != "*":
                        out[nr][nc] += 1

        rows = ["".join(str(cell) for cell in out[r]) for r in range(n)]
        blocks.append("\n".join([f"Field #{field_no}:"] + rows))
        field_no += 1

    return "\n\n".join(blocks)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
