import sys


def solve(data):
    lines = data.strip().split("\n")
    n, m = map(int, lines[0].split())
    grid = [lines[i + 1].strip() for i in range(n)]

    terrain = []
    for row in grid:
        t = 0
        for j, ch in enumerate(row):
            if ch == "P":
                t |= (1 << j)
        terrain.append(t)

    def ok_row(mask):
        return not (mask & (mask >> 1)) and not (mask & (mask >> 2))

    base_masks = [v for v in range(1 << m) if ok_row(v)]

    valid = [
        [mask for mask in base_masks if (mask & terrain[r]) == mask]
        for r in range(n)
    ]

    dp = {(0, mask): bin(mask).count("1") for mask in valid[0]}

    for r in range(1, n):
        next_dp = {}
        for curr in valid[r]:
            soldiers = bin(curr).count("1")
            for (prev2, prev1), count in dp.items():
                if curr & prev1:
                    continue
                if curr & prev2:
                    continue
                key = (prev1, curr)
                new_count = count + soldiers
                if next_dp.get(key, -1) < new_count:
                    next_dp[key] = new_count
        dp = next_dp

    return str(max(dp.values())) + "\n" if dp else "0\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
