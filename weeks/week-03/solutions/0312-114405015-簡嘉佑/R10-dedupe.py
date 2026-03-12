# R10. 去重且保序（1.10）

def dedupe(items):
    # seen 用來記錄「已看過」的元素。
    # set 查找平均是 O(1)，所以整體效率不錯。
    seen = set()

    # 逐一掃過原始資料，保持原本出現順序。
    for item in items:
        # 只在第一次出現時輸出（yield）
        if item not in seen:
            # yield 代表這是生成器（generator）函式：
            # 每次產生一個值，不會一次建立完整結果清單。
            yield item
            # 標記這個值已出現，後續重複值就會被略過。
            seen.add(item)


def dedupe2(items, key=None):
    # 進階版：支援自訂 key（比較依據）
    # 例如 item 是 dict 時，dict 本身不能放進 set，
    # 但可以把某些欄位組成可 hash 的 key（如 tuple）來去重。
    seen = set()
    for item in items:
        # 若沒有傳 key，直接以 item 本身去重；
        # 若有傳 key，則改用 key(item) 的結果去重。
        val = item if key is None else key(item)
        if val not in seen:
            # 仍然回傳原始 item，保持資料完整性。
            yield item
            # 記錄的是比較值 val，不一定是 item 本身。
            seen.add(val)
