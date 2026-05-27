"""UVA 11349 - Symmetric Matrix (-easy version)

Memorization-friendly idea:
- For each cell (i, j), compare with mirrored cell (n-1-i, n-1-j).
- Also ensure values are non-negative.
"""

from __future__ import annotations


def is_symmetric_matrix_easy(matrix: list[list[int]]) -> bool:
    """Check matrix by center symmetry rule in the problem."""
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                return False
            if matrix[i][j] != matrix[n - 1 - i][n - 1 - j]:
                return False

    return True


def solve(data: str) -> str:
    """Parse UVA input format and return verdicts per test case."""
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
