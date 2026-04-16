import math
import sys


def find_group_size(start_size, target_day):
    required = 2 * target_day + (start_size - 1) * start_size

    n = (math.isqrt(1 + 4 * required) - 1) // 2

    while n * (n + 1) < required:
        n += 1

    while n > start_size and (n - 1) * n >= required:
        n -= 1

    if n < start_size:
        n = start_size

    return n


def solve(data):
    out = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        s, d = map(int, line.split())
        out.append(str(find_group_size(s, d)))

    return "\n".join(out) + ("\n" if out else "")


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
