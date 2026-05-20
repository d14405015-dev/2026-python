from __future__ import annotations

import importlib.util
import io
import random
import re
import sys
import unittest
from pathlib import Path
from typing import Callable, List, Sequence, Set


def brute_min_stones(L: int, S: int, T: int, stones: Sequence[int]) -> int:
    stone_set: Set[int] = set(stones)
    max_pos = L + T
    inf = 10**9
    dp = [inf] * (max_pos + 1)
    dp[0] = 0

    for pos in range(max_pos + 1):
        if dp[pos] == inf or pos >= L:
            continue
        for step in range(S, T + 1):
            nxt = pos + step
            if nxt > max_pos:
                continue
            cost = 1 if (nxt <= L and nxt in stone_set) else 0
            dp[nxt] = min(dp[nxt], dp[pos] + cost)

    return min(dp[L : L + T + 1])


def build_input(L: int, S: int, T: int, stones: Sequence[int]) -> str:
    return f"{L}\n{S} {T} {len(stones)}\n{' '.join(map(str, stones))}\n"


def parse_output_to_int(text: str) -> int:
    m = re.search(r"-?\d+", text)
    if not m:
        raise AssertionError(f"輸出中找不到整數答案：{text!r}")
    return int(m.group())


def _load_solver() -> Callable[[int, int, int, Sequence[int]], int]:
    path = Path(__file__).resolve().parent / "solution_11150-hand.py"
    if not path.exists():
        raise AssertionError("找不到 solution_11150-hand.py")

    spec = importlib.util.spec_from_file_location("student_solution_11150_hand", path)
    if spec is None or spec.loader is None:
        raise AssertionError("無法載入 solution_11150-hand.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for fn_name in ["min_stones", "minimal_stones", "solve_case"]:
        fn = getattr(module, fn_name, None)
        if callable(fn):
            def solver(L: int, S: int, T: int, stones: Sequence[int], _fn=fn) -> int:
                v = _fn(L, S, T, list(stones))
                return int(v)

            return solver

    for fn_name in ["solve", "process", "process_input"]:
        fn = getattr(module, fn_name, None)
        if callable(fn):
            def solver(L: int, S: int, T: int, stones: Sequence[int], _fn=fn) -> int:
                text = str(_fn(build_input(L, S, T, stones)))
                return parse_output_to_int(text)

            return solver

    main_fn = getattr(module, "main", None)
    if callable(main_fn):
        def solver(L: int, S: int, T: int, stones: Sequence[int], _main=main_fn) -> int:
            old_stdin, old_stdout = sys.stdin, sys.stdout
            try:
                sys.stdin = io.StringIO(build_input(L, S, T, stones))
                sys.stdout = io.StringIO()
                _main()
                return parse_output_to_int(sys.stdout.getvalue())
            finally:
                sys.stdin, sys.stdout = old_stdin, old_stdout

        return solver

    raise AssertionError("找不到可測試介面")


class TestUVA11150Hand(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.solver = _load_solver()

    def assert_case(self, L: int, S: int, T: int, stones: Sequence[int]) -> None:
        expected = brute_min_stones(L, S, T, stones)
        actual = self.__class__.solver(L, S, T, stones)
        self.assertEqual(actual, expected)

    def test_deterministic_jump(self) -> None:
        self.assert_case(20, 4, 4, [4, 7, 8, 12, 16, 19])

    def test_can_avoid_all_stones(self) -> None:
        self.assert_case(12, 2, 3, [2, 5, 8, 11])

    def test_must_step_some_stones(self) -> None:
        self.assert_case(15, 3, 5, [3, 6, 7, 9, 12, 14])

    def test_random_small_cases(self) -> None:
        rng = random.Random(11150)
        for _ in range(120):
            L = rng.randint(8, 40)
            S = rng.randint(1, 6)
            T = rng.randint(S, 8)
            m = rng.randint(1, min(10, L - 1))
            stones = sorted(rng.sample(range(1, L), m))
            self.assert_case(L, S, T, stones)


if __name__ == "__main__":
    unittest.main(verbosity=2)
