"""UVA 118 manual version.

Hand-typed style solution:
- English-only comments
- Simple, direct control flow
- Correct handling for LOST and scent behavior
"""

from __future__ import annotations

import sys


def main() -> None:
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    if not lines:
        return

    max_x, max_y = map(int, lines[0].split())

    dirs = ["N", "E", "S", "W"]
    move = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
    }

    # scent key: (x, y, direction)
    scents: set[tuple[int, int, str]] = set()

    out: list[str] = []
    i = 1

    while i + 1 < len(lines):
        x_s, y_s, d = lines[i].split()
        cmds = lines[i + 1]

        x = int(x_s)
        y = int(y_s)
        lost = False

        for c in cmds:
            if c == "L":
                d = dirs[(dirs.index(d) - 1) % 4]
                continue
            if c == "R":
                d = dirs[(dirs.index(d) + 1) % 4]
                continue

            # Forward
            dx, dy = move[d]
            nx = x + dx
            ny = y + dy

            if nx < 0 or nx > max_x or ny < 0 or ny > max_y:
                if (x, y, d) in scents:
                    # Ignore dangerous forward command due to scent.
                    continue
                scents.add((x, y, d))
                lost = True
                break

            x, y = nx, ny

        if lost:
            out.append(f"{x} {y} {d} LOST")
        else:
            out.append(f"{x} {y} {d}")

        i += 2

    if out:
        print("\n".join(out))


if __name__ == "__main__":
    main()
