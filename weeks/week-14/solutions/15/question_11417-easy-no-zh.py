"""UVA 11417 - GCD (-easy version)

Memorization-friendly idea:
- Follow the formula directly with two loops.
- Sum gcd(i, j) for all 1 <= i < j <= N.
"""

from __future__ import annotations

from math import gcd


def gcd_sum_direct(n: int) -> int:
    """Compute G(n) directly by definition."""
    total = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total += gcd(i, j)
    return total


def solve(data: str) -> str:
    """Read N values line by line and stop at 0."""
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        n = int(line)
        if n == 0:
            break

        out.append(str(gcd_sum_direct(n)))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
