from collections import Counter
import sys


def count_pair_sums(numbers):
    """Count how many ordered pairs produce each sum.

    這一步是在準備 (a, b) 的所有可能結果。
    因為題目允許重複使用元素，
    所以每個位置都可以再次選同一個數字。
    """
    pair_sums = Counter()

    for left in numbers:
        for right in numbers:
            pair_sums[left + right] += 1

    return pair_sums


def count_triple_sums(numbers):
    """Count how many ordered triples produce each sum.

    這一步是在準備 (c, d, e) 的所有可能結果。
    把三層迴圈拆開寫，會比一次想六層迴圈容易記很多。
    """
    triple_sums = Counter()

    for first in numbers:
        for second in numbers:
            two_sum = first + second
            for third in numbers:
                triple_sums[two_sum + third] += 1

    return triple_sums


def solve_case(numbers):
    """Return the number of ordered 6-tuples.

    核心觀念：
    a + b + c + d + e = f

    把左邊五個數拆成兩段：
    1. a + b
    2. c + d + e

    如果知道：
    - 某個兩數和出現幾次
    - 某個三數和出現幾次

    那麼只要兩者相加等於某個 f，
    就能把組合數乘起來，累加到答案中。
    """
    pair_sums = count_pair_sums(numbers)
    triple_sums = count_triple_sums(numbers)

    answer = 0
    for target in numbers:
        for pair_sum, pair_count in pair_sums.items():
            needed_triple_sum = target - pair_sum
            triple_count = triple_sums.get(needed_triple_sum, 0)
            answer += pair_count * triple_count

    return answer


def solve(data):
    """Read input and format the final output string."""
    parts = data.split()
    if not parts:
        return ""

    size = int(parts[0])
    numbers = [int(value) for value in parts[1:1 + size]]
    answer = solve_case(numbers)
    return f"{answer}\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
