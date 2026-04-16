"""UVA 100（3n + 1）單元測試。

用途：
- 自動掃描同資料夾中的解答程式（*.py）。
- 以 subprocess 執行每個解答，餵入測資後比對輸出是否正確。

執行方式：
- 在目前資料夾執行：python -m unittest -v test_question_100.py
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


# 測試檔所在目錄（也就是 solutions/0311）
BASE_DIR = Path(__file__).resolve().parent


# 標準範例測資（來自題目敘述）
SAMPLE_INPUT = """1 10
100 200
201 210
900 1000
"""

SAMPLE_EXPECTED_OUTPUT = """1 10 20
100 200 125
201 210 89
900 1000 174
"""


# 額外邊界與方向測資：
# 1) 單點區間 1 1，最大 cycle length 應為 1
# 2) 反向區間 10 1，答案應與 1 10 相同，但輸出仍要保留原輸入順序
EXTRA_CASES = [
    ("1 1\n", "1 1 1\n"),
    ("10 1\n", "10 1 20\n"),
]


def discover_solution_scripts() -> list[Path]:
    """找出需要被測試的解答程式。

    規則：
    - 只找目前資料夾下的 .py 檔。
    - 排除測試檔本身與其他 test_*.py。
    """
    scripts: list[Path] = []
    for path in sorted(BASE_DIR.glob("*.py")):
        if path.name == Path(__file__).name:
            continue
        if path.name.startswith("test_"):
            continue
        scripts.append(path)
    return scripts


def run_script(script_path: Path, input_data: str) -> str:
    """執行解答程式，回傳標準輸出。

    使用與測試環境相同的 Python 直譯器（sys.executable），
    確保執行行為一致。
    """
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        input=input_data,
        text=True,
        capture_output=True,
        cwd=str(BASE_DIR),
        check=False,
    )

    # 若程式異常結束，附上 stderr 便於快速除錯。
    if completed.returncode != 0:
        raise AssertionError(
            f"程式執行失敗：{script_path.name}\n"
            f"return code: {completed.returncode}\n"
            f"stderr:\n{completed.stderr}"
        )

    return completed.stdout


def normalize_output(text: str) -> str:
    """正規化輸出格式，避免平台差異造成誤判。

    規則：
    - 將 Windows 換行（\r\n）統一成 \n。
    - 移除每行尾端空白。
    - 保證最終字串以單一換行結尾，讓比對更穩定。
    """
    normalized_lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]

    # split 後最後一行常是空字串（若原本以換行結尾），這裡移除尾端空行。
    while normalized_lines and normalized_lines[-1] == "":
        normalized_lines.pop()

    return "\n".join(normalized_lines) + "\n"


class TestUVA100Solutions(unittest.TestCase):
    """針對本資料夾所有 UVA 100 解答程式進行驗證。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scripts = discover_solution_scripts()

    def test_found_solution_scripts(self) -> None:
        """至少要有一個可測試的解答程式。"""
        self.assertTrue(
            self.scripts,
            "找不到可測試的解答程式（請先在同資料夾放入 .py 解答檔）。",
        )

    def test_sample_cases(self) -> None:
        """驗證題目提供的標準範例。"""
        expected = normalize_output(SAMPLE_EXPECTED_OUTPUT)

        for script in self.scripts:
            with self.subTest(script=script.name):
                actual = normalize_output(run_script(script, SAMPLE_INPUT))
                self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        """驗證常見邊界與反向區間行為。"""
        for script in self.scripts:
            for case_input, case_expected in EXTRA_CASES:
                with self.subTest(script=script.name, input=case_input.strip()):
                    actual = normalize_output(run_script(script, case_input))
                    expected = normalize_output(case_expected)
                    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
