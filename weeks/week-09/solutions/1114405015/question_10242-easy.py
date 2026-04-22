"""UVA 10242 - easy 記憶版

這版用更容易記憶的流程：
1. 把強連通分量（SCC）縮成點
2. 每個 SCC 的 ATM 先加總
3. 在 SCC-DAG 上做最長路 DP（從起點 SCC 出發）

口訣：
- 先縮點
- 再走 DAG
- 酒吧取最大
"""

from collections import deque


def read_case(text):
    """解析單筆測資。"""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None

    p = 0
    n, m = map(int, lines[p].split())
    p += 1

    edges = []
    for _ in range(m):
        a, b = map(int, lines[p].split())
        p += 1
        edges.append((a - 1, b - 1))

    money = []
    for _ in range(n):
        money.append(int(lines[p]))
        p += 1

    s, k = map(int, lines[p].split())
    p += 1
    bars = list(map(int, lines[p].split()))

    return n, edges, money, s - 1, [x - 1 for x in bars]


def solve_one(n, edges, money, start, bars):
    """回傳最大可搶金額。"""

    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)

    # -------- Tarjan SCC --------
    import sys

    sys.setrecursionlimit(1_000_000)
    time = 0
    dfn = [-1] * n
    low = [0] * n
    stack = []
    in_stack = [False] * n
    comp = [-1] * n
    comp_cnt = 0

    def dfs(u):
        nonlocal time, comp_cnt
        dfn[u] = time
        low[u] = time
        time += 1
        stack.append(u)
        in_stack[u] = True

        for v in g[u]:
            if dfn[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif in_stack[v]:
                low[u] = min(low[u], dfn[v])

        if low[u] == dfn[u]:
            while True:
                x = stack.pop()
                in_stack[x] = False
                comp[x] = comp_cnt
                if x == u:
                    break
            comp_cnt += 1

    for i in range(n):
        if dfn[i] == -1:
            dfs(i)

    # -------- SCC 金額/酒吧標記 --------
    comp_money = [0] * comp_cnt
    for i in range(n):
        comp_money[comp[i]] += money[i]

    comp_bar = [False] * comp_cnt
    for b in bars:
        comp_bar[comp[b]] = True

    # -------- 建 DAG --------
    dag = [set() for _ in range(comp_cnt)]
    indeg = [0] * comp_cnt
    for u, v in edges:
        cu = comp[u]
        cv = comp[v]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    start_comp = comp[start]

    # 先做可達性
    reach = [False] * comp_cnt
    stack2 = [start_comp]
    reach[start_comp] = True
    while stack2:
        u = stack2.pop()
        for v in dag[u]:
            if not reach[v]:
                reach[v] = True
                stack2.append(v)

    # 拓樸排序
    indeg2 = indeg[:]
    q = deque([i for i in range(comp_cnt) if indeg2[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in dag[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q.append(v)

    # DAG 最長路 DP
    NEG = -10**30
    dp = [NEG] * comp_cnt
    dp[start_comp] = comp_money[start_comp]

    for u in topo:
        if not reach[u] or dp[u] == NEG:
            continue
        for v in dag[u]:
            if reach[v]:
                dp[v] = max(dp[v], dp[u] + comp_money[v])

    ans = 0
    ok = False
    for c in range(comp_cnt):
        if reach[c] and comp_bar[c] and dp[c] != NEG:
            ok = True
            ans = max(ans, dp[c])

    return ans if ok else 0


def solve(text):
    """對外介面。"""

    parsed = read_case(text)
    if parsed is None:
        return ""

    n, edges, money, start, bars = parsed
    return str(solve_one(n, edges, money, start, bars))


def main():
    import sys

    data = sys.stdin.read()
    out = solve(data)
    if out:
        print(out)


if __name__ == "__main__":
    main()
