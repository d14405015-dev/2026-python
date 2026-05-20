"""UVA 11332 單元測試：從原點可見的鏡子線段判定。

使用方式：
1. 將 11332 解答放在同資料夾，檔名建議為 solution_11332.py。
2. 解答可提供以下任一介面：
   - solve(input_text: str) -> str
   - process(input_text: str) -> str
   - process_input(input_text: str) -> str
   - visible_segments(cases)
   - main()（測試會模擬 stdin/stdout）
3. 執行：python -m unittest -v test_question_11332.py
"""

from __future__ import annotations

import importlib.util
import io
import math
import random
import sys
import unittest
from pathlib import Path
from typing import Callable, Iterable, List, Sequence, Tuple


Segment = Tuple[int, int, int, int]
EPS = 1e-9
TWO_PI = 2.0 * math.pi


def _norm_angle(a: float) -> float:
    """將角度正規化到 [0, 2pi)。"""
    a %= TWO_PI
    if a < 0:
        a += TWO_PI
    return a


def _cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def ray_segment_distance(theta: float, seg: Segment) -> float | None:
    """計算指定角度射線與線段交點距離。

    回傳：
    - 若相交，回傳從原點到交點的距離（沿射線方向參數 t）
    - 否則回傳 None
    """
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
    """參考幾何解：判斷每條線段是否至少有一小段可見。

    觀念：
    - 對多個關鍵角度發射射線。
    - 在該角度上，距離原點最近且被射線打到的線段即為可見。
    - 關鍵角度包含：所有端點角度、端點微小擾動、相鄰端點角度中點。
    """
    n = len(segments)
    visible = [0] * n

    endpoint_angles: List[float] = []
    for sx, sy, ex, ey in segments:
        endpoint_angles.append(_norm_angle(math.atan2(sy, sx)))
        endpoint_angles.append(_norm_angle(math.atan2(ey, ex)))

    if not endpoint_angles:
        return visible

    endpoint_angles = sorted(endpoint_angles)

    sample_angles: List[float] = []

    # 端點角度與其微擾角度：覆蓋臨界邊界附近情況。
    delta = 1e-7
    for a in endpoint_angles:
        sample_angles.append(a)
        sample_angles.append(_norm_angle(a - delta))
        sample_angles.append(_norm_angle(a + delta))

    # 相鄰端點角度的中點：覆蓋區間內一般位置。
    m = len(endpoint_angles)
    for i in range(m):
        a = endpoint_angles[i]
        b = endpoint_angles[(i + 1) % m]
        if i == m - 1:
            b += TWO_PI
        mid = (a + b) * 0.5
        sample_angles.append(_norm_angle(mid))

    # 每個角度選最近相交線段，標記為可見。
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


def build_input(cases: Sequence[Sequence[Segment]]) -> str:
    """組合成多組 EOF 結束的輸入格式。"""
    lines: List[str] = []
    for segments in cases:
        lines.append(str(len(segments)))
        for sx, sy, ex, ey in segments:
            lines.append(f"{sx} {sy} {ex} {ey}")
    return "\n".join(lines) + "\n"


def normalize_output_lines(text: str) -> List[str]:
    """正規化輸出：每行以單一空白分隔 0/1。"""
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        tokens = s.split()
        lines.append(" ".join(tokens))
    return lines


def _load_student_runner() -> Callable[[str], str]:
    """載入學生解答，回傳 runner(input_text) -> output_text。"""
    current_dir = Path(__file__).resolve().parent
    candidate_files = [
        "solution_11332-easy.py",
        "solution_11332-hand.py",
        "solution_11332.py",
        "question_11332.py",
        "uva_11332.py",
        "main.py",
        "solution.py",
    ]

    target_file = None
    for filename in candidate_files:
        path = current_dir / filename
        if path.exists():
            target_file = path
            break

    if target_file is None:
        raise AssertionError("找不到 11332 解答檔，請放置 solution_11332.py（或候選檔名）。")

    spec = importlib.util.spec_from_file_location("student_solution_11332", target_file)
    if spec is None or spec.loader is None:
        raise AssertionError(f"無法載入解答檔：{target_file.name}")

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

    # 若學生提供 visible_segments(cases) 介面，也可直接轉成輸出。
    vis_fn = getattr(module, "visible_segments", None)
    if callable(vis_fn):
        def runner(input_text: str, _fn=vis_fn) -> str:
            nums = list(map(int, input_text.split()))
            idx = 0
            cases: List[List[Segment]] = []
            while idx < len(nums):
                n = nums[idx]
                idx += 1
                segs: List[Segment] = []
                for _ in range(n):
                    sx, sy, ex, ey = nums[idx], nums[idx + 1], nums[idx + 2], nums[idx + 3]
                    idx += 4
                    segs.append((sx, sy, ex, ey))
                cases.append(segs)

            outputs = _fn(cases)
            lines = [" ".join(map(str, row)) for row in outputs]
            return "\n".join(lines)

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

    raise AssertionError(f"在 {target_file.name} 中找不到可測試介面。")


class TestUVA11332(unittest.TestCase):
    """驗證每組鏡子可見性輸出。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = _load_student_runner()

    def assert_cases(self, cases: Sequence[Sequence[Segment]]) -> None:
        """對多組測資進行比對。"""
        expected_lines = []
        for segs in cases:
            flags = reference_visible_flags(segs)
            expected_lines.append(" ".join(map(str, flags)))

        actual_text = self.__class__.runner(build_input(cases))
        actual_lines = normalize_output_lines(actual_text)

        self.assertEqual(actual_lines, expected_lines)

    def test_single_case_basic(self) -> None:
        """基本案例：前景線段遮擋後景線段。"""
        case = [
            (1, -1, 1, 1),
            (2, -2, 2, 2),
            (-2, 1, -2, 3),
        ]
        self.assert_cases([case])

    def test_two_cases_mixed(self) -> None:
        """一次測兩組，驗證 EOF 多組輸入處理。"""
        case1 = [
            (2, 1, 3, 1),
            (2, 2, 3, 2),
            (4, 1, 4, 3),
        ]
        case2 = [
            (-3, -1, -2, -1),
            (-4, -2, -4, 1),
            (1, 3, 3, 3),
            (2, 1, 2, 4),
        ]
        self.assert_cases([case1, case2])

    def test_random_small_non_intersecting_cases(self) -> None:
        """隨機小型測資回歸測試（利用平行垂直線段避免交叉）。"""
        rng = random.Random(11332)
        cases: List[List[Segment]] = []

        for _ in range(12):
            n = rng.randint(4, 10)
            segs: List[Segment] = []
            used_x = set()

            # 產生不相交垂直線段：同一 x 不重複，確保線段之間不相交。
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
