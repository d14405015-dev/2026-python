from __future__ import annotations

import sys


class FenwickTree:
    """Fenwick Tree（Binary Indexed Tree）。

    這個資料結構可以在 O(log n) 時間內完成兩件事：
    1. 單點加值
    2. 查詢前綴和

    這題會把「還沒被使用的編號」視為 1，
    已經拿走的編號視為 0，
    這樣就能利用前綴和快速知道某個範圍內還剩多少可用編號。
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        """把指定位置的值增加 delta。"""
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        """回傳 1 到 index 的總和。"""
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & -index
        return total

    def find_kth(self, kth: int) -> int:
        """找出第 kth 個仍然可用的編號。

        這裡的 kth 是從 1 開始計數。
        例如：
        - kth = 1 代表目前最小的可用編號
        - kth = 2 代表目前第二小的可用編號
        """
        index = 0
        bit_mask = 1

        while bit_mask < self.size:
            bit_mask <<= 1

        current_sum = 0
        while bit_mask > 0:
            next_index = index + bit_mask
            if next_index <= self.size and current_sum + self.tree[next_index] < kth:
                index = next_index
                current_sum += self.tree[next_index]
            bit_mask >>= 1

        return index + 1


def solve(data: str) -> str:
    """根據每個位置前面有多少較小編號，還原完整排列。"""
    stripped = data.strip()
    if not stripped:
        return ""

    numbers = list(map(int, stripped.split()))
    cow_count = numbers[0]

    # 第一個位置前面沒有任何牛，所以輸入只會提供後面 N - 1 個數字。
    smaller_before_counts = [0] * (cow_count + 1)
    for position in range(2, cow_count + 1):
        smaller_before_counts[position] = numbers[position - 1]

    # 一開始每個編號 1..N 都還沒被使用，因此全部標成 1。
    available_numbers = FenwickTree(cow_count)
    for label in range(1, cow_count + 1):
        available_numbers.add(label, 1)

    answer = [0] * (cow_count + 1)

    # 從後往前還原：
    # 對於第 position 個位置，smaller_before_counts[position] 代表
    # 在它前面有多少頭編號比它小的牛。
    # 換句話說，當我們從後往前填答案時，
    # 它就是「目前剩下可用編號中的第 smaller_before_counts[position] + 1 小」。
    for position in range(cow_count, 0, -1):
        kth_smallest = smaller_before_counts[position] + 1
        chosen_label = available_numbers.find_kth(kth_smallest)
        answer[position] = chosen_label
        available_numbers.add(chosen_label, -1)

    return "\n".join(map(str, answer[1:])) + "\n"


def main() -> None:
    input_data = sys.stdin.read()
    sys.stdout.write(solve(input_data))


if __name__ == "__main__":
    main()