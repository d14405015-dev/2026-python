"""
UVA 948 天平找假幣 ─ 簡單好記版

【口訣記憶法】
  每枚硬幣只有兩種可能：「偏重假幣」或「偏輕假幣」。
  把每種可能拿去對照所有秤重結果，只要有一種說得通，該硬幣就是候選。
  最後只剩一枚候選 → 輸出；不止一枚或零枚 → 輸出 0。

【三條判斷規則（背起來）】
  1. 結果是 '='  → 假幣不能出現在任何一邊
  2. 結果是 '<'  → 假幣必須是「左邊偏輕」或「右邊偏重」
  3. 結果是 '>'  → 假幣必須是「左邊偏重」或「右邊偏輕」
"""

import sys


def check_ok(coin, heavy, weighings):
    """
    步驟 1：檢查「coin 是假幣（heavy=True偏重/False偏輕）」是否說得通。

    逐條秤重紀錄比對：
    - '=' 結果：假幣不能在秤重裡
    - '<' 結果：假幣必須在「左且輕」或「右且重」，否則解釋不了天平傾斜
    - '>' 結果：假幣必須在「左且重」或「右且輕」，否則解釋不了天平傾斜
    若所有紀錄都說得通，回傳 True。
    """
    for left, right, result in weighings:

        if result == '=':
            # 規則 1：等重 → 假幣不可現身
            if coin in left or coin in right:
                return False

        elif result == '<':
            # 規則 2：左邊輕 → 假幣必須「左+輕」或「右+重」
            if coin in left:
                if heavy:        # 偏重在左 → 左應更重，但天平說左輕 → 矛盾
                    return False
            elif coin in right:
                if not heavy:    # 偏輕在右 → 右應更輕，但天平說右重 → 矛盾
                    return False
            else:
                return False     # 假幣沒在秤，天平卻傾斜 → 矛盾

        else:  # '>'
            # 規則 3：左邊重 → 假幣必須「左+重」或「右+輕」
            if coin in left:
                if not heavy:    # 偏輕在左 → 左應更輕，但天平說左重 → 矛盾
                    return False
            elif coin in right:
                if heavy:        # 偏重在右 → 右應更重，但天平說右輕 → 矛盾
                    return False
            else:
                return False     # 假幣沒在秤，天平卻傾斜 → 矛盾

    return True


def find_fake(n, weighings):
    """
    步驟 2：對 1 到 N 每枚硬幣試「偏重」和「偏輕」，收集候選清單。
    候選唯一 → 回傳該硬幣編號，否則回傳 0。
    """
    candidates = []

    for coin in range(1, n + 1):
        # 偏重或偏輕，只要有一種說得通就是候選
        if check_ok(coin, True, weighings) or check_ok(coin, False, weighings):
            candidates.append(coin)

    return candidates[0] if len(candidates) == 1 else 0


def main():
    """
    步驟 3：讀取輸入並輸出結果。

    輸入格式：
      M（組數）
      （空白行）
      N K
      P c1..cP d1..dP   ← 第 i 次秤重的硬幣配置（左邊 P 枚，右邊 P 枚）
      結果符號（<, >, =）
      ...（共 K 組）
      （組間空白行）

    輸出格式：各組答案之間以空白行分隔。
    """
    lines = sys.stdin.read().split('\n')

    # 用迭代器跳過空白行，讓讀取更直覺
    nonempty = (line.strip() for line in lines if line.strip())
    it = iter(nonempty)

    M = int(next(it))  # 測試組數
    results = []

    for _ in range(M):
        n, k = map(int, next(it).split())  # N 枚硬幣，K 次秤重

        weighings = []
        for _ in range(k):
            nums = list(map(int, next(it).split()))
            p = nums[0]
            left  = set(nums[1:      p + 1])   # 左盤硬幣集合
            right = set(nums[p + 1: 2*p + 1])  # 右盤硬幣集合
            symbol = next(it)                  # '<', '>' 或 '='
            weighings.append((left, right, symbol))

        results.append(str(find_fake(n, weighings)))

    # 各組輸出以空白列分隔
    print('\n\n'.join(results))


if __name__ == '__main__':
    main()
