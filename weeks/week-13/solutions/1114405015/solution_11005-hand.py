from __future__ import annotations

import sys
from typing import List


def representation_cost(costs: List[int], n: int, base: int) -> int:
    if n == 0:
        return costs[0]
    total = 0
    while n > 0:
        total += costs[n % base]
        n //= base
    return total


def cheapest_bases(costs: List[int], n: int) -> List[int]:
    best_cost = None
    best_bases: List[int] = []
    for base in range(2, 37):
        c = representation_cost(costs, n, base)
        if best_cost is None or c < best_cost:
            best_cost = c
            best_bases = [base]
        elif c == best_cost:
            best_bases.append(base)
    return best_bases


def parse_input(text: str) -> List[str]:
    nums = list(map(int, text.split()))
    if not nums:
        return []
    t = nums[0]
    idx = 1
    out: List[str] = []
    for case_no in range(1, t + 1):
        costs = nums[idx:idx + 36]
        idx += 36
        q = nums[idx]
        idx += 1
        out.append(f"Case {case_no}:")
        for _ in range(q):
            n = nums[idx]
            idx += 1
            bases = cheapest_bases(costs, n)
            out.append(f"Cheapest base(s) for number {n}: {' '.join(map(str, bases))}")
        if case_no != t:
            out.append("")
    return out


def main() -> None:
    data = sys.stdin.read()
    lines = parse_input(data)
    if lines:
        sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
