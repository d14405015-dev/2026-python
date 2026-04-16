"""
UVA 948 / ZeroJudge c095：天平找假幣

解題核心思路
────────────
每枚硬幣只有兩種「假幣假設」：偏重（heavy）或偏輕（light）。

對每枚硬幣 coin（1 到 N），嘗試「coin 是偏重假幣」與「coin 是偏輕假幣」：

  秤重結果 '<'（左邊輕）→ 假幣必須是「在左邊且偏輕」或「在右邊且偏重」
  秤重結果 '>'（左邊重）→ 假幣必須是「在左邊且偏重」或「在右邊且偏輕」
  秤重結果 '='（兩邊等）→ 假幣不可能出現在這次秤重的任何一邊

若某枚硬幣「至少有一種假幣假設」與所有秤重結果均相容，則列為候選。
候選只有 1 枚 → 輸出該編號；否則輸出 0。
"""

import sys


def is_consistent(coin: int, heavy: bool, weighings: list) -> bool:
    """
    判斷「硬幣 coin 是假幣（heavy=True 表偏重，heavy=False 表偏輕）」
    是否與所有秤重紀錄相容。

    參數
    ----
    coin     : 候選假幣編號（1-indexed）
    heavy    : True → 假設假幣偏重；False → 假設假幣偏輕
    weighings: 秤重記錄清單，每筆為 (left_set, right_set, result_str)
    """
    for left, right, result in weighings:

        if result == '=':
            # '=' 代表兩邊均是真幣，假幣不可在任何一邊
            if coin in left or coin in right:
                return False  # 假幣竟然出現在等重的秤重中，矛盾

        elif result == '<':
            # 左邊輕，右邊重
            # 能解釋此結果的只有：假幣在左邊且偏輕，或假幣在右邊且偏重
            if coin in left:
                if heavy:
                    # 偏重假幣在左邊 → 左邊應該更重，但結果是左邊輕 → 矛盾
                    return False
            elif coin in right:
                if not heavy:
                    # 偏輕假幣在右邊 → 右邊應該更輕，但結果是右邊重 → 矛盾
                    return False
            else:
                # 假幣完全不在這次秤重中，卻出現了不平衡的結果 → 矛盾
                return False

        else:  # result == '>'
            # 左邊重，右邊輕
            # 能解釋此結果的只有：假幣在左邊且偏重，或假幣在右邊且偏輕
            if coin in left:
                if not heavy:
                    # 偏輕假幣在左邊 → 左邊應該更輕，但結果是左邊重 → 矛盾
                    return False
            elif coin in right:
                if heavy:
                    # 偏重假幣在右邊 → 右邊應該更重，但結果是右邊輕 → 矛盾
                    return False
            else:
                # 假幣不在這次秤重中，卻出現了不平衡的結果 → 矛盾
                return False

    return True  # 所有秤重均相容


def find_fake_coin(n: int, weighings: list) -> int:
    """
    在 n 枚硬幣中，根據秤重紀錄找出假幣。

    回傳假幣編號；無法確定時回傳 0。
    """
    candidates = []  # 所有「可能是假幣」的硬幣列表

    for coin in range(1, n + 1):
        # 只要偏重或偏輕其中一種假設成立，該硬幣就是候選假幣
        if is_consistent(coin, True, weighings) or is_consistent(coin, False, weighings):
            candidates.append(coin)

    # 候選恰好只有一枚，可唯一確定假幣
    if len(candidates) == 1:
        return candidates[0]
    return 0  # 無法確定（0 枚或多枚候選）


def read_next_nonempty(lines: list, idx: list) -> str:
    """
    從 lines 中跳過空白行，回傳下一行非空字串（並推進索引 idx[0]）。
    使用 list 包裝 idx 以模擬 pass-by-reference。
    """
    while idx[0] < len(lines) and lines[idx[0]].strip() == '':
        idx[0] += 1
    if idx[0] < len(lines):
        line = lines[idx[0]].strip()
        idx[0] += 1
        return line
    return ''


def main():
    lines = sys.stdin.read().split('\n')
    idx = [0]  # 用 list 包裝，讓 read_next_nonempty 可修改

    M = int(read_next_nonempty(lines, idx))  # 測試組數
    outputs = []

    for _ in range(M):
        # 讀取硬幣數 N 與秤重次數 K
        n, k = map(int, read_next_nonempty(lines, idx).split())

        weighings = []
        for _ in range(k):
            # 每次秤重由兩行組成：
            # 行1: P c1...cP d1...dP（P 為每邊硬幣數，前 P 個為左邊，後 P 個為右邊）
            # 行2: 秤重結果（<、>、=）
            nums = list(map(int, read_next_nonempty(lines, idx).split()))
            p = nums[0]  # 每邊硬幣數量
            left = set(nums[1: p + 1])        # 左盤硬幣編號集合
            right = set(nums[p + 1: 2 * p + 1])  # 右盤硬幣編號集合
            result = read_next_nonempty(lines, idx)  # '<', '>' 或 '='
            weighings.append((left, right, result))

        outputs.append(str(find_fake_coin(n, weighings)))

    # 各組輸出之間用空白列分隔
    print('\n\n'.join(outputs))


if __name__ == '__main__':
    main()
