import math


def solve(input_data: str) -> str:
    tokens = input_data.split()
    if not tokens:
        return "0"

    a = int(tokens[0])
    n = a * a + 1

    root = math.isqrt(n)
    d = 1
    for x in range(root, 0, -1):
        if n % x == 0:
            d = x
            break

    e = n // d
    ans = 2 * a + d + e
    return str(ans)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
