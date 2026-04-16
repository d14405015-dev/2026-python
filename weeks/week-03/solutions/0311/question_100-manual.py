"""UVA 100 manual version.

This file is intended to represent a hand-typed solution:
- Simple structure
- English-only comments
- Correct output format for UVA 100
"""

from __future__ import annotations

import sys


def cycle_length(n: int, memo: dict[int, int]) -> int:
    """Return Collatz cycle length for n, counting both n and 1."""
    if n in memo:
        return memo[n]

    path: list[int] = []
    x = n

    # Walk forward until we hit a value already in memo.
    while x not in memo:
        path.append(x)
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1

    # Backfill memo from the known tail.
    length = memo[x]
    for value in reversed(path):
        length += 1
        memo[value] = length

    return memo[n]


def main() -> None:
    """Read all input pairs and print i j maxCycleLength per line."""
    memo = {1: 1}

    for raw in sys.stdin.read().splitlines():
        line = raw.strip()
        if not line:
            continue

        i_str, j_str = line.split()
        i = int(i_str)
        j = int(j_str)

        left = min(i, j)
        right = max(i, j)

        best = 0
        for value in range(left, right + 1):
            current = cycle_length(value, memo)
            if current > best:
                best = current

        print(i, j, best)


if __name__ == "__main__":
    main()
