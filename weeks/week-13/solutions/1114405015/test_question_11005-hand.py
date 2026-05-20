from __future__ import annotations

import importlib.util
import random
import unittest
from pathlib import Path
from typing import Callable, Iterable, List


def digits_in_base(n: int, base: int) -> List[int]:
    if n == 0:
        return [0]
    digits: List[int] = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return list(reversed(digits))


def calc_cost(n: int, base: int, costs: List[int]) -> int:
    return sum(costs[d] for d in digits_in_base(n, base))


def brute_cheapest_bases(n: int, costs: List[int]) -> List[int]:
    all_costs = {base: calc_cost(n, base, costs) for base in range(2, 37)}
    min_cost = min(all_costs.values())
    return [base for base in range(2, 37) if all_costs[base] == min_cost]


def _load_student_callable() -> Callable[[List[int], int], Iterable[int]]:
    path = Path(__file__).resolve().parent / "solution_11005-hand.py"
    if not path.exists():
        raise AssertionError("找不到 solution_11005-hand.py")

    spec = importlib.util.spec_from_file_location("student_solution_11005_hand", path)
    if spec is None or spec.loader is None:
        raise AssertionError("無法載入 solution_11005-hand.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for fn_name in ["cheapest_bases", "find_cheapest_bases", "cheapest_bases_for_number"]:
        fn = getattr(module, fn_name, None)
        if callable(fn):
            return fn

    raise AssertionError("solution_11005-hand.py 中找不到可呼叫的解答函式")


class TestUVA11005CheapestBaseHand(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.student_fn = _load_student_callable()

    def assert_student_matches_bruteforce(self, costs: List[int], n: int) -> None:
        expected = brute_cheapest_bases(n, costs)
        actual = list(self.__class__.student_fn(costs, n))
        self.assertEqual(actual, sorted(set(actual)))
        self.assertTrue(all(2 <= b <= 36 for b in actual))
        self.assertEqual(actual, expected)

    def test_zero_should_tie_all_bases(self) -> None:
        costs = [i % 7 + 1 for i in range(36)]
        self.assert_student_matches_bruteforce(costs, 0)

    def test_uniform_costs_prefers_short_representation(self) -> None:
        costs = [1] * 36
        self.assert_student_matches_bruteforce(costs, 10)
        self.assert_student_matches_bruteforce(costs, 2000000000)

    def test_custom_costs_with_tie(self) -> None:
        costs = [5] * 36
        costs[1] = 1
        costs[10] = 1
        self.assert_student_matches_bruteforce(costs, 10)
        self.assert_student_matches_bruteforce(costs, 101)

    def test_random_small_cases_against_bruteforce(self) -> None:
        rng = random.Random(11005)
        for _ in range(120):
            costs = [rng.randint(1, 20) for _ in range(36)]
            n = rng.randint(0, 50000)
            self.assert_student_matches_bruteforce(costs, n)


if __name__ == "__main__":
    unittest.main(verbosity=2)
