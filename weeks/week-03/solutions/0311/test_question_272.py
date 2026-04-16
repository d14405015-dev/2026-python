"""UVA 272（Tex Quotes）單元測試。

用途：
- 自動掃描同資料夾中的 `question_272*.py` 解答程式。
- 以 subprocess 執行解答，餵入測資後比對輸出是否正確。

執行方式：
- 在目前資料夾執行：python -m unittest -v test_question_272.py
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


# 測試檔所在目錄（solutions/0311）
BASE_DIR = Path(__file__).resolve().parent


# UVA 272 經典範例：
# 普通雙引號 " 需要交替轉成 `` 與 ''。
SAMPLE_INPUT = '"To be or not to be," quoth the Bard, "that is the question"\n'
SAMPLE_EXPECTED_OUTPUT = "``To be or not to be,'' quoth the Bard, ``that is the question''\n"


# 額外測資：
# 1) 含多行與多組引號，驗證跨行仍持續交替。
# 2) 不含雙引號時，輸出必須完全不變。
EXTRA_CASES = [
    (
        "She said, \"hello\".\nThen he replied, \"ok\".\n",
        "She said, ``hello''.\nThen he replied, ``ok''.\n",
    ),
    (
        "No quote here.\nKeep everything unchanged.\n",
        "No quote here.\nKeep everything unchanged.\n",
    ),
]


def discover_solution_scripts() -> list[Path]:
    """找出需要測試的 UVA 272 解答程式。

    規則：
    - 只測目前資料夾下檔名符合 `question_272*.py` 的檔案。
    - 排除測試檔（test_*.py）。
    """
    scripts: list[Path] = []
    for path in sorted(BASE_DIR.glob("question_272*.py")):
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


class TestUVA272Solutions(unittest.TestCase):
    """驗證本資料夾所有 UVA 272 解答程式。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scripts = discover_solution_scripts()

    def test_found_solution_scripts(self) -> None:
        """確認至少有一個可測試的解答程式。"""
        self.assertTrue(
            self.scripts,
            "找不到 question_272*.py 解答檔，請先放入解答程式。",
        )

    def test_sample_case(self) -> None:
        """驗證題目經典範例。"""
        for script in self.scripts:
            with self.subTest(script=script.name):
                actual = run_script(script, SAMPLE_INPUT)
                self.assertEqual(actual, SAMPLE_EXPECTED_OUTPUT)

    def test_extra_cases(self) -> None:
        """驗證多行內容與無引號內容。"""
        for script in self.scripts:
            for case_input, case_expected in EXTRA_CASES:
                with self.subTest(script=script.name):
                    actual = run_script(script, case_input)
                    self.assertEqual(actual, case_expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
