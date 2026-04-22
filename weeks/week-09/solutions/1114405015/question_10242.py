from collections import deque


def parse_input(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return None

    idx = 0
    n, m = map(int, lines[idx].split())
    idx += 1

    edges = []
    for _ in range(m):
        u, v = map(int, lines[idx].split())
        idx += 1
        edges.append((u - 1, v - 1))

    atm = []
    for _ in range(n):
        atm.append(int(lines[idx]))
        idx += 1

    s, p = map(int, lines[idx].split())
    idx += 1
    bars = list(map(int, lines[idx].split()))

    return n, edges, atm, s - 1, [b - 1 for b in bars]


def solve_case(n, edges, atm, start, bars):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    import sys

    sys.setrecursionlimit(1_000_000)
    index = 0
    stack = []
    on_stack = [False] * n
    dfn = [-1] * n
    low = [0] * n
    comp_id = [-1] * n
    comp_cnt = 0

    def tarjan(u):
        nonlocal index, comp_cnt
        dfn[u] = index
        low[u] = index
        index += 1
        stack.append(u)
        on_stack[u] = True

        for v in graph[u]:
            if dfn[v] == -1:
                tarjan(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], dfn[v])

        if low[u] == dfn[u]:
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp_id[w] = comp_cnt
                if w == u:
                    break
            comp_cnt += 1

    for i in range(n):
        if dfn[i] == -1:
            tarjan(i)

    comp_money = [0] * comp_cnt
    for i in range(n):
        comp_money[comp_id[i]] += atm[i]

    comp_bar = [False] * comp_cnt
    for b in bars:
        comp_bar[comp_id[b]] = True

    dag = [set() for _ in range(comp_cnt)]
    indeg = [0] * comp_cnt
    for u, v in edges:
        cu = comp_id[u]
        cv = comp_id[v]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    start_comp = comp_id[start]

    reachable = [False] * comp_cnt
    st = [start_comp]
    reachable[start_comp] = True
    while st:
        u = st.pop()
        for v in dag[u]:
            if not reachable[v]:
                reachable[v] = True
                st.append(v)

    q = deque([i for i in range(comp_cnt) if indeg[i] == 0])
    topo = []
    indeg2 = indeg[:]
    while q:
        u = q.popleft()
        topo.append(u)
        for v in dag[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q.append(v)

    NEG = -10**30
    dp = [NEG] * comp_cnt
    dp[start_comp] = comp_money[start_comp]

    for u in topo:
        if not reachable[u] or dp[u] == NEG:
            continue
        for v in dag[u]:
            if reachable[v]:
                candidate = dp[u] + comp_money[v]
                if candidate > dp[v]:
                    dp[v] = candidate

    ans = 0
    found = False
    for c in range(comp_cnt):
        if reachable[c] and comp_bar[c] and dp[c] != NEG:
            found = True
            ans = max(ans, dp[c])

    return ans if found else 0


def solve(data):
    parsed = parse_input(data)
    if parsed is None:
        return ""
    n, edges, atm, start, bars = parsed
    return str(solve_case(n, edges, atm, start, bars))


def main():
    import sys

    data = sys.stdin.read()
    out = solve(data)
    if out:
        print(out)


if __name__ == "__main__":
    main()
