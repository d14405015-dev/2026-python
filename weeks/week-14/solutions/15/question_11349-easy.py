"""UVA 11349 - Symmetric Matrix（-easy 版本）

好記版本重點：
- 每看一個位置 (i, j)，就和它的鏡像位置 (n-1-i, n-1-j) 比較。
- 同時檢查值不能是負數。
- 條件任一不符就立即回傳 False。
"""

from __future__ import annotations


def is_symmetric_matrix_easy(matrix: list[list[int]]) -> bool:
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                return False
            if matrix[i][j] != matrix[n - 1 - i][n - 1 - j]:
                return False

    return True


def solve(data: str) -> str:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    pos = 1
    out = []

    for case_no in range(1, t + 1):
        n = int(lines[pos].split()[-1])
        pos += 1

        matrix = []
        for _ in range(n):
            matrix.append(list(map(int, lines[pos].split())))
            pos += 1

        if is_symmetric_matrix_easy(matrix):
            out.append(f"Test #{case_no}: Symmetric.")
        else:
            out.append(f"Test #{case_no}: Non-symmetric.")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
