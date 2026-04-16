from collections import Counter
import sys


def count_pair_sums(numbers):
    pair_sums = Counter()
    for a in numbers:
        for b in numbers:
            pair_sums[a + b] += 1
    return pair_sums


def count_triple_sums(numbers):
    triple_sums = Counter()
    for a in numbers:
        for b in numbers:
            for c in numbers:
                triple_sums[a + b + c] += 1
    return triple_sums


def solve(data):
    parts = data.split()
    if not parts:
        return ""

    n = int(parts[0])
    numbers = [int(x) for x in parts[1:1 + n]]

    pair_sums = count_pair_sums(numbers)
    triple_sums = count_triple_sums(numbers)

    answer = 0
    for f in numbers:
        for pair_sum, pair_count in pair_sums.items():
            triple_count = triple_sums.get(f - pair_sum, 0)
            answer += pair_count * triple_count

    return f"{answer}\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
