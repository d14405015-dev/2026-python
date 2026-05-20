from __future__ import annotations

import importlib.util
import io
import random
import sys
import unittest
from collections import deque
from pathlib import Path
from typing import Callable, List, Sequence, Tuple

Point = Tuple[int, int]


def has_left_to_right_path(n: int, m: int, blocked: set[Point]) -> bool:
    q: deque[Point] = deque()
    visited: set[Point] = set()

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
    blocked: set[Point] = set()
    outputs: List[str] = []

    for p in placements:
        blocked.add(p)
        if has_left_to_right_path(n, m, blocked):
            outputs.append("<(_ _)>")
        else:
            blocked.remove(p)
            outputs.append(">_<")

    return outputs


def build_input(n: int, m: int, placements: Sequence[Point]) -> str:
    lines = [f"{n} {m} {len(placements)}"]
    lines.extend(f"{x} {y}" for x, y in placements)
    return "\n".join(lines) + "\n"


def normalize_output_lines(text: str) -> List[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _load_runner() -> Callable[[str], str]:
    path = Path(__file__).resolve().parent / "solution_11321-hand.py"
    if not path.exists():
        raise AssertionError("找不到 solution_11321-hand.py")

    spec = importlib.util.spec_from_file_location("student_solution_11321_hand", path)
    if spec is None or spec.loader is None:
        raise AssertionError("無法載入 solution_11321-hand.py")

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


class TestUVA11321Hand(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = _load_runner()

    def assert_case(self, n: int, m: int, placements: Sequence[Point]) -> None:
        expected = reference_simulation(n, m, placements)
        actual = normalize_output_lines(self.__class__.runner(build_input(n, m, placements)))
        self.assertEqual(actual, expected)

    def test_single_row_simple_block(self) -> None:
        self.assert_case(1, 5, [(0, 1), (0, 2), (0, 3)])

    def test_small_grid_with_mix_results(self) -> None:
        self.assert_case(3, 4, [(0, 1), (1, 1), (2, 1), (1, 2), (0, 2)])

    def test_first_trap_can_be_rejected(self) -> None:
        self.assert_case(1, 2, [(0, 0)])

    def test_random_small_cases(self) -> None:
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
