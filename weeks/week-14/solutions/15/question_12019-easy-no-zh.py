"""UVA 12019 - Doom's Day Algorithm (-easy version)

Memorization-friendly idea:
- Use Python built-in datetime to get weekday directly.
- Keep the implementation short and straightforward.
"""

from __future__ import annotations

from datetime import date


def weekday_2012_easy(month: int, day: int) -> str:
    """Return weekday name for a date in year 2012."""
    return date(2012, month, day).strftime("%A")


def solve(data: str) -> str:
    """Parse input and print weekday names."""
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    out = []

    for i in range(1, t + 1):
        m, d = map(int, lines[i].split())
        out.append(weekday_2012_easy(m, d))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
