import importlib.util
import pathlib
import subprocess
import sys
import unittest


class TestUVA10189Minesweeper(unittest.TestCase):
    """UVA 10189（踩地雷）單元測試。"""

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答檔放在同一個資料夾，預設解答檔名為 solution_10189.py
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10189.py"

    def run_solver(self, input_data: str) -> str:
        """
        嘗試兩種方式執行受測程式：
        1. 匯入 solution_10189.py 並呼叫 solve(input_data)（推薦）。
        2. 若沒有 solve，退回以子行程執行腳本，從標準輸入餵資料。
        """
        if not self.solution_path.exists():
            self.fail(
                f"找不到受測檔案: {self.solution_path.name}。"
                "請在同一資料夾建立 solution_10189.py。"
            )

        spec = importlib.util.spec_from_file_location("solution_10189", self.solution_path)
        if spec is None or spec.loader is None:
            self.fail("無法載入 solution_10189.py。")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 優先使用函式介面，方便精準做 unit test
        if hasattr(module, "solve") and callable(module.solve):
            result = module.solve(input_data)
            self.assertIsInstance(result, str, "solve(input_data) 必須回傳字串。")
            return result

        # 若沒有 solve 函式，改為以命令列方式執行整支程式
        completed = subprocess.run(
            [sys.executable, str(self.solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            self.fail(
                "受測程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            )
        return completed.stdout

    @staticmethod
    def normalize_output(output: str) -> str:
        # 正規化輸出：去除每行尾端空白，並統一結尾換行
        lines = [line.rstrip() for line in output.strip().splitlines()]
        return "\n".join(lines)

    def assert_output_equal(self, actual: str, expected: str):
        self.assertEqual(self.normalize_output(actual), self.normalize_output(expected))

    def test_official_sample(self):
        """題目範例測資。"""
        input_data = """\
4 4
*...
....
.*..
....
3 5
**...
.....
.*...
0 0
"""
        expected = """\
Field #1:
*100
2210
1*10
1110

Field #2:
**100
33200
1*100
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_single_mine(self):
        """最小有雷案例：1x1 且唯一格子是地雷。"""
        input_data = """\
1 1
*
0 0
"""
        expected = """\
Field #1:
*
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_single_empty(self):
        """最小無雷案例：1x1 且唯一格子是空白，答案應為 0。"""
        input_data = """\
1 1
.
0 0
"""
        expected = """\
Field #1:
0
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_all_mines(self):
        """全是地雷時，輸出應與輸入雷區一致。"""
        input_data = """\
2 3
***
***
0 0
"""
        expected = """\
Field #1:
***
***
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_no_mines(self):
        """沒有地雷時，所有格子都應為 0。"""
        input_data = """\
2 4
....
....
0 0
"""
        expected = """\
Field #1:
0000
0000
"""
        self.assert_output_equal(self.run_solver(input_data), expected)

    def test_multiple_fields_blank_line(self):
        """多組資料時，Field 之間要有一個空行。"""
        input_data = """\
1 2
*.
2 2
..
.*
0 0
"""
        expected = """\
Field #1:
*1

Field #2:
11
1*
"""
        self.assert_output_equal(self.run_solver(input_data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
