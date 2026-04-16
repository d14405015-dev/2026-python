"""UVA 490（Rotating Sentences）單元測試。

用途：
- 自動掃描同資料夾中的 question_490*.py 解答程式。
- 以 subprocess 執行解答，餵入測資並比對輸出是否正確。

執行方式：
- 在目前資料夾執行：python -m unittest -v test_question_490.py
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


# 測試檔所在目錄（solutions/0311）
BASE_DIR = Path(__file__).resolve().parent


# 經典案例：HELLO / WORLD 旋轉 90 度順時針
SAMPLE_INPUT = """HELLO
WORLD
"""

SAMPLE_EXPECTED_OUTPUT = """WH
OE
RL
LL
DO
"""


# 額外案例：
# 1) 不等長字串，驗證補空白後的旋轉結果（重點看前導空白是否正確）。
# 2) 含空白與標點，驗證一般字元保持不變，只做旋轉。
EXTRA_CASES = [
    (
        """ABC
DE
F
""",
        """FDA
 EB
  C
""",
    ),
    (
        """A B!
xy
""",
        """xA
y 
 B
 !
""",
    ),
]


def discover_solution_scripts() -> list[Path]:
    """找出需要測試的 UVA 490 解答程式。

    規則：
    - 只測目前資料夾下檔名符合 question_490*.py 的檔案。
    - 排除測試檔（test_*.py）。
    """
    scripts: list[Path] = []
    for path in sorted(BASE_DIR.glob("question_490*.py")):
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


def normalize_newline(text: str) -> str:
    """統一換行符號，避免平台差異造成誤判。"""
    return text.replace("\r\n", "\n")


class TestUVA490Solutions(unittest.TestCase):
    """驗證本資料夾所有 UVA 490 解答程式。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scripts = discover_solution_scripts()

    def test_found_solution_scripts(self) -> None:
        """確認至少有一個可測試的解答程式。"""
        self.assertTrue(
            self.scripts,
            "找不到 question_490*.py 解答檔，請先放入解答程式。",
        )

    def test_sample_case(self) -> None:
        """驗證經典旋轉案例。"""
        expected = normalize_newline(SAMPLE_EXPECTED_OUTPUT)
        for script in self.scripts:
            with self.subTest(script=script.name):
                actual = normalize_newline(run_script(script, SAMPLE_INPUT))
                self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        """驗證不等長輸入與含空白標點的旋轉結果。"""
        for script in self.scripts:
            for case_input, case_expected in EXTRA_CASES:
                with self.subTest(script=script.name):
                    actual = normalize_newline(run_script(script, case_input))
                    expected = normalize_newline(case_expected)
                    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
