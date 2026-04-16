"""UVA 299（Train Swapping）單元測試。

用途：
- 自動掃描同資料夾中的 `question_299*.py` 解答程式。
- 以 subprocess 執行解答，餵入測資並比對輸出。

執行方式：
- 在目前資料夾執行：python -m unittest -v test_question_299.py
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


# 測試檔所在目錄（solutions/0311）
BASE_DIR = Path(__file__).resolve().parent


# 標準型測資：
# 1) 1 3 2 -> 只需交換一次
# 2) 4 3 2 1 -> 完全反序，4 個元素需要 6 次相鄰交換
# 3) 2 1 -> 1 次交換
SAMPLE_INPUT = """3
3
1 3 2
4
4 3 2 1
2
2 1
"""

SAMPLE_EXPECTED_OUTPUT = """Optimal train swapping takes 1 swaps.
Optimal train swapping takes 6 swaps.
Optimal train swapping takes 1 swaps.
"""


# 額外案例：
# 1) 已排序，不需要交換。
# 2) 單一車廂，不需要交換。
# 3) 長度為 0（依題目範圍可出現），也不需要交換。
EXTRA_CASES = [
    (
        """3
5
1 2 3 4 5
1
1
0

""",
        """Optimal train swapping takes 0 swaps.
Optimal train swapping takes 0 swaps.
Optimal train swapping takes 0 swaps.
""",
    ),
    (
        """1
5
5 1 2 4 3
""",
        """Optimal train swapping takes 5 swaps.
""",
    ),
]


def discover_solution_scripts() -> list[Path]:
    """找出需要測試的 UVA 299 解答程式。

    規則：
    - 只測目前資料夾下檔名符合 `question_299*.py` 的檔案。
    - 排除測試檔（test_*.py）。
    """
    scripts: list[Path] = []
    for path in sorted(BASE_DIR.glob("question_299*.py")):
        if path.name.startswith("test_"):
            continue
        scripts.append(path)
    return scripts


def run_script(script_path: Path, input_data: str) -> str:
    """執行解答程式並回傳標準輸出。"""
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        input=input_data,
        text=True,
        capture_output=True,
        cwd=str(BASE_DIR),
        check=False,
    )

    if completed.returncode != 0:
        raise AssertionError(
            f"程式執行失敗：{script_path.name}\n"
            f"return code: {completed.returncode}\n"
            f"stderr:\n{completed.stderr}"
        )

    return completed.stdout


def normalize_output(text: str) -> str:
    """正規化輸出，避免平台換行與尾端空白差異造成誤判。"""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


class TestUVA299Solutions(unittest.TestCase):
    """驗證本資料夾所有 UVA 299 解答程式。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scripts = discover_solution_scripts()

    def test_found_solution_scripts(self) -> None:
        """確認至少有一個可測試的解答程式。"""
        self.assertTrue(
            self.scripts,
            "找不到 question_299*.py 解答檔，請先放入解答程式。",
        )

    def test_sample_case(self) -> None:
        """驗證標準型測資。"""
        expected = normalize_output(SAMPLE_EXPECTED_OUTPUT)
        for script in self.scripts:
            with self.subTest(script=script.name):
                actual = normalize_output(run_script(script, SAMPLE_INPUT))
                self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        """驗證已排序、單元素、L=0 與一般隨機序列。"""
        for script in self.scripts:
            for case_input, case_expected in EXTRA_CASES:
                with self.subTest(script=script.name):
                    actual = normalize_output(run_script(script, case_input))
                    expected = normalize_output(case_expected)
                    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
