from __future__ import annotations

import math
import sys
from typing import List, Sequence, Tuple

Segment = Tuple[int, int, int, int]
EPS = 1e-9
TWO_PI = 2.0 * math.pi


def normalize_angle(angle: float) -> float:
    angle %= TWO_PI
    if angle < 0:
        angle += TWO_PI
    return angle


def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def ray_segment_distance(theta: float, seg: Segment) -> float | None:
    sx, sy, ex, ey = seg
    dx = math.cos(theta)
    dy = math.sin(theta)
    vx = ex - sx
    vy = ey - sy

    den = cross(dx, dy, vx, vy)
    if abs(den) < EPS:
        return None

    t = cross(sx, sy, vx, vy) / den
    u = cross(sx, sy, dx, dy) / den

    if t < -EPS:
        return None
    if u < -EPS or u > 1 + EPS:
        return None

    return max(0.0, t)


def visible_flags_for_case(segments: Sequence[Segment]) -> List[int]:
    n = len(segments)
    visible = [0] * n
    if n == 0:
        return visible

    endpoint_angles: List[float] = []
    for sx, sy, ex, ey in segments:
        endpoint_angles.append(normalize_angle(math.atan2(sy, sx)))
        endpoint_angles.append(normalize_angle(math.atan2(ey, ex)))

    endpoint_angles.sort()

    sample_angles: List[float] = []
    delta = 1e-7
    for a in endpoint_angles:
        sample_angles.append(a)
        sample_angles.append(normalize_angle(a - delta))
        sample_angles.append(normalize_angle(a + delta))

    m = len(endpoint_angles)
    for i in range(m):
        a = endpoint_angles[i]
        b = endpoint_angles[(i + 1) % m]
        if i == m - 1:
            b += TWO_PI
        sample_angles.append(normalize_angle((a + b) * 0.5))

    for theta in sample_angles:
        best_idx = -1
        best_dist = float("inf")
        for idx, seg in enumerate(segments):
            d = ray_segment_distance(theta, seg)
            if d is None:
                continue
            if d < best_dist - 1e-8:
                best_dist = d
                best_idx = idx
        if best_idx != -1:
            visible[best_idx] = 1

    return visible


def solve(input_text: str) -> str:
    nums = list(map(int, input_text.split()))
    if not nums:
        return ""

    idx = 0
    out_lines: List[str] = []
    while idx < len(nums):
        n = nums[idx]
        idx += 1
        segs: List[Segment] = []
        for _ in range(n):
            sx, sy, ex, ey = nums[idx], nums[idx + 1], nums[idx + 2], nums[idx + 3]
            idx += 4
            segs.append((sx, sy, ex, ey))
        out_lines.append(" ".join(map(str, visible_flags_for_case(segs))))

    return "\n".join(out_lines)


def main() -> None:
    data = sys.stdin.read()
    out = solve(data)
    if out:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
