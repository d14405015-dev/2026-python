"""
題目 10226 - Optimized 版本

優化重點：
1. 不再先收集所有完整排列，再二次處理輸出。
2. 直接在 DFS 產生排列時，立即和前一筆結果比較並輸出差異尾端。
3. 使用 bitmask 表示哪些人已經被使用，減少 list/set 操作成本。
4. 先為每個位置預算可放哪些人，DFS 時少做重複判斷。

注意：
- 這份程式仍依照目前 QUESTION-10226.md 的文字敘述實作。
"""

from __future__ import annotations

from typing import List, Set


def parse_cases(data: str) -> List[List[Set[int]]]:
    lines = [line.strip() for line in data.splitlines()]
    idx = 0
    cases: List[List[Set[int]]] = []

    while idx < len(lines):
        if not lines[idx]:
            idx += 1
            continue

        n = int(lines[idx])
        idx += 1

        forbidden: List[Set[int]] = []
        for _ in range(n):
            row = lines[idx] if idx < len(lines) else "0"
            idx += 1

            bad_positions: Set[int] = set()
            for num in map(int, row.split() or ["0"]):
                if num == 0:
                    break
                bad_positions.add(num - 1)
            forbidden.append(bad_positions)

        cases.append(forbidden)

    return cases


def solve_case(forbidden: List[Set[int]]) -> List[str]:
    n = len(forbidden)
    letters = [chr(ord("A") + i) for i in range(n)]

    # allowed_people[pos] = 這個位置可以放哪些人。
    allowed_people = [
        [person for person in range(n) if pos not in forbidden[person]]
        for pos in range(n)
    ]

    current = [""] * n
    output: List[str] = []
    previous = ""

    def dfs(pos: int, used_mask: int) -> None:
        nonlocal previous

        if pos == n:
            arrangement = "".join(current)
            if not previous:
                output.append(arrangement)
            else:
                diff_index = 0
                while diff_index < n and arrangement[diff_index] == previous[diff_index]:
                    diff_index += 1
                output.append(arrangement[diff_index:])
            previous = arrangement
            return

        for person in allowed_people[pos]:
            bit = 1 << person
            if used_mask & bit:
                continue
            current[pos] = letters[person]
            dfs(pos + 1, used_mask | bit)

    dfs(0, 0)
    return output


def solve(data: str) -> str:
    cases = parse_cases(data)
    all_lines: List[str] = []

    for case_index, forbidden in enumerate(cases):
        all_lines.extend(solve_case(forbidden))
        if case_index != len(cases) - 1:
            all_lines.append("")

    return "\n".join(all_lines)


def main() -> None:
    import sys

    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()