# U02. 正則表達式進階技巧（2.4–2.6）
# 預編譯效能 / sub 回呼函數 / 大小寫一致替換
#
# 本檔案示範三個實務常用主題：
# 1. re.compile() 預編譯：重複使用同一模式時可減少解析成本。
# 2. re.sub() + 回呼函式：替換時可根據每次匹配內容做動態轉換。
# 3. 大小寫保留替換：在不區分大小寫搜尋下，輸出仍維持原文風格。

import re
import timeit
from calendar import month_abbr

# ── 預編譯效能（2.4）──────────────────────────────────
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
# 這個模式會抓到 月/日/年 三個群組
# group(1)=月, group(2)=日, group(3)=年
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")


def using_module():
    # 每次呼叫都讓 re 處理字串模式（可能包含重複解析成本）
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():
    # 使用已編譯好的 pattern 物件，重複操作時通常較有效率
    return datepat.findall(text)


# 簡單基準測試：比較 50,000 次呼叫的總耗時
# 注意：實際速度差受 Python 版本、輸入資料、模式複雜度影響
t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")


# ── sub 回呼函數（2.5）────────────────────────────────
def change_date(m: re.Match) -> str:
    # m 是每次匹配到的 Match 物件，可用 group(n) 讀取各群組
    # month_abbr[11] -> 'Nov'，month_abbr[3] -> 'Mar'
    mon_name = month_abbr[int(m.group(1))]
    # 把原本 M/D/Y 轉成 D Mon Y
    return f"{m.group(2)} {mon_name} {m.group(3)}"


# sub(函式, text) 會對每個匹配呼叫 change_date，回傳新字串
print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 保持大小寫一致的替換（2.6）───────────────────────
def matchcase(word: str):
    # 回傳一個 replace 函式，供 re.sub 當回呼使用
    # 這是 closure：內層函式可存取外層 word
    def replace(m: re.Match) -> str:
        t = m.group()
        # 若原文字是全大寫，替換詞也轉全大寫
        if t.isupper():
            return word.upper()
        # 若原文字是全小寫，替換詞也轉全小寫
        if t.islower():
            return word.lower()
        # 若原文字是首字大寫（Title case），替換詞也套用 capitalize
        if t[0].isupper():
            return word.capitalize()
        # 其他格式直接回傳原替換詞
        return word

    return replace


s = "UPPER PYTHON, lower python, Mixed Python"
# IGNORECASE：搜尋時不分大小寫
# matchcase('snake')：替換時依原匹配字詞的大小寫風格調整
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
