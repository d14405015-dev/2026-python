"""Week 02 - Task 1: Sequence Clean

讀取一行以空白分隔的整數，輸出：
1. dedupe: 去重後（保留第一次出現順序）
2. asc: 由小到大排序
3. desc: 由大到小排序
4. evens: 偶數序列（維持原始順序）
"""

from __future__ import annotations


def sequence_clean(numbers: list[int]) -> dict[str, list[int]]:
    """依題目規格整理序列，並回傳四種結果。"""
    # seen 用來記錄「已經出現過」的數字，避免重複加入 dedupe。
    seen: set[int] = set()
    # dedupe 需要保留原始出現順序，因此使用 list 逐一追加。
    dedupe: list[int] = []

    # 只在第一次看到元素時加入 dedupe，確保順序與原始輸入一致
    for num in numbers:
        if num not in seen:
            seen.add(num)
            dedupe.append(num)

    # asc / desc 直接使用內建排序，程式簡潔且可讀性高。
    asc = sorted(numbers)
    desc = sorted(numbers, reverse=True)

    # evens 透過列表生成式保留原順序，只挑選可被 2 整除的元素。
    evens = [num for num in numbers if num % 2 == 0]

    return {
        "dedupe": dedupe,
        "asc": asc,
        "desc": desc,
        "evens": evens,
    }


def parse_numbers(line: str) -> list[int]:
    """把輸入字串轉成整數列表；空字串會得到空列表。"""
    # 先移除前後空白，避免只輸入空白字元時造成解析問題。
    stripped = line.strip()
    if not stripped:
        return []
    # 以空白切開後逐一轉為 int。
    return [int(token) for token in stripped.split()]


def format_output(result: dict[str, list[int]]) -> str:
    """依作業格式組合輸出文字。"""
    # 依題目要求固定輸出四行，順序不可改變。
    lines = []
    for key in ("dedupe", "asc", "desc", "evens"):
        # 將整數列表轉成空白分隔字串，符合評測比對格式。
        values = " ".join(str(x) for x in result[key])
        lines.append(f"{key}: {values}".rstrip())
    return "\n".join(lines)


def main() -> None:
    """命令列進入點：讀取一行輸入後輸出結果。"""
    import sys

    # 題目規格為一行輸入，因此只讀取第一行。
    line = sys.stdin.readline()
    numbers = parse_numbers(line)
    result = sequence_clean(numbers)
    # 統一由 format_output 控制輸出格式，避免不同位置重複字串拼接。
    print(format_output(result))


if __name__ == "__main__":
    main()
