from __future__ import annotations

import sys
from typing import List, Sequence

INF = 10**9
CAP = 100


def compress_positions(L: int, stones: Sequence[int], cap: int = CAP) -> tuple[int, List[int]]:
    stones = sorted(stones)
    compressed: List[int] = []
    prev = 0
    cur = 0
    for p in stones:
        cur += min(p - prev, cap)
        compressed.append(cur)
        prev = p
    cur += min(L - prev, cap)
    return cur, compressed


def min_stones(L: int, S: int, T: int, stones: Sequence[int]) -> int:
    if L <= 0:
        return 0

    if S == T:
        step = S
        sset = set(stones)
        pos = step
        ans = 0
        while pos < L:
            if pos in sset:
                ans += 1
            pos += step
        return ans

    Lc, cstones = compress_positions(L, stones)
    sset = set(cstones)
    max_pos = Lc + T
    dp = [INF] * (max_pos + 1)
    dp[0] = 0

    for i in range(max_pos + 1):
        if dp[i] == INF or i >= Lc:
            continue
        for step in range(S, T + 1):
            nxt = i + step
            if nxt > max_pos:
                continue
            add = 1 if (nxt <= Lc and nxt in sset) else 0
            v = dp[i] + add
            if v < dp[nxt]:
                dp[nxt] = v

    return min(dp[Lc : Lc + T + 1])


def solve(input_text: str) -> str:
    nums = list(map(int, input_text.split()))
    if not nums:
        return ""
    L = nums[0]
    S, T, M = nums[1], nums[2], nums[3]
    stones = nums[4 : 4 + M]
    return str(min_stones(L, S, T, stones))


def main() -> None:
    data = sys.stdin.read()
    out = solve(data)
    if out:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
