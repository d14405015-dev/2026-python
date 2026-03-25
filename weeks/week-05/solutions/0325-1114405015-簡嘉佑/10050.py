import sys


def lost_workdays(n: int, parties: list[int]) -> int:
    """計算 n 天內，因罷會損失的工作天數。

    參數:
    - n: 模擬總天數
    - parties: 各政黨的罷會週期 h
    """
    # 用 set 記錄罷會日，避免不同政黨同一天罷會被重複計算。
    lost = set()

    # 對每個政黨，從第 h 天開始，每隔 h 天罷會一次。
    for h in parties:
        day = h
        while day <= n:
            # 題目設定第 1 天是星期日，因此：
            # day % 7 == 6 -> 星期五
            # day % 7 == 0 -> 星期六
            # 這兩天是週末，不算工作天損失。
            if day % 7 not in (6, 0):
                lost.add(day)
            day += h

    return len(lost)


def solve(data: str) -> str:
    """解析輸入並輸出每組測資的答案。"""
    # 將所有輸入整數化，方便用索引依序讀取。
    nums = list(map(int, data.split()))
    if not nums:
        return ""

    # 第一個數字是測資組數 T。
    t = nums[0]
    # idx 指向目前讀到 nums 的哪個位置。
    idx = 1
    ans = []

    for _ in range(t):
        # 每組先讀取總天數 N。
        n = nums[idx]
        idx += 1

        # 再讀取政黨數量 P。
        p = nums[idx]
        idx += 1

        # 接著讀取 P 個 hartal 參數。
        parties = nums[idx : idx + p]
        idx += p

        ans.append(str(lost_workdays(n, parties)))

    # 每組答案各一行。
    return "\n".join(ans)


def main() -> None:
    # 以整包 stdin 讀入，符合 OJ 常見輸入形式。
    data = sys.stdin.read()
    out = solve(data)
    if out:
        print(out)


if __name__ == "__main__":
    main()
