"""Week 02 - Task 2: Student Ranking

輸入多筆學生資料（name score age），依規則排序後輸出前 k 名：
1. score 由高到低
2. 同分時 age 由小到大
3. 再同時 name 字母序由小到大
"""

from __future__ import annotations


def rank_students(students: list[tuple[str, int, int]], k: int) -> list[tuple[str, int, int]]:
    """依題目規則排序並回傳前 k 名。"""
    # key 設計：
    # 1) score 要由高到低，因此使用 -score
    # 2) age 要由小到大，直接放 age
    # 3) name 要字母序由小到大，直接放 name
    ranked = sorted(students, key=lambda row: (-row[1], row[2], row[0]))
    # 只回傳前 k 名（若 k 大於總人數，切片會自動回傳全部）
    return ranked[:k]


def parse_input(lines: list[str]) -> tuple[list[tuple[str, int, int]], int]:
    """把輸入行轉成學生資料與 k。"""
    # 防禦性處理：若完全沒有輸入，回傳空資料。
    if not lines:
        return [], 0

    # 第一行格式：n k
    n, k = map(int, lines[0].strip().split())
    students: list[tuple[str, int, int]] = []

    # 接下來讀取 n 行，每行格式：name score age
    for line in lines[1 : n + 1]:
        name, score, age = line.strip().split()
        students.append((name, int(score), int(age)))

    return students, k


def format_output(students: list[tuple[str, int, int]]) -> str:
    """把排序結果轉為題目要求的多行字串。"""
    # 每位學生輸出一行：name score age
    return "\n".join(f"{name} {score} {age}" for name, score, age in students)


def main() -> None:
    """命令列進入點：讀 stdin、排序、輸出。"""
    import sys

    # readlines() 讀入全部輸入行，再交由 parse_input 統一解析。
    lines = [line.rstrip("\n") for line in sys.stdin.readlines()]
    students, k = parse_input(lines)
    # 格式化後一次印出，確保輸出格式穩定。
    print(format_output(rank_students(students, k)))


if __name__ == "__main__":
    main()
