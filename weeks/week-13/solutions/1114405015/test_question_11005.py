"""UVA 11005 Cheapest Base 單元測試

使用方式：
1. 將你的解答程式放在同一資料夾，檔名建議為 solution_11005-easy.py。
2. 解答需提供以下任一函式：
   - cheapest_bases(costs, n)
   - find_cheapest_bases(costs, n)
   - cheapest_bases_for_number(costs, n)
3. 執行：python -m unittest -v test_question_11005.py
"""

from __future__ import annotations

import importlib.util
import random
import unittest
from pathlib import Path
from typing import Callable, Iterable, List


def digits_in_base(n: int, base: int) -> List[int]:
    """將十進位整數 n 轉為 base 進位的數字陣列（最低位在後）。"""
    if n == 0:
        return [0]

    digits: List[int] = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return list(reversed(digits))


def calc_cost(n: int, base: int, costs: List[int]) -> int:
    """計算數字 n 在指定進位 base 的總印刷成本。"""
    return sum(costs[d] for d in digits_in_base(n, base))


def brute_cheapest_bases(n: int, costs: List[int]) -> List[int]:
    """以暴力法找出成本最低的進位，作為測試標準答案。"""
    all_costs = {base: calc_cost(n, base, costs) for base in range(2, 37)}
    min_cost = min(all_costs.values())
    return [base for base in range(2, 37) if all_costs[base] == min_cost]


def _load_student_callable() -> Callable[[List[int], int], Iterable[int]]:
    """嘗試從同資料夾載入學生解答函式。

    這裡做了多種檔名與函式名的相容，降低對你實作命名的限制。
    """
    current_dir = Path(__file__).resolve().parent
    candidate_files = [
        "solution_11005-easy.py",
        "solution_11005.py",
        "question_11005.py",
        "uva_11005.py",
        "main.py",
        "solution.py",
    ]
    candidate_functions = [
        "cheapest_bases",
        "find_cheapest_bases",
        "cheapest_bases_for_number",
    ]

    for filename in candidate_files:
        path = current_dir / filename
        if not path.exists():
            continue

        spec = importlib.util.spec_from_file_location("student_solution_11005", path)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for fn_name in candidate_functions:
            fn = getattr(module, fn_name, None)
            if callable(fn):
                return fn

    raise AssertionError(
        "找不到可測試的解答函式。請在同資料夾提供 solution_11005.py（或其他候選檔名），"
        "並實作 cheapest_bases(costs, n) 或 find_cheapest_bases(costs, n)。"
    )


class TestUVA11005CheapestBase(unittest.TestCase):
    """針對 UVA 11005 的核心邏輯測試。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.student_fn = _load_student_callable()

    def assert_student_matches_bruteforce(self, costs: List[int], n: int) -> None:
        """比對學生函式結果與暴力基準，並檢查格式合法性。"""
        expected = brute_cheapest_bases(n, costs)
        # 透過類別屬性取用函式，避免被 instance 綁成 method 而多出 self 參數。
        actual = list(self.__class__.student_fn(costs, n))

        # 基本格式檢查：必須是排序後、無重複、合法範圍內的進位
        self.assertEqual(actual, sorted(set(actual)), "回傳進位需為遞增且不可重複")
        self.assertTrue(all(2 <= b <= 36 for b in actual), "進位範圍必須在 2 到 36")

        self.assertEqual(
            actual,
            expected,
            f"數字 {n} 的最低成本進位不正確，期望 {expected}，實得 {actual}",
        )

    def test_zero_should_tie_all_bases(self) -> None:
        """N=0 時所有進位表示皆為 0，成本應完全相同。"""
        costs = [i % 7 + 1 for i in range(36)]
        self.assert_student_matches_bruteforce(costs, 0)

    def test_uniform_costs_prefers_short_representation(self) -> None:
        """所有字元成本相同時，位數越少越便宜（通常偏向較大進位）。"""
        costs = [1] * 36
        self.assert_student_matches_bruteforce(costs, 10)
        self.assert_student_matches_bruteforce(costs, 2000000000)

    def test_custom_costs_with_tie(self) -> None:
        """自訂成本，檢查多個進位並列最便宜的情況。"""
        costs = [5] * 36
        # 讓 digit 1 和 digit A(10) 比較便宜，製造不同進位可能出現平手
        costs[1] = 1
        costs[10] = 1
        self.assert_student_matches_bruteforce(costs, 10)
        self.assert_student_matches_bruteforce(costs, 101)

    def test_random_small_cases_against_bruteforce(self) -> None:
        """隨機小型測資回歸測試，強化正確性信心。"""
        rng = random.Random(11005)
        for _ in range(120):
            costs = [rng.randint(1, 20) for _ in range(36)]
            n = rng.randint(0, 50000)
            self.assert_student_matches_bruteforce(costs, n)


if __name__ == "__main__":
    unittest.main(verbosity=2)
