import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion948(unittest.TestCase):
    """測試 QUESTION-948 解答程式：天平找假幣。

    解題策略：
    - 對每枚硬幣，嘗試它是「輕假幣」或「重假幣」
    - 驗證所有秤重結果是否與該假設相容
    - 若唯一相容的硬幣只有一枚，輸出該硬幣編號；否則輸出 0
    """

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式都預期放在同一個資料夾中
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """尋找同目錄下所有 948 相關的解答檔（排除測試檔自身）。"""
        all_py = sorted(
            p for p in cls.base_dir.glob("*.py")
            if p.name != Path(__file__).name and not p.name.startswith("test_")
        )
        if not all_py:
            return []

        # 優先選取含 948 關鍵字的檔名
        preferred = [p for p in all_py if "948" in p.name]
        if preferred:
            return preferred

        # 退而求其次，回傳所有非測試的 .py
        return all_py

    def run_solution(self, solution_path, input_data):
        """執行指定解答程式，傳入標準輸入，回傳標準輸出字串。"""
        if not self.solution_paths:
            self.skipTest(
                "找不到解答程式。請先把 QUESTION-948 的 Python 解答放在同一個資料夾中。"
            )

        result = subprocess.run(
            [sys.executable, str(solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            cwd=self.base_dir,
            check=False,
        )

        if result.returncode != 0:
            self.fail(
                f"解答程式 {solution_path.name} 執行失敗。\n"
                f"exit code: {result.returncode}\n"
                f"stderr:\n{result.stderr}"
            )

        return result.stdout

    def assert_output(self, input_data, expected_output):
        """對所有找到的解答檔，逐行比對輸出是否符合預期。"""
        if not self.solution_paths:
            self.skipTest(
                "找不到解答程式。請先把 QUESTION-948 的 Python 解答放在同一個資料夾中。"
            )

        for sol in self.solution_paths:
            with self.subTest(solution=sol.name):
                actual = self.run_solution(sol, input_data)
                # 逐行比對（忽略行尾空白）
                actual_lines = [ln.rstrip() for ln in actual.strip().splitlines()]
                expected_lines = [ln.rstrip() for ln in expected_output.strip().splitlines()]
                self.assertEqual(
                    actual_lines,
                    expected_lines,
                    msg=(
                        f"\n解答程式：{sol.name}"
                        f"\n輸入：\n{input_data}"
                        f"\n期望輸出：\n{expected_output.strip()}"
                        f"\n實際輸出：\n{actual.strip()}"
                    ),
                )

    # -----------------------------------------------------------------------
    # 測試案例
    # -----------------------------------------------------------------------

    def test_case1_find_heavy_coin(self):
        """測試案例 1：3 枚硬幣，兩次秤重後可確認硬幣 2 是假的（偏重）。

        秤重 1：硬幣 1 vs 硬幣 2，左邊輕 (<)
        秤重 2：硬幣 1 vs 硬幣 3，兩邊一樣 (=)
        => 秤重 2 的 = 表示硬幣 1 和 3 都是真的，所以假幣是硬幣 2。
        """
        input_data = (
            "1\n"
            "\n"
            "3 2\n"
            "1 1 2\n"
            "<\n"
            "1 1 3\n"
            "=\n"
        )
        expected = "2"
        self.assert_output(input_data, expected)

    def test_case2_ambiguous_one_weighing(self):
        """測試案例 2：4 枚硬幣，只秤一次，無法判斷是哪枚假幣，輸出 0。

        秤重：硬幣 1,2 vs 硬幣 3,4，左邊輕 (<)
        => 硬幣 1 或 2 偏輕，或硬幣 3 或 4 偏重，共 4 種可能，無法唯一確定。
        """
        input_data = (
            "1\n"
            "\n"
            "4 1\n"
            "2 1 2 3 4\n"
            "<\n"
        )
        expected = "0"
        self.assert_output(input_data, expected)

    def test_case3_coin_not_weighed(self):
        """測試案例 3：3 枚硬幣，只有硬幣 1 和 2 被放上天平且兩邊一樣，因此假幣是硬幣 3。

        秤重：硬幣 1 vs 硬幣 2，兩邊一樣 (=)
        => 硬幣 1、2 均為真，假幣必定是硬幣 3。
        """
        input_data = (
            "1\n"
            "\n"
            "3 1\n"
            "1 1 2\n"
            "=\n"
        )
        expected = "3"
        self.assert_output(input_data, expected)

    def test_case4_find_heavy_coin_excluded(self):
        """測試案例 4：5 枚硬幣，由秤重結果確認假幣是硬幣 5（偏重）。

        秤重 1：硬幣 1,2 vs 硬幣 3,4，兩邊一樣 (=)
        秤重 2：硬幣 1 vs 硬幣 5，左邊輕 (<)
        => 秤重 1 的 = 確認 1,2,3,4 均為真；
           秤重 2 中硬幣 1 為真，左邊輕表示右邊（硬幣 5）偏重。
        """
        input_data = (
            "1\n"
            "\n"
            "5 2\n"
            "2 1 2 3 4\n"
            "=\n"
            "1 1 5\n"
            "<\n"
        )
        expected = "5"
        self.assert_output(input_data, expected)

    def test_case5_three_weighings_narrow_down(self):
        """測試案例 5：6 枚硬幣，三次秤重縮小範圍，最終確認假幣是硬幣 3（偏重）。

        秤重 1：硬幣 1,2,3 vs 硬幣 4,5,6，左邊重 (>)  => 假幣可能在其中
        秤重 2：硬幣 1,4 vs 硬幣 2,5，兩邊一樣 (=)    => 1,4,2,5 均為真
        秤重 3：硬幣 3 vs 硬幣 1，左邊重 (>)           => 硬幣 3 偏重
        """
        input_data = (
            "1\n"
            "\n"
            "6 3\n"
            "3 1 2 3 4 5 6\n"
            ">\n"
            "2 1 4 2 5\n"
            "=\n"
            "1 3 1\n"
            ">\n"
        )
        expected = "3"
        self.assert_output(input_data, expected)

    def test_case6_multiple_test_cases(self):
        """測試案例 6：多組測試資料（M=3），每組輸出之間有空白列。

        組 1：硬幣 2 是假的（偏重）
        組 2：無法判斷，輸出 0
        組 3：硬幣 3 是假的（原因同 test_case3）
        """
        input_data = (
            "3\n"
            "\n"
            "3 2\n"
            "1 1 2\n"
            "<\n"
            "1 1 3\n"
            "=\n"
            "\n"
            "4 1\n"
            "2 1 2 3 4\n"
            "<\n"
            "\n"
            "3 1\n"
            "1 1 2\n"
            "=\n"
        )
        # 每組結果之間輸出空白列
        expected = "2\n\n0\n\n3"
        self.assert_output(input_data, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
