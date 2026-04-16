import subprocess
import sys
import unittest
from itertools import combinations
from pathlib import Path


class TestQuestion10093(unittest.TestCase):
    """測試 QUESTION-10093 解答程式是否能正確計算最多可部署的炮兵部隊數量。"""

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式預期都放在同一個學生作業資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下與 10093 題目對應的解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10093.py",
            "10093-easy.py",
            "10093-manual.py",
            "question_10093.py",
            "solution_10093.py",
            "uva_10093.py",
        ]

        selected_files = []
        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            if "10093" in path.name.lower() and path not in selected_files:
                selected_files.append(path)

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行學生解答程式，並回傳標準輸出內容（去除首尾空白）。"""
        completed = subprocess.run(
            [sys.executable, str(solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            cwd=self.base_dir,
            check=False,
        )
        if completed.returncode != 0:
            self.fail(
                f"解答程式 {solution_path.name} 執行失敗。\n"
                f"exit code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            )
        return completed.stdout.strip()

    def brute_force(self, grid):
        """用暴力列舉法計算正確答案，供小型測資驗證使用。

        步驟：
        1. 收集所有 P 格的座標。
        2. 列舉這些格子的所有子集合。
        3. 對每個子集合，檢查任意兩格之間是否互相攻擊。
        4. 回傳最大合法子集的大小。

        攻擊條件：
        - 同一行，欄位差 ≤ 2
        - 同一欄，列位差 ≤ 2
        """
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        # 收集所有可放置炮兵的位置（只有 P 格才能放）。
        plains = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == "P"
        ]

        def conflicts(pos_a, pos_b):
            ra, ca = pos_a
            rb, cb = pos_b
            # 同一行且欄位差 ≤ 2，代表互相攻擊。
            if ra == rb and abs(ca - cb) <= 2:
                return True
            # 同一欄且列位差 ≤ 2，代表互相攻擊。
            if ca == cb and abs(ra - rb) <= 2:
                return True
            return False

        best = 0
        for size in range(len(plains) + 1):
            for chosen in combinations(plains, size):
                valid = True
                for i in range(len(chosen)):
                    for j in range(i + 1, len(chosen)):
                        if conflicts(chosen[i], chosen[j]):
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    best = max(best, size)

        return best

    def assert_max_artillery(self, grid_lines):
        """把地圖轉成題目輸入格式，並驗證所有解答檔的輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到 QUESTION-10093 的解答程式。請先把對應 Python 檔放在同一個資料夾中。")

        grid = grid_lines
        rows = len(grid)
        cols = len(grid[0])
        input_data = f"{rows} {cols}\n" + "\n".join(grid) + "\n"
        expected = str(self.brute_force(grid))

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name, grid=grid):
                actual = self.run_solution(solution_path, input_data)
                self.assertEqual(actual, expected)

    def test_single_plain(self):
        # 1×1 的平原，只能放 1 支炮兵。
        self.assert_max_artillery(["P"])

    def test_single_mountain(self):
        # 1×1 的山地，無法放置任何炮兵。
        self.assert_max_artillery(["H"])

    def test_single_row_all_plain(self):
        # 1×5 全平原，橫向每隔兩格才能放一支，最多 2 支（例如位置 0 和 3）。
        self.assert_max_artillery(["PPPPP"])

    def test_single_col_all_plain(self):
        # 5×1 全平原，縱向每隔兩格才能放一支，最多 2 支。
        self.assert_max_artillery(["P", "P", "P", "P", "P"])

    def test_all_mountain(self):
        # 全山地，無論多大都放不了任何炮兵。
        self.assert_max_artillery(["HHH", "HHH", "HHH"])

    def test_mountains_as_blockers(self):
        # 山地作為天然屏障，可以讓更多炮兵安全部署。
        # 例如 1×3 的 "PHP"，兩端各放一支，山地擋住了攻擊範圍不存在的影響，
        # 但距離仍然是 2，所以互相攻擊，最多仍是 1。
        self.assert_max_artillery(["PHP"])

    def test_2x2_all_plain(self):
        # 2×2 全平原：(0,0) 攻擊 (0,1) 和 (1,0)，(1,1) 攻擊 (0,1) 和 (1,0)。
        # 對角 (0,0) 和 (1,1) 不互相攻擊，最多 2 支。
        self.assert_max_artillery(["PP", "PP"])

    def test_3x3_all_plain(self):
        # 3×3 全平原，用暴力法驗算正確答案。
        self.assert_max_artillery(["PPP", "PPP", "PPP"])

    def test_mixed_terrain(self):
        # 混合地形，山地分散在中間位置，驗證程式對地形的判斷是否正確。
        self.assert_max_artillery([
            "PHPH",
            "PPHP",
            "HPPP",
        ])


if __name__ == "__main__":
    unittest.main()
