"""UVA 11461 - Square Numbers (-easy version)

Memorization-friendly idea:
- Start from ceil(sqrt(a)).
- Enumerate x^2 while x^2 <= b.
"""

from __future__ import annotations

from math import isqrt


def count_squares_easy(a: int, b: int) -> int:
    """Count perfect squares in [a, b] by direct enumeration."""
    start = isqrt(a)
    if start * start < a:
        start += 1

    cnt = 0
    x = start
    while x * x <= b:
        cnt += 1
        x += 1

    return cnt


def solve(data: str) -> str:
    """Parse multiple ranges and output counts."""
    out = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        out.append(str(count_squares_easy(a, b)))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
