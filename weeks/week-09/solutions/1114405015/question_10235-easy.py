"""UVA 10235（課堂版本）- easy 記憶版

這份程式和正式版同樣正確，但刻意寫成比較好背的風格。
你可以記這個口訣：
1. 一格一格掃描
2. 每格看 top + left
3. 補出 right + down，讓度數 = 2

只要所有可用格（1）度數都等於 2，整體就會是若干個環，
剛好符合「每條蛇都咬住自己尾巴」。
"""

from functools import lru_cache

MOD = 1_000_000_007


def parse_cases(text):
    """解析輸入。"""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    t = int(lines[0])
    p = 1
    cases = []

    for _ in range(t):
        n, m = map(int, lines[p].split())
        p += 1
        grid = lines[p : p + n]
        p += n
        cases.append((n, m, grid))

    return cases


def row_mask_of_ones(row_str):
    """把像 '10110' 轉成 bitmask（1 的位置為可用格）。"""

    mask = 0
    for c, ch in enumerate(row_str):
        if ch == "1":
            mask |= 1 << c
    return mask


def solve_one(n, m, grid):
    """解單筆測資。"""

    open_masks = [row_mask_of_ones(row) for row in grid]

    @lru_cache(maxsize=None)
    def transit_row(up_mask, row_mask, next_row_mask):
        """在單一列做轉移：up_mask -> 多個 down_mask。"""

        # key = (down_mask, left)
        states = {(0, 0): 1}

        for c in range(m):
            new_states = {}
            top = (up_mask >> c) & 1
            is_open = (row_mask >> c) & 1

            # 右邊可連邊的條件：當前格與右格都必須是 1。
            right_ok = c + 1 < m and ((row_mask >> (c + 1)) & 1)

            # 下邊可連邊的條件：下一列同欄位是 1。
            down_ok = ((next_row_mask >> c) & 1) == 1

            for (down_mask, left), cnt in states.items():
                if not is_open:
                    # 0 格不可被佔用，因此 top 和 left 都必須是 0。
                    if top == 0 and left == 0:
                        key = (down_mask, 0)
                        new_states[key] = (new_states.get(key, 0) + cnt) % MOD
                    continue

                # 1 格必須剛好 degree=2。
                need = 2 - top - left
                if need < 0 or need > 2:
                    continue

                # 試 right/down 的所有 0/1 組合，保留 sum=need 的情況。
                for right in (0, 1):
                    if right == 1 and not right_ok:
                        continue

                    for down in (0, 1):
                        if down == 1 and not down_ok:
                            continue
                        if right + down != need:
                            continue

                        next_down_mask = down_mask | ((1 << c) if down else 0)
                        key = (next_down_mask, right)
                        new_states[key] = (new_states.get(key, 0) + cnt) % MOD

            states = new_states
            if not states:
                break

        # 一列結束時，left 必須回到 0（不能有邊跑出邊界）。
        res = {}
        for (down_mask, left), cnt in states.items():
            if left == 0:
                res[down_mask] = (res.get(down_mask, 0) + cnt) % MOD

        return tuple(sorted(res.items()))

    # dp[up_mask] = 目前處理到這一列之前的方案數
    dp = {0: 1}

    for r in range(n):
        row_mask = open_masks[r]
        next_row_mask = open_masks[r + 1] if r + 1 < n else 0
        new_dp = {}

        for up_mask, ways in dp.items():
            for down_mask, cnt in transit_row(up_mask, row_mask, next_row_mask):
                new_dp[down_mask] = (new_dp.get(down_mask, 0) + ways * cnt) % MOD

        dp = new_dp
        if not dp:
            break

    # 最後不能再有往下的邊。
    return dp.get(0, 0)


def solve(text):
    """整體求解，回傳 `Case i: ans`。"""

    cases = parse_cases(text)
    out_lines = []

    for i, (n, m, grid) in enumerate(cases, start=1):
        ans = solve_one(n, m, grid)
        out_lines.append(f"Case {i}: {ans}")

    return "\n".join(out_lines)


def main():
    import sys

    data = sys.stdin.read()
    print(solve(data))


if __name__ == "__main__":
    main()
