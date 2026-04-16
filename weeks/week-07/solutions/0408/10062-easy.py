from __future__ import annotations

import sys


class FenwickTree:
    """用來維護目前哪些編號還可以被選到。

    tree[i] 不是單一位置的值，
    而是某一段區間的累積資訊。
    透過 Fenwick Tree 可以把「找第 k 小可用編號」控制在 O(log n)。
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def find_kth_available_number(self, kth: int) -> int:
        """回傳目前第 kth 小的可用編號。"""
        answer_index = 0
        prefix_sum_so_far = 0
        bit_value = 1

        while bit_value < self.size:
            bit_value <<= 1

        while bit_value > 0:
            candidate_index = answer_index + bit_value
            if candidate_index <= self.size:
                candidate_sum = prefix_sum_so_far + self.tree[candidate_index]
                if candidate_sum < kth:
                    answer_index = candidate_index
                    prefix_sum_so_far = candidate_sum
            bit_value >>= 1

        return answer_index + 1


def restore_order(cow_count: int, smaller_before_counts: list[int]) -> list[int]:
    """把題目提供的資訊還原成完整排列。

    思考方式：
    1. 從最後一個位置往前想。
    2. 如果某個位置前面有 x 頭比牠小，
       表示它在當前剩餘編號裡面是第 x + 1 小。
    3. 找到這個編號後，把它從可用集合中刪掉，再繼續往前填。
    """
    available = FenwickTree(cow_count)
    for label in range(1, cow_count + 1):
        available.add(label, 1)

    answer = [0] * cow_count

    for position in range(cow_count - 1, -1, -1):
        how_many_smaller_before = smaller_before_counts[position]
        kth_smallest_number = how_many_smaller_before + 1
        chosen_label = available.find_kth_available_number(kth_smallest_number)
        answer[position] = chosen_label
        available.add(chosen_label, -1)

    return answer


def solve(data: str) -> str:
    stripped = data.strip()
    if not stripped:
        return ""

    values = list(map(int, stripped.split()))
    cow_count = values[0]

    # 第 1 個位置沒有輸入資料，所以手動補成 0。
    smaller_before_counts = [0]
    smaller_before_counts.extend(values[1:])

    answer = restore_order(cow_count, smaller_before_counts)
    return "\n".join(map(str, answer)) + "\n"


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()