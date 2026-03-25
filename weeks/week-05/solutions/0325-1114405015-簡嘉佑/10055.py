import sys


class Fenwick:
    """Fenwick Tree（Binary Indexed Tree）。

    用途：快速計算「前綴和」與「單點更新」。
    時間複雜度：更新 O(log N)、查詢 O(log N)。
    這裡用來統計區間 [l, r] 內「減函數」的個數。
    """

    def __init__(self, n: int) -> None:
        # bit 陣列大小為 n+1，索引從 1 開始。
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        # 單點更新：將位置 i 加上 delta，並透過低位元往上更新。
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def sum(self, i: int) -> int:
        # 前綴和查詢：回傳 [1, i] 的總和。
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        # 區間和查詢：利用前綴差計算 [l, r] 的總和。
        return self.sum(r) - self.sum(l - 1)


def solve(data: str) -> str:
    # 把所有數字一次讀入後以索引依序存取，避免逐行處理的麻煩。
    nums = list(map(int, data.split()))
    if not nums:
        return ""

    idx = 0
    n = nums[idx]  # 函數總數 N
    idx += 1
    q = nums[idx]  # 操作總數 Q
    idx += 1

    # state[i] = 0(增) / 1(減)，記錄每個函數目前的狀態，初始全為增函數。
    state = [0] * (n + 1)
    # 以 Fenwick Tree 維護「減函數」的個數，支援快速區間查詢。
    fw = Fenwick(n)
    out = []

    for _ in range(q):
        v = nums[idx]
        idx += 1

        if v == 1:
            # 操作 v=1：反轉第 i 個函數的增減性。
            i = nums[idx]
            idx += 1

            if state[i] == 0:
                # 原本是增函數，反轉為減函數，Fenwick Tree 加 1。
                state[i] = 1
                fw.add(i, 1)
            else:
                # 原本是減函數，反轉為增函數，Fenwick Tree 減 1。
                state[i] = 0
                fw.add(i, -1)
        else:
            # 操作 v=2：查詢複合函數 f_L∘f_(L+1)∘…∘f_R 的增減性。
            l = nums[idx]
            idx += 1
            r = nums[idx]
            idx += 1

            # 區間內減函數個數為奇數 -> 複合結果為減函數(1)，偶數 -> 增函數(0)。
            out.append(str(fw.range_sum(l, r) % 2))

    # 每個查詢結果各佔一行。
    return "\n".join(out)


def main() -> None:
    # 整包讀入 stdin，適用 OJ 環境。
    data = sys.stdin.read()
    ans = solve(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
