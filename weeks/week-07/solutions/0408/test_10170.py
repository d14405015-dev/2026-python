import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10170(unittest.TestCase):
    """測試 QUESTION-10170 解答程式是否正確計算第 D 天住宿團體的人數。"""

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式預期都放在同一個學生作業資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下與 10170 題目對應的解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10170.py",
            "10170-easy.py",
            "10170-manual.py",
            "question_10170.py",
            "solution_10170.py",
            "uva_10170.py",
        ]

        selected_files = []

        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            lowered_name = path.name.lower()
            if "10170" in lowered_name and path not in selected_files:
                selected_files.append(path)

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行學生解答程式，回傳標準輸出內容（逐行）。"""
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

        return completed.stdout.splitlines()

    def expected_group_size(self, start_size, target_day):
        """用二分搜尋計算第 target_day 天的旅行團人數。

        若從 S 人團開始，當前考慮某個人數 n（n >= S）時，
        住到 n 人團結束為止的總天數是：
        S + (S+1) + ... + n

        這是一個等差級數，可寫為：
        n(n+1)/2 - (S-1)S/2

        我們要找的是最小的 n，使得上式 >= D。
        """
        left = start_size
        right = start_size

        def total_days_until(group_size):
            return (
                group_size * (group_size + 1) // 2
                - (start_size - 1) * start_size // 2
            )

        # 先把右界翻倍擴張到足夠大，確保二分搜尋有解區間。
        while total_days_until(right) < target_day:
            right *= 2

        while left < right:
            mid = (left + right) // 2
            if total_days_until(mid) >= target_day:
                right = mid
            else:
                left = mid + 1

        return left

    def assert_cases(self, cases):
        """把多筆 (S, D) 組成輸入，驗證所有解答檔輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到 QUESTION-10170 的解答程式。請先把對應 Python 檔放在同一個資料夾中。")

        input_data = "\n".join(f"{s} {d}" for s, d in cases) + "\n"
        expected_output_lines = [
            str(self.expected_group_size(s, d))
            for s, d in cases
        ]

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name, cases=cases):
                actual_output_lines = self.run_solution(solution_path, input_data)
                self.assertEqual(actual_output_lines, expected_output_lines)

    def test_single_case_start_day(self):
        # 第一天一定是起始旅行團入住。
        self.assert_cases([(4, 1)])

    def test_single_case_boundary_of_first_group(self):
        # 第 4 天仍是 4 人團（第一團最後一天）。
        self.assert_cases([(4, 4)])

    def test_single_case_next_group(self):
        # 第 5 天應該進入 5 人團。
        self.assert_cases([(4, 5)])

    def test_multiple_cases_in_one_input(self):
        # 驗證程式能處理直到 EOF 的多筆輸入。
        self.assert_cases([
            (1, 1),
            (1, 2),
            (4, 6),
            (10, 100),
        ])

    def test_large_day_value(self):
        # 大天數測資，確認沒有溢位與效能問題。
        self.assert_cases([(10000, 10**12)])

    def test_large_day_value_near_limit(self):
        # 接近題目上限的 D，確認答案仍正確。
        self.assert_cases([(9999, 10**15 - 1)])


if __name__ == "__main__":
    unittest.main()
