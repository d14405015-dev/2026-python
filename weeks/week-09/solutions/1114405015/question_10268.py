MORE_TEXT = "More than 63 trials needed."


def parse_cases(data: str):
    cases = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        k, n = map(int, line.split())
        if k == 0:
            break

        cases.append((k, n))

    return cases


def min_trials(k: int, n: int):
    if n <= 0:
        return "0"

    dp = [0] * (k + 1)

    for t in range(1, 64):
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1

        if dp[k] >= n:
            return str(t)

    return MORE_TEXT


def solve(data: str) -> str:
    cases = parse_cases(data)
    ans = [min_trials(k, n) for k, n in cases]
    return "\n".join(ans)


def main():
    import sys

    data = sys.stdin.read()
    out = solve(data)
    if out:
        print(out)


if __name__ == "__main__":
    main()
