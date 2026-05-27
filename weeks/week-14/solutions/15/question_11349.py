"""UVA 11349 - Symmetric Matrix

標準版解法：
1. 先檢查是否有負數；只要出現負數就直接判定 Non-symmetric。
2. 再檢查中心對稱條件 M[i][j] == M[n-1-i][n-1-j]。
"""

from __future__ import annotations


def is_symmetric_matrix(matrix: list[list[int]]) -> bool:
    """檢查矩陣是否符合題目定義的對稱矩陣。"""
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            v = matrix[i][j]
            if v < 0:
                return False
            if v != matrix[n - 1 - i][n - 1 - j]:
                return False

    return True


def solve(data: str) -> str:
    """依 UVA 輸入格式解析，輸出每筆判斷結果。"""
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    idx = 1
    out = []

    for case_no in range(1, t + 1):
        # 本行格式類似: "N = 3"，取最後一個 token 即可取得 n
        n = int(lines[idx].split()[-1])
        idx += 1

        matrix = []
        for _ in range(n):
            row = list(map(int, lines[idx].split()))
            idx += 1
            matrix.append(row)

        result = "Symmetric." if is_symmetric_matrix(matrix) else "Non-symmetric."
        out.append(f"Test #{case_no}: {result}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
