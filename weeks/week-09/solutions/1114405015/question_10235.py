from functools import lru_cache

MOD = 1_000_000_007


def _build_open_masks(grid):
    n = len(grid)
    masks = []
    for r in range(n):
        mask = 0
        for c in range(len(grid[r])):
            if grid[r][c] == "1":
                mask |= 1 << c
        masks.append(mask)
    return masks


def _parse_input(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return []

    t = int(lines[0])
    idx = 1
    cases = []

    for _ in range(t):
        n, m = map(int, lines[idx].split())
        idx += 1
        grid = lines[idx : idx + n]
        idx += n
        cases.append((n, m, grid))

    return cases


def solve_case(n, m, grid):
    open_masks = _build_open_masks(grid)

    @lru_cache(maxsize=None)
    def transition_for_row(up_mask, row_mask, next_row_mask):
        states = {(0, 0): 1}

        for c in range(m):
            new_states = {}
            top = (up_mask >> c) & 1

            is_open = (row_mask >> c) & 1
            right_allowed = c + 1 < m and ((row_mask >> (c + 1)) & 1)
            down_allowed = ((next_row_mask >> c) & 1) == 1

            for (down_mask, left), cnt in states.items():
                if not is_open:
                    if top == 0 and left == 0:
                        key = (down_mask, 0)
                        new_states[key] = (new_states.get(key, 0) + cnt) % MOD
                    continue

                need = 2 - top - left
                if need < 0 or need > 2:
                    continue

                for right in (0, 1):
                    if right == 1 and not right_allowed:
                        continue

                    for down in (0, 1):
                        if down == 1 and not down_allowed:
                            continue
                        if right + down != need:
                            continue

                        new_down_mask = down_mask | ((1 << c) if down else 0)
                        key = (new_down_mask, right)
                        new_states[key] = (new_states.get(key, 0) + cnt) % MOD

            states = new_states
            if not states:
                break

        result = {}
        for (down_mask, left), cnt in states.items():
            if left == 0:
                result[down_mask] = (result.get(down_mask, 0) + cnt) % MOD

        return tuple(sorted(result.items()))

    dp = {0: 1}

    for r in range(n):
        row_mask = open_masks[r]
        next_row_mask = open_masks[r + 1] if r + 1 < n else 0
        new_dp = {}

        for up_mask, ways in dp.items():
            transitions = transition_for_row(up_mask, row_mask, next_row_mask)
            for down_mask, cnt in transitions:
                new_dp[down_mask] = (new_dp.get(down_mask, 0) + ways * cnt) % MOD

        dp = new_dp
        if not dp:
            break

    return dp.get(0, 0)


def solve(data):
    cases = _parse_input(data)
    out = []

    for i, (n, m, grid) in enumerate(cases, start=1):
        ans = solve_case(n, m, grid)
        out.append(f"Case {i}: {ans}")

    return "\n".join(out)


def main():
    import sys

    data = sys.stdin.read()
    print(solve(data))


if __name__ == "__main__":
    main()
