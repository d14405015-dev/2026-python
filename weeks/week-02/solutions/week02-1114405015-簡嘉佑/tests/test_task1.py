"""Task 1: Sequence Clean 的單元測試。

使用方式（建議在 solutions/week02-1114405015-簡嘉佑 目錄下執行）：
    python -m unittest discover -s tests -p "test_*.py" -v
"""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


# 以目前測試檔案位置反推作業根目錄
BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = BASE_DIR / "task1_sequence_clean.py"


class TestTask1SequenceClean(unittest.TestCase):
    """針對 Task 1 規格進行測試。"""

    @classmethod
    def setUpClass(cls) -> None:
        # 嘗試匯入學生實作模組（若尚未完成，測試會給出清楚錯誤）
        cls.module = cls._try_import_module()

    @staticmethod
    def _try_import_module():
        if str(BASE_DIR) not in sys.path:
            sys.path.insert(0, str(BASE_DIR))

        try:
            return importlib.import_module("task1_sequence_clean")
        except ModuleNotFoundError:
            return None

    def _run_solver(self, nums: list[int]) -> dict[str, list[int]]:
        """執行學生程式，統一回傳為 dict 結構。

        支援兩種常見作法：
        1) 函式回傳 dict / tuple
        2) 命令列讀 stdin、印出指定格式
        """
        if self.module is not None:
            for fn_name in (
                "sequence_clean",
                "solve_sequence_clean",
                "process_sequence",
                "analyze_numbers",
            ):
                fn = getattr(self.module, fn_name, None)
                if callable(fn):
                    raw = fn(nums)
                    return self._normalize_result(raw)

        # 若沒有可呼叫函式，改用腳本輸入輸出測試
        return self._run_by_cli(nums)

    def _run_by_cli(self, nums: list[int]) -> dict[str, list[int]]:
        self.assertTrue(SCRIPT_PATH.exists(), "找不到 task1_sequence_clean.py，請先建立此檔案")

        input_text = " ".join(map(str, nums)) + "\n"
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
            cwd=str(BASE_DIR),
        )

        self.assertEqual(
            completed.returncode,
            0,
            msg=f"程式執行失敗\nSTDERR:\n{completed.stderr}\nSTDOUT:\n{completed.stdout}",
        )
        return self._parse_stdout(completed.stdout)

    def _normalize_result(self, raw) -> dict[str, list[int]]:
        """把不同回傳格式轉成統一 dict。"""
        if isinstance(raw, dict):
            for key in ("dedupe", "asc", "desc", "evens"):
                self.assertIn(key, raw, f"回傳 dict 缺少鍵：{key}")
            return {
                "dedupe": list(raw["dedupe"]),
                "asc": list(raw["asc"]),
                "desc": list(raw["desc"]),
                "evens": list(raw["evens"]),
            }

        if isinstance(raw, tuple) and len(raw) == 4:
            return {
                "dedupe": list(raw[0]),
                "asc": list(raw[1]),
                "desc": list(raw[2]),
                "evens": list(raw[3]),
            }

        self.fail(
            "函式回傳格式不支援，請回傳 dict(含 dedupe/asc/desc/evens) 或 4 元 tuple"
        )

    def _parse_stdout(self, stdout: str) -> dict[str, list[int]]:
        """解析題目指定輸出格式。"""
        result: dict[str, list[int]] = {}

        for line in stdout.splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            values = value.strip()
            if key in {"dedupe", "asc", "desc", "evens"}:
                result[key] = [int(x) for x in values.split()] if values else []

        for key in ("dedupe", "asc", "desc", "evens"):
            self.assertIn(key, result, f"輸出缺少行：{key}: ...\n目前輸出:\n{stdout}")
        return result

    def _assert_common_rules(self, nums: list[int], got: dict[str, list[int]]) -> None:
        """檢查四項輸出的核心規格。"""
        dedupe_expected = []
        seen = set()
        for n in nums:
            if n not in seen:
                seen.add(n)
                dedupe_expected.append(n)

        self.assertEqual(got["dedupe"], dedupe_expected, "dedupe 應保留第一次出現順序")
        self.assertEqual(got["asc"], sorted(nums), "asc 應為遞增排序")
        self.assertEqual(got["desc"], sorted(nums, reverse=True), "desc 應為遞減排序")
        self.assertEqual(got["evens"], [x for x in nums if x % 2 == 0], "evens 應保留原順序")

    def test_sample_case(self):
        """題目範例：一般情況。"""
        nums = [5, 3, 5, 2, 9, 2, 8, 3, 1]
        got = self._run_solver(nums)
        self._assert_common_rules(nums, got)

    def test_empty_input(self):
        """邊界情況：空輸入。"""
        nums: list[int] = []
        got = self._run_solver(nums)
        self._assert_common_rules(nums, got)

    def test_all_same_numbers(self):
        """重複值極端情況。"""
        nums = [7, 7, 7, 7]
        got = self._run_solver(nums)
        self._assert_common_rules(nums, got)

    def test_all_unique_numbers(self):
        """全部唯一值，dedupe 應與原序列相同。"""
        nums = [4, 1, 9, 0, -3]
        got = self._run_solver(nums)
        self._assert_common_rules(nums, got)

    def test_negative_and_zero(self):
        """包含負數與 0，驗證排序與偶數判斷。"""
        nums = [-2, -1, 0, 3, -2, 4]
        got = self._run_solver(nums)
        self._assert_common_rules(nums, got)

    def test_order_sensitive_dedupe_and_evens(self):
        """容易寫錯的情況：dedupe 與 evens 都要保留原始順序。"""
        nums = [2, 1, 2, 4, 1, 6, 4, 8]
        got = self._run_solver(nums)
        self.assertEqual(got["dedupe"], [2, 1, 4, 6, 8])
        self.assertEqual(got["evens"], [2, 2, 4, 6, 4, 8])


if __name__ == "__main__":
    unittest.main()
