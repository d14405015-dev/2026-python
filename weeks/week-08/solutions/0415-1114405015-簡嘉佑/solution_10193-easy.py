import math


# -easy 版本：
# 口訣只有三步
# 1) 算 n = a^2 + 1
# 2) 找 n 的因數配對 (d, e)
# 3) 答案是 2a + d + e 的最小值


def solve(input_data: str) -> str:
    tokens = input_data.split()
    if not tokens:
        return "0"

    a = int(tokens[0])
    n = a * a + 1

    best = 10**30

    # 只要掃到 sqrt(n) 就夠了，另一半因數可由 n//d 得到
    limit = math.isqrt(n)
    for d in range(1, limit + 1):
        if n % d != 0:
            continue

        e = n // d

        # b = a + d, c = a + e
        # 所以 b + c = 2a + d + e
        total = 2 * a + d + e
        if total < best:
            best = total

    return str(best)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
