import importlib.util
import io
import os
import re
import subprocess
import sys
import unittest
from contextlib import redirect_stdout


class CandidateRunner:
    """負責載入並執行受測解答程式。"""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.solution_path = self._find_solution_path()
        self.module = self._load_module(self.solution_path) if self.solution_path else None

    def _find_solution_path(self):
        preferred_names = [
            "question_10242.py",
            "solution_10242.py",
            "uva_10242.py",
            "main.py",
        ]

        for name in preferred_names:
            path = os.path.join(self.base_dir, name)
            if os.path.isfile(path):
                return path

        # 若找不到預設檔名，則挑同目錄第一個非測試 Python 檔。
        for name in sorted(os.listdir(self.base_dir)):
            if not name.endswith(".py"):
                continue
            if name.startswith("test_"):
                continue
            if name == os.path.basename(__file__):
                continue
            return os.path.join(self.base_dir, name)

        return None

    def _load_module(self, file_path):
        spec = importlib.util.spec_from_file_location("candidate_solution_10242", file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run(self, input_data: str) -> str:
        if self.solution_path is None:
            raise AssertionError(
                "找不到解答程式，請在同資料夾放入 question_10242.py（或其他 Python 解答檔）。"
            )

        # 優先使用 solve(input_str) 介面，沒有就改用子行程跑腳本。
        if self.module is not None and hasattr(self.module, "solve"):
            solve_fn = getattr(self.module, "solve")
            with io.StringIO() as buf, redirect_stdout(buf):
                returned = solve_fn(input_data)
                printed = buf.getvalue()

            if isinstance(returned, str):
                return returned
            return printed

        completed = subprocess.run(
            [sys.executable, self.solution_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"解答程式執行失敗（exit code={completed.returncode}）：\n{completed.stderr}"
            )
        return completed.stdout


def build_input(n, edges, atm_values, start, bars):
    """把測資轉成題目輸入格式。"""

    lines = [f"{n} {len(edges)}"]
    for u, v in edges:
        lines.append(f"{u} {v}")

    for value in atm_values:
        lines.append(str(value))

    lines.append(f"{start} {len(bars)}")
    lines.append(" ".join(map(str, bars)))
    return "\n".join(lines) + "\n"


def parse_single_integer(output: str) -> int:
    """解析輸出中的最終整數答案。"""

    tokens = re.findall(r"-?\d+", output)
    if not tokens:
        raise AssertionError(f"輸出中找不到整數答案：{output}")
    return int(tokens[-1])


def reference_solve(n, edges, atm_values, start, bars):
    """參考解：SCC 壓縮 + DAG DP。"""

    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u - 1].append(v - 1)

    sys.setrecursionlimit(1_000_000)

    index = 0
    stack = []
    on_stack = [False] * n
    indices = [-1] * n
    low = [0] * n
    comp_id = [-1] * n
    comp_count = 0

    def strongconnect(v):
        nonlocal index, comp_count
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for to in graph[v]:
            if indices[to] == -1:
                strongconnect(to)
                low[v] = min(low[v], low[to])
            elif on_stack[to]:
                low[v] = min(low[v], indices[to])

        if low[v] == indices[v]:
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp_id[w] = comp_count
                if w == v:
                    break
            comp_count += 1

    for v in range(n):
        if indices[v] == -1:
            strongconnect(v)

    comp_money = [0] * comp_count
    comp_is_bar = [False] * comp_count
    for v in range(n):
        c = comp_id[v]
        comp_money[c] += atm_values[v]

    for b in bars:
        comp_is_bar[comp_id[b - 1]] = True

    dag = [set() for _ in range(comp_count)]
    indeg = [0] * comp_count

    for u, v in edges:
        cu = comp_id[u - 1]
        cv = comp_id[v - 1]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    # 先從起點 SCC 做可達性，避免處理不相關節點。
    start_comp = comp_id[start - 1]
    reachable = [False] * comp_count
    stack2 = [start_comp]
    reachable[start_comp] = True
    while stack2:
        u = stack2.pop()
        for v in dag[u]:
            if not reachable[v]:
                reachable[v] = True
                stack2.append(v)

    # 拓樸排序（只取可達節點）。
    from collections import deque

    indeg2 = indeg[:]
    q = deque(i for i in range(comp_count) if indeg2[i] == 0)
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in dag[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q.append(v)

    NEG = -10**30
    dp = [NEG] * comp_count
    dp[start_comp] = comp_money[start_comp]

    for u in topo:
        if not reachable[u] or dp[u] == NEG:
            continue
        for v in dag[u]:
            if reachable[v]:
                cand = dp[u] + comp_money[v]
                if cand > dp[v]:
                    dp[v] = cand

    ans = 0
    found = False
    for c in range(comp_count):
        if reachable[c] and comp_is_bar[c] and dp[c] != NEG:
            found = True
            ans = max(ans, dp[c])

    return ans if found else 0


class TestQuestion10242(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = CandidateRunner()

    def assert_case(self, n, edges, atm_values, start, bars):
        input_data = build_input(n, edges, atm_values, start, bars)
        expected = reference_solve(n, edges, atm_values, start, bars)
        actual_text = self.runner.run(input_data)
        actual = parse_single_integer(actual_text)

        self.assertEqual(
            actual,
            expected,
            msg=(
                "答案不正確。\n"
                f"輸入:\n{input_data}\n"
                f"預期: {expected}\n"
                f"實際輸出: {actual_text}"
            ),
        )

    def test_simple_chain(self):
        # 1 -> 2 -> 3，終點酒吧在 3，應吃到全部 ATM。
        self.assert_case(
            n=3,
            edges=[(1, 2), (2, 3)],
            atm_values=[5, 7, 11],
            start=1,
            bars=[3],
        )

    def test_cycle_collect_once(self):
        # 1 <-> 2 形成 SCC，再走到 3。
        # 雖可重複經過路口，但每台 ATM 只能拿一次。
        self.assert_case(
            n=3,
            edges=[(1, 2), (2, 1), (2, 3)],
            atm_values=[10, 20, 5],
            start=1,
            bars=[3],
        )

    def test_choose_best_bar_path(self):
        # 有多條路、多個酒吧，要選總金額最大的可達酒吧。
        self.assert_case(
            n=4,
            edges=[(1, 2), (1, 3), (2, 4), (3, 4)],
            atm_values=[1, 100, 50, 1],
            start=1,
            bars=[2, 4],
        )

    def test_unreachable_bar(self):
        # 若酒吧不可達，期望答案為 0。
        self.assert_case(
            n=3,
            edges=[(1, 2)],
            atm_values=[5, 6, 100],
            start=1,
            bars=[3],
        )

    def test_multi_scc_path(self):
        # 測試多個 SCC 串接時，SCC 金額加總是否正確。
        self.assert_case(
            n=5,
            edges=[(1, 2), (2, 1), (2, 3), (3, 4), (4, 3), (4, 5)],
            atm_values=[3, 4, 5, 6, 7],
            start=1,
            bars=[5],
        )


if __name__ == "__main__":
    unittest.main()
