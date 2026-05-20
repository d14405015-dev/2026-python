from __future__ import annotations

import importlib.util
import io
import math
import random
import sys
import unittest
from pathlib import Path
from typing import Callable, List, Sequence, Tuple

Segment = Tuple[int, int, int, int]
EPS = 1e-9
TWO_PI = 2.0 * math.pi


def _norm_angle(a: float) -> float:
    a %= TWO_PI
    if a < 0:
        a += TWO_PI
    return a


def _cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def ray_segment_distance(theta: float, seg: Segment) -> float | None:
    sx, sy, ex, ey = seg
    dx = math.cos(theta)
    dy = math.sin(theta)
    vx = ex - sx
    vy = ey - sy

    den = _cross(dx, dy, vx, vy)
    if abs(den) < EPS:
        return None

    t = _cross(sx, sy, vx, vy) / den
    u = _cross(sx, sy, dx, dy) / den

    if t < -EPS:
        return None
    if u < -EPS or u > 1 + EPS:
        return None

    return max(0.0, t)


def reference_visible_flags(segments: Sequence[Segment]) -> List[int]:
    n = len(segments)
    visible = [0] * n
    if not segments:
        return visible

    endpoint_angles: List[float] = []
    for sx, sy, ex, ey in segments:
        endpoint_angles.append(_norm_angle(math.atan2(sy, sx)))
        endpoint_angles.append(_norm_angle(math.atan2(ey, ex)))

    endpoint_angles.sort()
    sample_angles: List[float] = []
    delta = 1e-7

    for a in endpoint_angles:
        sample_angles.append(a)
        sample_angles.append(_norm_angle(a - delta))
        sample_angles.append(_norm_angle(a + delta))

    m = len(endpoint_angles)
    for i in range(m):
        a = endpoint_angles[i]
        b = endpoint_angles[(i + 1) % m]
        if i == m - 1:
            b += TWO_PI
        sample_angles.append(_norm_angle((a + b) * 0.5))

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


def build_input(cases: Sequence[Sequence[Segment]]) -> str:
    lines: List[str] = []
    for segs in cases:
        lines.append(str(len(segs)))
        for sx, sy, ex, ey in segs:
            lines.append(f"{sx} {sy} {ex} {ey}")
    return "\n".join(lines) + "\n"


def normalize_output_lines(text: str) -> List[str]:
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        lines.append(" ".join(s.split()))
    return lines


def _load_runner() -> Callable[[str], str]:
    path = Path(__file__).resolve().parent / "solution_11332-hand.py"
    if not path.exists():
        raise AssertionError("找不到 solution_11332-hand.py")

    spec = importlib.util.spec_from_file_location("student_solution_11332_hand", path)
    if spec is None or spec.loader is None:
        raise AssertionError("無法載入 solution_11332-hand.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for fn_name in ("solve", "process", "process_input"):
        fn = getattr(module, fn_name, None)
        if callable(fn):
            def runner(input_text: str, _fn=fn) -> str:
                result = _fn(input_text)
                if isinstance(result, str):
                    return result
                if isinstance(result, list):
                    return "\n".join(map(str, result))
                return str(result)

            return runner

    main_fn = getattr(module, "main", None)
    if callable(main_fn):
        def runner(input_text: str, _main=main_fn) -> str:
            old_stdin, old_stdout = sys.stdin, sys.stdout
            try:
                sys.stdin = io.StringIO(input_text)
                sys.stdout = io.StringIO()
                _main()
                return sys.stdout.getvalue()
            finally:
                sys.stdin, sys.stdout = old_stdin, old_stdout

        return runner

    raise AssertionError("找不到可測試介面")


class TestUVA11332Hand(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = _load_runner()

    def assert_cases(self, cases: Sequence[Sequence[Segment]]) -> None:
        expected_lines = []
        for segs in cases:
            expected_lines.append(" ".join(map(str, reference_visible_flags(segs))))
        actual_lines = normalize_output_lines(self.__class__.runner(build_input(cases)))
        self.assertEqual(actual_lines, expected_lines)

    def test_single_case_basic(self) -> None:
        case = [(1, -1, 1, 1), (2, -2, 2, 2), (-2, 1, -2, 3)]
        self.assert_cases([case])

    def test_two_cases_mixed(self) -> None:
        case1 = [(2, 1, 3, 1), (2, 2, 3, 2), (4, 1, 4, 3)]
        case2 = [(-3, -1, -2, -1), (-4, -2, -4, 1), (1, 3, 3, 3), (2, 1, 2, 4)]
        self.assert_cases([case1, case2])

    def test_random_small_non_intersecting_cases(self) -> None:
        rng = random.Random(11332)
        cases: List[List[Segment]] = []

        for _ in range(12):
            n = rng.randint(4, 10)
            segs: List[Segment] = []
            used_x = set()
            for _ in range(n):
                while True:
                    x = rng.randint(-30, 30)
                    if x == 0 or x in used_x:
                        continue
                    used_x.add(x)
                    break
                y1 = rng.randint(-25, 20)
                y2 = y1 + rng.randint(1, 8)
                segs.append((x, y1, x, y2))
            cases.append(segs)

        self.assert_cases(cases)


if __name__ == "__main__":
    unittest.main(verbosity=2)
