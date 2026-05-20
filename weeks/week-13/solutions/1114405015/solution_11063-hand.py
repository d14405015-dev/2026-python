from __future__ import annotations

import sys
from typing import List, Tuple


def rgb_to_xyz(r: int, g: int, b: int) -> Tuple[float, float, float]:
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    return x, y, z


def solve(input_text: str) -> str:
    tokens = list(map(int, input_text.split()))
    if not tokens:
        return ""

    n = tokens[0]
    idx = 1
    total_pixels = n * n
    y_sum = 0.0
    out_lines: List[str] = []

    for _ in range(total_pixels):
        r = tokens[idx]
        g = tokens[idx + 1]
        b = tokens[idx + 2]
        idx += 3
        x, y, z = rgb_to_xyz(r, g, b)
        y_sum += y
        out_lines.append(f"{x:.4f} {y:.4f} {z:.4f}")

    out_lines.append(f"The average of Y is {y_sum / total_pixels:.4f}")
    return "\n".join(out_lines)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
