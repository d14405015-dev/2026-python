import math


def solve(input_data: str) -> str:
    """
    UVA 10193

    由
        arctan(1/a) = arctan(1/b) + arctan(1/c)
    與反正切加法公式可推得：
        bc - a(b + c) = 1

    將式子改寫：
        (b - a)(c - a) = a^2 + 1

    設
        d = b - a, e = c - a
    則
        d * e = a^2 + 1，且 b + c = 2a + d + e

    因此只要在 a^2+1 的所有因數配對 (d, e) 中，找最小的 d+e 即可。
    由於 d、e 互為因數，最小 d+e 會出現在最接近 sqrt(a^2+1) 的配對。
    """
    tokens = input_data.split()
    if not tokens:
        return "0"

    a = int(tokens[0])
    n = a * a + 1

    root = math.isqrt(n)

    # 從 sqrt(n) 往下找第一個可整除的因數，可直接得到最小 d+e
    d = 1
    for x in range(root, 0, -1):
        if n % x == 0:
            d = x
            break

    e = n // d
    answer = 2 * a + d + e
    return str(answer)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
