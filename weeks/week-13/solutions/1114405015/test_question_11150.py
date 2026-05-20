"""UVA 11150 單元測試：過橋最少踩石子數。

使用方式：
1. 將 11150 解答放在同資料夾，檔名建議為 solution_11150.py。
2. 解答可提供以下任一介面：
   - min_stones(L, S, T, stones)
   - minimal_stones(L, S, T, stones)
   - solve_case(L, S, T, stones)
   - solve(input_text) / process(input_text) / process_input(input_text)
   - main()（測試會模擬 stdin/stdout）
3. 執行：python -m unittest -v test_question_11150.py
"""

from __future__ import annotations

import importlib.util
import io
import random
import re
import sys
import unittest
from pathlib import Path
from typing import Callable, Iterable, List, Sequence, Set


def brute_min_stones(L: int, S: int, T: int, stones: Sequence[int]) -> int:
    """以暴力 DP 計算最少踩石子數（作為測試標準答案）。"""
    stone_set: Set[int] = set(stones)

    # 青蛙只要跳到或超過 L 即過河，因此狀態開到 L+T 即可。
    max_pos = L + T
    inf = 10**9
    dp = [inf] * (max_pos + 1)
    dp[0] = 0

    for pos in range(max_pos + 1):
        if dp[pos] == inf:
            continue
        if pos >= L:
            continue

        for step in range(S, T + 1):
            nxt = pos + step
            if nxt > max_pos:
                continue

            # 只有落在橋上（<=L）時才可能踩到石子。
            cost = 1 if (nxt <= L and nxt in stone_set) else 0
            dp[nxt] = min(dp[nxt], dp[pos] + cost)

    return min(dp[L : L + T + 1])


def build_input(L: int, S: int, T: int, stones: Sequence[int]) -> str:
    """組合成題目輸入格式（單筆測資）。"""
    m = len(stones)
    return f"{L}\n{S} {T} {m}\n{' '.join(map(str, stones))}\n"


def parse_output_to_int(text: str) -> int:
    """從解答輸出抓第一個整數答案。"""
    m = re.search(r"-?\d+", text)
    if not m:
        raise AssertionError(f"輸出中找不到整數答案：{text!r}")
    return int(m.group())


def _load_student_solver() -> Callable[[int, int, int, Sequence[int]], int]:
    """載入學生解答，回傳統一介面 solver(L, S, T, stones) -> int。"""
    current_dir = Path(__file__).resolve().parent
    candidate_files = [
        "solution_11150-easy.py",
        "solution_11150-hand.py",
        "solution_11150.py",
        "question_11150.py",
        "uva_11150.py",
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
        raise AssertionError("找不到 11150 解答檔，請放置 solution_11150.py（或候選檔名）。")

    spec = importlib.util.spec_from_file_location("student_solution_11150", target_file)
    if spec is None or spec.loader is None:
        raise AssertionError(f"無法載入解答檔：{target_file.name}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 優先使用直接函式介面，避免 I/O 影響測試穩定度。
    for fn_name in ["min_stones", "minimal_stones", "solve_case"]:
        fn = getattr(module, fn_name, None)
        if callable(fn):
            def solver(L: int, S: int, T: int, stones: Sequence[int], _fn=fn) -> int:
                value = _fn(L, S, T, list(stones))
                if isinstance(value, int):
                    return value
                return int(value)

            return solver

    # 次選文字介面：solve/process/process_input。
    for fn_name in ["solve", "process", "process_input"]:
        fn = getattr(module, fn_name, None)
        if callable(fn):
            def solver(L: int, S: int, T: int, stones: Sequence[int], _fn=fn) -> int:
                input_text = build_input(L, S, T, stones)
                result = _fn(input_text)
                if isinstance(result, list):
                    result_text = "\n".join(map(str, result))
                else:
                    result_text = str(result)
                return parse_output_to_int(result_text)

            return solver

    # 最後相容 main()：模擬標準輸入輸出。
    main_fn = getattr(module, "main", None)
    if callable(main_fn):
        def solver(L: int, S: int, T: int, stones: Sequence[int], _main=main_fn) -> int:
            input_text = build_input(L, S, T, stones)
            old_stdin, old_stdout = sys.stdin, sys.stdout
            try:
                sys.stdin = io.StringIO(input_text)
                sys.stdout = io.StringIO()
                _main()
                return parse_output_to_int(sys.stdout.getvalue())
            finally:
                sys.stdin, sys.stdout = old_stdin, old_stdout

        return solver

    raise AssertionError(f"在 {target_file.name} 找不到可測試的函式或 main()")


class TestUVA11150(unittest.TestCase):
    """驗證最少踩石子數的正確性。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.solver = _load_student_solver()

    def assert_case(self, L: int, S: int, T: int, stones: Sequence[int]) -> None:
        """比對學生輸出與暴力 DP 標準答案。"""
        expected = brute_min_stones(L, S, T, stones)
        actual = self.__class__.solver(L, S, T, stones)
        self.assertEqual(
            actual,
            expected,
            f"L={L}, S={S}, T={T}, stones={list(stones)} 時答案錯誤",
        )

    def test_deterministic_jump(self) -> None:
        """S=T 時跳距固定，路徑唯一，容易人工驗證。"""
        L, S, T = 20, 4, 4
        stones = [4, 7, 8, 12, 16, 19]
        self.assert_case(L, S, T, stones)

    def test_can_avoid_all_stones(self) -> None:
        """存在不踩任何石子的路徑。"""
        L, S, T = 12, 2, 3
        stones = [2, 5, 8, 11]
        self.assert_case(L, S, T, stones)

    def test_must_step_some_stones(self) -> None:
        """設計需要至少踩到部分石子的情況。"""
        L, S, T = 15, 3, 5
        stones = [3, 6, 7, 9, 12, 14]
        self.assert_case(L, S, T, stones)

    def test_random_small_cases(self) -> None:
        """小範圍隨機測資，使用暴力 DP 回歸測試。"""
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
