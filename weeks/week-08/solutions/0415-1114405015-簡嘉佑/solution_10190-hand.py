from typing import List, Tuple


def solve(input_data: str) -> str:
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    if not lines:
        return "0.00"

    n, w, t, v = map(int, lines[0].split())

    intervals: List[Tuple[int, int]] = []
    for i in range(1, n + 1):
        x, l, _speed = map(int, lines[i].split())
        left = max(0, x)
        right = min(w, x + l)
        if left < right:
            intervals.append((left, right))

    if not intervals:
        return f"{w * t * v:.2f}"

    intervals.sort()

    covered = 0
    cur_l, cur_r = intervals[0]
    for l, r in intervals[1:]:
        if l <= cur_r:
            cur_r = max(cur_r, r)
        else:
            covered += cur_r - cur_l
            cur_l, cur_r = l, r

    covered += cur_r - cur_l

    uncovered = max(0, w - covered)
    volume = uncovered * t * v
    return f"{volume:.2f}"


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
