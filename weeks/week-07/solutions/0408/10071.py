from collections import Counter
import sys


def build_pair_sum_counts(numbers):
    """統計所有有序兩元組 (a, b) 的和出現幾次。

    題目允許重複使用集合中的元素，
    所以 a 與 b 都可以自由從 numbers 中挑選。
    另外這裡把順序視為不同情況，
    也就是說 (a, b) 與 (b, a) 都要分別計算。
    """
    pair_sum_counts = Counter()

    for first_number in numbers:
        for second_number in numbers:
            pair_sum_counts[first_number + second_number] += 1

    return pair_sum_counts


def build_triple_sum_counts(numbers):
    """統計所有有序三元組 (c, d, e) 的和出現幾次。"""
    triple_sum_counts = Counter()

    for first_number in numbers:
        for second_number in numbers:
            partial_sum = first_number + second_number
            for third_number in numbers:
                triple_sum_counts[partial_sum + third_number] += 1

    return triple_sum_counts


def count_six_tuples(numbers):
    """計算滿足 a + b + c + d + e = f 的有序六元組數量。

    直接枚舉六個位置需要 O(N^6)，會太慢。
    這裡把左邊五個數拆成：

    - (a, b)
    - (c, d, e)

    先分別統計所有兩數和與三數和，
    最後再檢查哪些 pair_sum + triple_sum 可以等於某個 f。
    """
    pair_sum_counts = build_pair_sum_counts(numbers)
    triple_sum_counts = build_triple_sum_counts(numbers)

    total_count = 0
    for target_value in numbers:
        for pair_sum, pair_count in pair_sum_counts.items():
            needed_triple_sum = target_value - pair_sum
            triple_count = triple_sum_counts.get(needed_triple_sum, 0)
            total_count += pair_count * triple_count

    return total_count


def solve(data):
    """讀取輸入並回傳答案字串。"""
    values = data.split()
    if not values:
        return ""

    count = int(values[0])
    numbers = [int(value) for value in values[1:1 + count]]
    answer = count_six_tuples(numbers)
    return f"{answer}\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()