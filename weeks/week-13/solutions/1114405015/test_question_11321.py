"""UVA 11321 單元測試：逐次放置陷阱且不可封死左到右通路。

使用方式：
1. 將 11321 解答放在同資料夾，檔名建議為 solution_11321.py。
2. 解答可提供以下任一介面：
   - solve(input_text: str) -> str
   - process(input_text: str) -> str
   - process_input(input_text: str) -> str
   - main()（測試會模擬 stdin/stdout）
3. 執行：python -m unittest -v test_question_11321.py
"""

from __future__ import annotations

import importlib.util
import io
import random
import sys
import unittest
from collections import deque
from pathlib import Path
from typing import Callable, Iterable, List, Sequence, Tuple


Point = Tuple[int, int]


def has_left_to_right_path(n: int, m: int, blocked: set[Point]) -> bool:
    """檢查在目前障礙配置下，是否存在左欄到右欄的路徑。"""
    q: deque[Point] = deque()
    visited: set[Point] = set()

    # 所有左邊界可站立格子都可作為起點。
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


def reference_simulation(n: int, m: int, placements: Sequence[Point]) -> List[str]:
    """用參考邏輯模擬每次放陷阱，回傳應輸出序列。"""
    blocked: set[Point] = set()
    outputs: List[str] = []

    for p in placements:
        blocked.add(p)

        if has_left_to_right_path(n, m, blocked):
            outputs.append("<(_ _)>")
        else:
            # 若封死，該陷阱不成立，需回復狀態。
            blocked.remove(p)
            outputs.append(">_<")

    return outputs


def build_input(n: int, m: int, placements: Sequence[Point]) -> str:
    """組成題目輸入格式。"""
    lines = [f"{n} {m} {len(placements)}"]
    lines.extend(f"{x} {y}" for x, y in placements)
    return "\n".join(lines) + "\n"


def normalize_output_lines(text: str) -> List[str]:
    """正規化輸出行，只保留非空行。"""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _load_student_runner() -> Callable[[str], str]:
    """載入學生解答，回傳 runner(input_text) -> output_text。"""
    current_dir = Path(__file__).resolve().parent
    candidate_files = [
        "solution_11321-easy.py",
        "solution_11321-hand.py",
        "solution_11321.py",
        "question_11321.py",
        "uva_11321.py",
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
        raise AssertionError("找不到 11321 解答檔，請放置 solution_11321.py（或候選檔名）。")

    spec = importlib.util.spec_from_file_location("student_solution_11321", target_file)
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

    raise AssertionError(f"在 {target_file.name} 中找不到 solve/process/process_input/main 介面。")


class TestUVA11321(unittest.TestCase):
    """測試逐步放陷阱時的合法性判定。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = _load_student_runner()

    def assert_case(self, n: int, m: int, placements: Sequence[Point]) -> None:
        """比對學生輸出與參考模擬結果。"""
        input_text = build_input(n, m, placements)
        expected = reference_simulation(n, m, placements)
        actual = normalize_output_lines(self.__class__.runner(input_text))

        self.assertEqual(
            actual,
            expected,
            f"n={n}, m={m}, placements={list(placements)} 時輸出不符",
        )

    def test_single_row_simple_block(self) -> None:
        """單列情境：只要中間全被阻斷就會失敗。"""
        n, m = 1, 5
        placements = [(0, 1), (0, 2), (0, 3)]
        self.assert_case(n, m, placements)

    def test_small_grid_with_mix_results(self) -> None:
        """小型格子：同時涵蓋可放與不可放情況。"""
        n, m = 3, 4
        placements = [(0, 1), (1, 1), (2, 1), (1, 2), (0, 2)]
        self.assert_case(n, m, placements)

    def test_first_trap_can_be_rejected(self) -> None:
        """若第一個陷阱就封死，應直接回傳 >_<。"""
        n, m = 1, 2
        placements = [(0, 0)]
        self.assert_case(n, m, placements)

    def test_random_small_cases(self) -> None:
        """隨機小範圍回歸測試。"""
        rng = random.Random(11321)
        for _ in range(80):
            n = rng.randint(1, 6)
            m = rng.randint(1, 6)

            all_cells = [(x, y) for x in range(n) for y in range(m)]
            t = rng.randint(1, min(len(all_cells), 15))
            placements = rng.sample(all_cells, t)

            self.assert_case(n, m, placements)


if __name__ == "__main__":
    unittest.main(verbosity=2)
