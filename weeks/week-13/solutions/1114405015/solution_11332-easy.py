"""UVA 11332 - 鏡子可見性判定（easy 版本）

題意（依目前題目敘述）：
- 某 M 站在原點 (0, 0)。
- 平面上有 n 條鏡子，每條鏡子是線段 (sx, sy) -> (ex, ey)。
- 鏡子之間不互相相交，且不會通過原點。
- 若某條鏡子的任意一小段可由原點直接看到（不考慮反射），就算可見。

這份 easy 版追求「好懂、好記」：
1. 先收集所有端點方向角。
2. 用關鍵角度發射射線（端點角、端點微擾、相鄰端點中點）。
3. 每條射線只會看見最前面的那條線段。
4. 被至少一條射線打到且在最前面的線段，即標記為可見（1），否則不可見（0）。

時間複雜度（單組）：
- 設線段數為 n，採樣角度約 O(n)
- 每個角度掃過所有線段 O(n)
- 總計約 O(n^2)

備註：
- 這是偏教學與可讀性的寫法，在小中型測資下很穩定。
"""

from __future__ import annotations

import math
import sys
from typing import List, Sequence, Tuple


Segment = Tuple[int, int, int, int]
EPS = 1e-9
TWO_PI = 2.0 * math.pi


def normalize_angle(angle: float) -> float:
    """把角度正規化到 [0, 2pi)。"""
    angle %= TWO_PI
    if angle < 0:
        angle += TWO_PI
    return angle


def cross(ax: float, ay: float, bx: float, by: float) -> float:
    """2D 向量外積。"""
    return ax * by - ay * bx


def ray_segment_distance(theta: float, seg: Segment) -> float | None:
    """計算「從原點出發、角度 theta 的射線」是否打到線段 seg。

    若有相交，回傳交點到原點的距離參數 t（非負）。
    若無相交，回傳 None。

    幾何方程：
    - 射線：R(t) = t * d, t >= 0
    - 線段：S(u) = s + u * v, 0 <= u <= 1
    聯立求解 t, u。
    """
    sx, sy, ex, ey = seg

    # 射線方向向量（單位向量）
    dx = math.cos(theta)
    dy = math.sin(theta)

    # 線段方向向量
    vx = ex - sx
    vy = ey - sy

    den = cross(dx, dy, vx, vy)
    if abs(den) < EPS:
        # 平行（或幾乎平行）視為不相交
        return None

    t = cross(sx, sy, vx, vy) / den
    u = cross(sx, sy, dx, dy) / den

    # t >= 0 代表在射線前方；0<=u<=1 代表在線段範圍內
    if t < -EPS:
        return None
    if u < -EPS or u > 1 + EPS:
        return None

    return max(0.0, t)


def visible_flags_for_case(segments: Sequence[Segment]) -> List[int]:
    """回傳每條線段是否可見（1/0）。"""
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

    # 1) 端點角及其微擾：捕捉臨界邊界附近可見性
    for a in endpoint_angles:
        sample_angles.append(a)
        sample_angles.append(normalize_angle(a - delta))
        sample_angles.append(normalize_angle(a + delta))

    # 2) 相鄰端點角中點：捕捉區間內一般方向
    m = len(endpoint_angles)
    for i in range(m):
        a = endpoint_angles[i]
        b = endpoint_angles[(i + 1) % m]
        if i == m - 1:
            b += TWO_PI
        mid = (a + b) * 0.5
        sample_angles.append(normalize_angle(mid))

    # 每條採樣射線挑出最近可交線段，即為該方向可見鏡子
    for theta in sample_angles:
        best_idx = -1
        best_dist = float("inf")

        for idx, seg in enumerate(segments):
            dist = ray_segment_distance(theta, seg)
            if dist is None:
                continue
            if dist < best_dist - 1e-8:
                best_dist = dist
                best_idx = idx

        if best_idx != -1:
            visible[best_idx] = 1

    return visible


def solve(input_text: str) -> str:
    """處理 EOF 多組輸入，輸出每組一行 0/1。"""
    nums = list(map(int, input_text.split()))
    if not nums:
        return ""

    idx = 0
    out_lines: List[str] = []

    while idx < len(nums):
        n = nums[idx]
        idx += 1

        segments: List[Segment] = []
        for _ in range(n):
            sx = nums[idx]
            sy = nums[idx + 1]
            ex = nums[idx + 2]
            ey = nums[idx + 3]
            idx += 4
            segments.append((sx, sy, ex, ey))

        flags = visible_flags_for_case(segments)
        out_lines.append(" ".join(map(str, flags)))

    return "\n".join(out_lines)


def main() -> None:
    """線上評測入口。"""
    data = sys.stdin.read()
    ans = solve(data)
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
