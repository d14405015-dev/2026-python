import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10008(unittest.TestCase):
    """測試 QUESTION-10008 解答程式：密文字母頻率統計。

    解題核心：
    - 讀取 n 列文字，統計 A–Z（大小寫視為相同）各字母出現次數
    - 出現次數由大到小排序；次數相同時，按字母順序（A → Z）排序
    - 未出現的字母不輸出
    """

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式都預期放在同一個資料夾中
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """尋找同目錄下所有 10008 相關的解答檔（排除測試檔自身）。"""
        all_py = sorted(
            p for p in cls.base_dir.glob("*.py")
            if p.name != Path(__file__).name and not p.name.startswith("test_")
        )
        if not all_py:
            return []

        # 優先選取含 10008 關鍵字的檔名
        preferred = [p for p in all_py if "10008" in p.name]
        if preferred:
            return preferred

        return all_py

    def run_solution(self, solution_path, input_data):
        """執行指定解答程式，傳入標準輸入，回傳標準輸出字串。"""
        if not self.solution_paths:
            self.skipTest(
                "找不到解答程式。請先把 QUESTION-10008 的 Python 解答放在同一個資料夾中。"
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
                "找不到解答程式。請先把 QUESTION-10008 的 Python 解答放在同一個資料夾中。"
            )

        for sol in self.solution_paths:
            with self.subTest(solution=sol.name):
                actual = self.run_solution(sol, input_data)
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

    def test_case1_basic(self):
        """測試案例 1：基本範例，大小寫混合，一列文字。

        輸入：
          1
          Hello World

        字母統計（不分大小寫）：H=1, E=1, L=3, O=2, W=1, R=1, D=1
        排序規則：次數多者優先，次數相同時按字母序。
        預期輸出：
          L 3
          O 2
          D 1
          E 1
          H 1
          R 1
          W 1
        """
        input_data = "1\nHello World\n"
        expected = (
            "L 3\n"
            "O 2\n"
            "D 1\n"
            "E 1\n"
            "H 1\n"
            "R 1\n"
            "W 1"
        )
        self.assert_output(input_data, expected)

    def test_case2_single_letter(self):
        """測試案例 2：只有一個字母。

        輸入：
          1
          a

        預期輸出：A 1
        """
        input_data = "1\na\n"
        expected = "A 1"
        self.assert_output(input_data, expected)

    def test_case3_empty_lines(self):
        """測試案例 3：多列輸入含空行，空行不貢獻任何字母。

        輸入：
          3
          aaa
          (空行)
          bbb

        A 出現 3 次，B 出現 3 次，次數相同 → 按字母序，A 在 B 前。
        預期輸出：
          A 3
          B 3
        """
        input_data = "3\naaa\n\nbbb\n"
        expected = "A 3\nB 3"
        self.assert_output(input_data, expected)

    def test_case4_only_numbers_and_spaces(self):
        """測試案例 4：輸入只有數字與空白，沒有字母，無任何輸出。

        輸入：
          2
          12345
          67890

        預期輸出：（空）
        """
        input_data = "2\n12345\n67890\n"
        expected = ""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。")
        for sol in self.solution_paths:
            with self.subTest(solution=sol.name):
                actual = self.run_solution(sol, input_data).strip()
                self.assertEqual(
                    actual, "",
                    msg=f"{sol.name}：無字母時應無輸出，但實際輸出：{repr(actual)}"
                )

    def test_case5_all_same_count(self):
        """測試案例 5：所有出現字母次數相同，應按字母順序輸出。

        輸入：
          1
          abcde

        A=B=C=D=E=1，次數相同 → 按字母序 A, B, C, D, E。
        預期輸出：
          A 1
          B 1
          C 1
          D 1
          E 1
        """
        input_data = "1\nabcde\n"
        expected = "A 1\nB 1\nC 1\nD 1\nE 1"
        self.assert_output(input_data, expected)

    def test_case6_multiline_accumulate(self):
        """測試案例 6：跨多列累加字母次數。

        輸入：
          3
          aA
          Bb
          CC

        A 共 2 次（a+A），B 共 2 次（B+b），C 共 2 次（C+C）。
        次數相同 → 按字母序 A, B, C。
        預期輸出：
          A 2
          B 2
          C 2
        """
        input_data = "3\naA\nBb\nCC\n"
        expected = "A 2\nB 2\nC 2"
        self.assert_output(input_data, expected)

    def test_case7_longer_sentence(self):
        """測試案例 7：較長句子，驗證排序正確性。

        輸入：
          1
          The quick brown fox

        統計（不分大小寫）：
          T=1, H=1, E=1, Q=1, U=1, I=1, C=1, K=1,
          B=1, R=1, O=2, W=1, N=1, F=1, X=1
        次數 2：只有 O
        次數 1：B, C, E, F, H, I, K, N, Q, R, T, U, W, X → 按字母序
        預期輸出：
          O 2
          B 1
          C 1
          E 1
          F 1
          H 1
          I 1
          K 1
          N 1
          Q 1
          R 1
          T 1
          U 1
          W 1
          X 1
        """
        input_data = "1\nThe quick brown fox\n"
        expected = (
            "O 2\n"
            "B 1\n"
            "C 1\n"
            "E 1\n"
            "F 1\n"
            "H 1\n"
            "I 1\n"
            "K 1\n"
            "N 1\n"
            "Q 1\n"
            "R 1\n"
            "T 1\n"
            "U 1\n"
            "W 1\n"
            "X 1"
        )
        self.assert_output(input_data, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
