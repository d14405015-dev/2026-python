"""
題目 10242 - Easy 版本

這題依照題目敘述，其核心是：
1. 圖上可能有環。
2. 同一個強連通分量（SCC）內的點都可以互相到達，
   所以只要進入這個分量，就能把裡面所有 ATM 金額都拿走一次。
3. 把每個 SCC 縮成一個點後，整張圖會變成 DAG，
   接著在 DAG 上做最大路徑 DP 即可。

這份 easy 版本刻意保留直白結構，方便手打與記憶。
"""

from __future__ import annotations

import sys


def solve(data: str) -> str:
    tokens = list(map(int, data.split()))
    if not tokens:
        return ""

    index = 0
    n = tokens[index]
    index += 1
    m = tokens[index]
    index += 1

    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = tokens[index]
        index += 1
        v = tokens[index]
        index += 1
        graph[u].append(v)

    money = [0] * (n + 1)
    for node in range(1, n + 1):
        money[node] = tokens[index]
        index += 1

    start = tokens[index]
    index += 1
    bar_count = tokens[index]
    index += 1
    bars = set(tokens[index:index + bar_count])

    # Tarjan 演算法所需資料。
    order = 0
    stack = []
    in_stack = [False] * (n + 1)
    visit_order = [0] * (n + 1)
    low_link = [0] * (n + 1)

    scc_id = [-1] * (n + 1)
    scc_money = []
    scc_has_bar = []
    scc_count = 0

    sys.setrecursionlimit(1_000_000)

    def tarjan(node: int) -> None:
        nonlocal order, scc_count

        order += 1
        visit_order[node] = order
        low_link[node] = order
        stack.append(node)
        in_stack[node] = True

        for nxt in graph[node]:
            if visit_order[nxt] == 0:
                tarjan(nxt)
                low_link[node] = min(low_link[node], low_link[nxt])
            elif in_stack[nxt]:
                low_link[node] = min(low_link[node], visit_order[nxt])

        # 若自己是 SCC 根，就把這個 SCC 整包取出來。
        if low_link[node] == visit_order[node]:
            total_money = 0
            has_bar = False

            while True:
                top = stack.pop()
                in_stack[top] = False
                scc_id[top] = scc_count
                total_money += money[top]
                if top in bars:
                    has_bar = True
                if top == node:
                    break

            scc_money.append(total_money)
            scc_has_bar.append(has_bar)
            scc_count += 1

    for node in range(1, n + 1):
        if visit_order[node] == 0:
            tarjan(node)

    # 建立 SCC 縮點後的 DAG。
    dag = [set() for _ in range(scc_count)]
    indegree = [0] * scc_count

    for node in range(1, n + 1):
        for nxt in graph[node]:
            a = scc_id[node]
            b = scc_id[nxt]
            if a != b and b not in dag[a]:
                dag[a].add(b)
                indegree[b] += 1

    start_scc = scc_id[start]

    # 先找出從起點可以走到哪些 SCC，避免處理無關節點。
    reachable = [False] * scc_count
    stack2 = [start_scc]
    reachable[start_scc] = True
    while stack2:
        now = stack2.pop()
        for nxt in dag[now]:
            if not reachable[nxt]:
                reachable[nxt] = True
                stack2.append(nxt)

    # 在 DAG 上做最大路徑 DP。
    # dp[x] = 從起點走到 SCC x 時，最多能拿到多少錢。
    dp = [-1] * scc_count
    dp[start_scc] = scc_money[start_scc]

    queue = []
    current_indegree = indegree[:]
    for scc in range(scc_count):
        if current_indegree[scc] == 0:
            queue.append(scc)

    head = 0
    while head < len(queue):
        now = queue[head]
        head += 1

        for nxt in dag[now]:
            if dp[now] != -1:
                candidate = dp[now] + scc_money[nxt]
                if candidate > dp[nxt]:
                    dp[nxt] = candidate

            current_indegree[nxt] -= 1
            if current_indegree[nxt] == 0:
                queue.append(nxt)

    answer = 0
    for scc in range(scc_count):
        if reachable[scc] and scc_has_bar[scc] and dp[scc] > answer:
            answer = dp[scc]

    return str(answer)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()