"""Week 02 - Task 3: Log Summary

統計每位使用者事件數，並輸出全域最常見 action。
"""

from __future__ import annotations

from collections import Counter


def summarize_logs(records: list[tuple[str, str]]) -> tuple[list[tuple[str, int]], tuple[str, int]]:
    """回傳使用者總事件排序與最常見 action。"""
    # user_counter: 統計每位使用者出現次數（總事件數）
    user_counter = Counter(user for user, _ in records)
    # action_counter: 統計全域 action 出現次數
    action_counter = Counter(action for _, action in records)

    # 使用者輸出規則：次數由大到小；同次數時名稱由小到大
    user_summary = sorted(user_counter.items(), key=lambda x: (-x[1], x[0]))

    if action_counter:
        # top_action 規則：次數由大到小；同次數時 action 名稱由小到大
        top_action = sorted(action_counter.items(), key=lambda x: (-x[1], x[0]))[0]
    else:
        # 題目要求可處理空輸入，這裡提供穩定的預設輸出
        top_action = ("None", 0)

    return user_summary, top_action


def parse_input(lines: list[str]) -> list[tuple[str, str]]:
    """把輸入行轉成 (user, action) 記錄列表。"""
    # 完全沒有輸入時直接回傳空列表
    if not lines:
        return []

    # 第一行為紀錄筆數 m
    m = int(lines[0].strip())
    records: list[tuple[str, str]] = []

    # 後續 m 行每行格式：user action
    for line in lines[1 : m + 1]:
        user, action = line.strip().split()
        records.append((user, action))

    return records


def format_output(user_summary: list[tuple[str, int]], top_action: tuple[str, int]) -> str:
    """把統計結果轉成題目要求輸出格式。"""
    # 先輸出每位使用者的總事件數
    lines = [f"{user} {count}" for user, count in user_summary]
    # 最後輸出全域最常見 action
    lines.append(f"top_action: {top_action[0]} {top_action[1]}")
    return "\n".join(lines)


def main() -> None:
    """命令列進入點：讀 stdin、統計、輸出。"""
    import sys

    # 讀取所有輸入行，交由 parse_input 統一解析
    lines = [line.rstrip("\n") for line in sys.stdin.readlines()]
    records = parse_input(lines)
    user_summary, top_action = summarize_logs(records)
    # 由 format_output 統一控制輸出格式
    print(format_output(user_summary, top_action))


if __name__ == "__main__":
    main()
