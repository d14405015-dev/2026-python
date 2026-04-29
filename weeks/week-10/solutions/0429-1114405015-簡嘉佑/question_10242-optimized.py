"""
題目 10242 - Optimized 版本

優化重點：
1. 改用 Kosaraju 分解 SCC，並以 iterative DFS 避免深遞迴風險。
2. 建完 SCC 後，只在起點可到達的 SCC 子圖上做拓樸 DP。
3. 將圖、反圖、SCC、DAG 流程分段，方便維護與除錯。
"""

from __future__ import annotations

import sys
from collections import deque


def solve(data: str) -> str:
    values = list(map(int, data.split()))
    if not values:
        return ""

    index = 0
    node_count = values[index]
    index += 1
    edge_count = values[index]
    index += 1

    graph = [[] for _ in range(node_count + 1)]
    reverse_graph = [[] for _ in range(node_count + 1)]
    for _ in range(edge_count):
        start = values[index]
        index += 1
        end = values[index]
        index += 1
        graph[start].append(end)
        reverse_graph[end].append(start)

    atm_money = [0] * (node_count + 1)
    for node in range(1, node_count + 1):
        atm_money[node] = values[index]
        index += 1

    source = values[index]
    index += 1
    bar_count = values[index]
    index += 1
    bars = set(values[index:index + bar_count])

    visited = [False] * (node_count + 1)
    order = []

    def build_order(start_node: int) -> None:
        stack = [(start_node, 0)]
        visited[start_node] = True

        while stack:
            node, state = stack.pop()
            if state == 0:
                stack.append((node, 1))
                for nxt in graph[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append((nxt, 0))
            else:
                order.append(node)

    for node in range(1, node_count + 1):
        if not visited[node]:
            build_order(node)

    component_id = [-1] * (node_count + 1)
    component_money = []
    component_has_bar = []
    component_count = 0

    for start_node in reversed(order):
        if component_id[start_node] != -1:
            continue

        stack = [start_node]
        component_id[start_node] = component_count
        total_money = 0
        has_bar = False

        while stack:
            node = stack.pop()
            total_money += atm_money[node]
            if node in bars:
                has_bar = True

            for prev in reverse_graph[node]:
                if component_id[prev] == -1:
                    component_id[prev] = component_count
                    stack.append(prev)

        component_money.append(total_money)
        component_has_bar.append(has_bar)
        component_count += 1

    dag = [set() for _ in range(component_count)]
    for node in range(1, node_count + 1):
        comp_u = component_id[node]
        for nxt in graph[node]:
            comp_v = component_id[nxt]
            if comp_u != comp_v:
                dag[comp_u].add(comp_v)

    source_component = component_id[source]

    reachable = [False] * component_count
    stack = [source_component]
    reachable[source_component] = True
    while stack:
        comp = stack.pop()
        for nxt in dag[comp]:
            if not reachable[nxt]:
                reachable[nxt] = True
                stack.append(nxt)

    indegree = [0] * component_count
    for comp in range(component_count):
        if not reachable[comp]:
            continue
        for nxt in dag[comp]:
            if reachable[nxt]:
                indegree[nxt] += 1

    dp = [-1] * component_count
    dp[source_component] = component_money[source_component]

    queue = deque(
        comp for comp in range(component_count)
        if reachable[comp] and indegree[comp] == 0
    )

    while queue:
        comp = queue.popleft()
        for nxt in dag[comp]:
            if not reachable[nxt]:
                continue
            if dp[comp] != -1:
                dp[nxt] = max(dp[nxt], dp[comp] + component_money[nxt])
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    answer = 0
    for comp in range(component_count):
        if reachable[comp] and component_has_bar[comp] and dp[comp] > answer:
            answer = dp[comp]

    return str(answer)


def main() -> None:
    sys.setrecursionlimit(1_000_000)
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()