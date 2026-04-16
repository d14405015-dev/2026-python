"""UVA 299 manual version.

Hand-typed style implementation:
- English-only comments
- Simple bubble-sort swap counter
"""

from __future__ import annotations

import sys


def count_swaps(arr: list[int]) -> int:
    """Count adjacent swaps needed to sort the list."""
    a = arr[:]
    n = len(a)
    swaps = 0

    for i in range(n):
        changed = False
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                changed = True
        if not changed:
            break

    return swaps


def main() -> None:
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip() != ""]
    if not lines:
        return

    t = int(lines[0])
    idx = 1
    out: list[str] = []

    for _ in range(t):
        l = int(lines[idx])
        idx += 1

        if l == 0:
            out.append("Optimal train swapping takes 0 swaps.")
            continue

        arr = list(map(int, lines[idx].split()))
        idx += 1

        s = count_swaps(arr)
        out.append(f"Optimal train swapping takes {s} swaps.")

    print("\n".join(out))


if __name__ == "__main__":
    main()
