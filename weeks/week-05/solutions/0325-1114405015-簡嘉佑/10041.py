import sys


def min_total_distance(addresses: list[int]) -> int:
    """計算此組地址的最小總距離。

    核心觀念：在一維線段上，讓絕對距離總和最小的位置是中位數。
    """
    sorted_addresses = sorted(addresses)
    # 取排序後的中位數位置作為最佳住址。
    median = sorted_addresses[len(sorted_addresses) // 2]
    # 將每位親戚到最佳住址的距離加總。
    return sum(abs(x - median) for x in sorted_addresses)


def solve(data: str) -> str:
    """解析 UVA 10041 輸入格式並輸出每組答案。"""
    nums = list(map(int, data.split()))
    if not nums:
        return ""

    # 第一個數字是測試資料組數。
    t = nums[0]
    idx = 1
    outputs = []

    for _ in range(t):
        # 每組第一個數字 r 代表親戚人數，後面接著 r 個門牌。
        r = nums[idx]
        idx += 1
        addresses = nums[idx : idx + r]
        idx += r
        outputs.append(str(min_total_distance(addresses)))

    # 題目要求每組結果各佔一行。
    return "\n".join(outputs)


def main() -> None:
    # 以整包標準輸入讀入，方便在 OJ 平台直接提交。
    input_data = sys.stdin.read()
    result = solve(input_data)
    if result:
        print(result)


if __name__ == "__main__":
    main()
