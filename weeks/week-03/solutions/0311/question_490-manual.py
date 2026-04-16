"""UVA 490 manual version.

Hand-typed style implementation:
- English-only comments
- Straightforward 90-degree clockwise rotation
"""

from __future__ import annotations

import sys


def main() -> None:
    lines = sys.stdin.read().splitlines()
    if not lines:
        return

    width = max(len(s) for s in lines)
    padded = [s.ljust(width, " ") for s in lines]

    out: list[str] = []
    rows = len(padded)

    for c in range(width):
        chars: list[str] = []
        for r in range(rows - 1, -1, -1):
            chars.append(padded[r][c])
        out.append("".join(chars))

    print("\n".join(out) + "\n", end="")


if __name__ == "__main__":
    main()
