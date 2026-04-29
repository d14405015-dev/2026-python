"""
UVA 10226（依題目檔描述）- Easy 版本

重點做法：
1. 把每個人「不想站的位置」存成集合。
2. 依位置由左到右放人，且每一步都從字母小到大嘗試，
   這樣自然就是字典序。
3. 每產生一個完整排列，就只輸出和上一個排列不同的尾端。

注意：
- 這份解法是依據課程檔 QUESTION-10226.md 的文字描述實作。
- 若實際評測輸出格式和題目站台有額外細節差異，請再依樣板微調。
"""

from __future__ import annotations

from typing import List, Set


def parse_cases(data: str) -> List[List[Set[int]]]:
    """解析多筆測資。

    輸入假設（依題目檔文字）：
    - 多筆測資直到 EOF。
    - 每筆先給一個 N。
    - 接著 N 行，第 i 行是第 i 個人不想站的位置清單，以 0 結尾。
    - 位置以 1 起算。
    """
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
            # 允許該行為空，代表沒有禁忌位置。
            row = lines[idx] if idx < len(lines) else "0"
            idx += 1

            nums = [int(x) for x in row.split()] if row else [0]
            bad_positions: Set[int] = set()
            for num in nums:
                if num == 0:
                    break
                # 轉成 0-based 位置索引
                bad_positions.add(num - 1)
            forbidden.append(bad_positions)

        cases.append(forbidden)

    return cases


def solve_case(forbidden: List[Set[int]]) -> List[str]:
    """解單筆測資，回傳要輸出的每一行字串。"""
    n = len(forbidden)
    letters = [chr(ord("A") + i) for i in range(n)]

    # placed[pos] = person_index
    placed = [-1] * n
    used = [False] * n

    raw_permutations: List[str] = []

    def dfs(pos: int) -> None:
        # 所有位置都填滿，收下一組完整排列。
        if pos == n:
            raw_permutations.append("".join(letters[placed[i]] for i in range(n)))
            return

        # 依字母順序嘗試人員，確保最終結果是字典序。
        for person in range(n):
            if used[person]:
                continue
            if pos in forbidden[person]:
                continue

            used[person] = True
            placed[pos] = person
            dfs(pos + 1)
            used[person] = False
            placed[pos] = -1

    dfs(0)

    # 題意要求：與上一個相同的前綴不輸出，只輸出不同尾端。
    output: List[str] = []
    prev = ""
    for cur in raw_permutations:
        if not prev:
            output.append(cur)
        else:
            first_diff = 0
            limit = min(len(prev), len(cur))
            while first_diff < limit and prev[first_diff] == cur[first_diff]:
                first_diff += 1
            output.append(cur[first_diff:])
        prev = cur

    return output


def solve(data: str) -> str:
    """整體解題流程：解析 -> 解各測資 -> 組合輸出。"""
    cases = parse_cases(data)

    all_lines: List[str] = []
    for case_index, forbidden in enumerate(cases):
        all_lines.extend(solve_case(forbidden))
        # 多筆測資間用空行分隔，閱讀比較清楚。
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
