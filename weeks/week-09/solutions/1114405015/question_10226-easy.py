"""UVA/ZeroJudge 10226（本課題版本）- easy 記憶版

這一版刻意用「容易背」的寫法：
1. 先決定第幾個位置（position）
2. 再挑一個還沒用過的人（person）
3. 合法就放下去，遞迴到下一格

核心口訣：
- 位置往下走
- 人只能用一次
- 違反限制就跳過
"""

from typing import List


def read_cases(text: str):
    """把輸入文字解析成多筆測資。"""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    i = 0
    cases = []

    while i < len(lines):
        n = int(lines[i])
        i += 1

        forbidden = []
        for _ in range(n):
            arr = list(map(int, lines[i].split()))
            i += 1

            bad_positions = set()
            for x in arr:
                if x == 0:
                    break
                bad_positions.add(x)

            forbidden.append(bad_positions)

        cases.append((n, forbidden))

    return cases


def solve_one(n: int, forbidden: List[set]) -> List[str]:
    """回傳單筆測資的輸出行。"""

    # A, B, C, ...
    people = [chr(ord("A") + k) for k in range(n)]

    # used[p] = True 代表第 p 個人已經被放進某個位置。
    used = [False] * n

    # path[pos] = 該位置目前放了誰。
    path = [""] * n

    # answer_lines 存最後要輸出的每一行。
    answer_lines: List[str] = []

    # prev_perm 記錄上一個合法排列，為了實作「只印不同尾段」。
    prev_perm: List[str] | None = None

    def output_by_rule(curr_perm: List[str]):
        """套用題目輸出規則。"""

        nonlocal prev_perm

        # 第一個合法排列要完整輸出。
        if prev_perm is None:
            answer_lines.append("".join(curr_perm))
            prev_perm = curr_perm[:]
            return

        # 找到第一個和上一筆不同的位置。
        j = 0
        while j < n and prev_perm[j] == curr_perm[j]:
            j += 1

        # 只印從差異點開始的尾段。
        answer_lines.append("".join(curr_perm[j:]))
        prev_perm = curr_perm[:]

    def backtrack(position: int):
        """在指定位置嘗試放人（字典序）。"""

        # 全部位置都填完，得到一個合法排列。
        if position == n:
            output_by_rule(path)
            return

        # 題目限制的位置編號是 1-based。
        pos1 = position + 1

        # 按 A -> B -> C... 嘗試，天然保證字典序。
        for p in range(n):
            if used[p]:
                continue

            # 這個人不想站在 pos1，就不能放。
            if pos1 in forbidden[p]:
                continue

            used[p] = True
            path[position] = people[p]
            backtrack(position + 1)
            used[p] = False

    backtrack(0)
    return answer_lines


def solve(text: str) -> str:
    """整體求解：支援多筆測資。"""

    chunks = []
    for n, forbidden in read_cases(text):
        lines = solve_one(n, forbidden)
        chunks.append("\n".join(lines))

    return "\n".join(chunks).rstrip()


def main():
    import sys

    data = sys.stdin.read()
    out = solve(data)
    if out:
        print(out)


if __name__ == "__main__":
    main()
