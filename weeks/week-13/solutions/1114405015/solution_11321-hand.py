from __future__ import annotations

from collections import deque
from typing import List, Set, Tuple
import sys

Point = Tuple[int, int]


def has_path_left_to_right(n: int, m: int, blocked: Set[Point]) -> bool:
    q: deque[Point] = deque()
    visited: Set[Point] = set()

    for x in range(n):
        p = (x, 0)
        if p not in blocked:
            q.append(p)
            visited.add(p)

    if not q:
        return False

    while q:
        x, y = q.popleft()
        if y == m - 1:
            return True

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            np = (nx, ny)
            if 0 <= nx < n and 0 <= ny < m and np not in blocked and np not in visited:
                visited.add(np)
                q.append(np)

    return False


def solve(input_text: str) -> str:
    nums = list(map(int, input_text.split()))
    if not nums:
        return ""

    idx = 0
    n, m, t = nums[idx], nums[idx + 1], nums[idx + 2]
    idx += 3

    blocked: Set[Point] = set()
    out_lines: List[str] = []

    for _ in range(t):
        x, y = nums[idx], nums[idx + 1]
        idx += 2

        p = (x, y)
        blocked.add(p)

        if has_path_left_to_right(n, m, blocked):
            out_lines.append("<(_ _)>")
        else:
            blocked.remove(p)
            out_lines.append(">_<")

    return "\n".join(out_lines)


def main() -> None:
    data = sys.stdin.read()
    out = solve(data)
    if out:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
