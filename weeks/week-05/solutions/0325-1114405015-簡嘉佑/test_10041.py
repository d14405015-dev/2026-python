import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class TestUVA10041(unittest.TestCase):
    """UVA 10041（Vito's Family）單元測試。"""

    # 可透過環境變數 TARGET_SOLUTION 指定受測檔案，
    # 未指定時預設測 10041.py。
    SOLUTION_FILE = Path(__file__).with_name(os.getenv("TARGET_SOLUTION", "10041.py"))

    def run_solution(self, input_data: str) -> list[str]:
        """執行受測程式，回傳去除空白後的輸出行。"""
        # 先確認受測檔案存在，避免測試失敗原因不明確。
        self.assertTrue(
            self.SOLUTION_FILE.exists(),
            f"找不到受測檔案：{self.SOLUTION_FILE}，請先建立 10041.py",
        )

        # 透過 subprocess 模擬 OJ 的標準輸入/輸出執行方式。
        completed = subprocess.run(
            [sys.executable, str(self.SOLUTION_FILE)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )

        # 要求程式正常結束（return code = 0），否則印出錯誤訊息方便除錯。
        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )

        # 逐行清理輸出空白，避免末尾空行影響比對。
        return [line.strip() for line in completed.stdout.splitlines() if line.strip()]

    @staticmethod
    def expected_min_sum(addresses: list[int]) -> int:
        """以中位數計算最小總距離。"""
        # 中位數性質：可使一維絕對距離總和最小。
        arr = sorted(addresses)
        median = arr[len(arr) // 2]
        return sum(abs(x - median) for x in arr)

    def test_basic_and_duplicate_cases(self) -> None:
        """測試基本案例、重複地址與偶數筆資料。"""
        # 固定測資涵蓋：奇數個地址、偶數個地址、重複地址、單一地址。
        input_data = "\n".join(
            [
                "6",
                "2 2 4",
                "3 2 4 6",
                "4 2 4 6 8",
                "5 10 2 14 4 7",
                "6 10 10 10 10 10 10",
                "1 12345",
            ]
        ) + "\n"

        # 每筆測資對應一行預期輸出。
        expected = ["2", "4", "8", "18", "0", "0"]
        actual = self.run_solution(input_data)
        self.assertEqual(expected, actual)

    def test_random_cases(self) -> None:
        """隨機小資料驗證，避免只對固定測資過關。"""
        # 固定亂數種子，確保每次測試可重現。
        random.seed(10041)
        cases: list[list[int]] = []
        for _ in range(20):
            r = random.randint(1, 10)
            addresses = [random.randint(1, 50) for _ in range(r)]
            cases.append(addresses)

        # 組裝成題目指定的輸入格式：第一行為筆數，後續每行為一組測資。
        lines = [str(len(cases))]
        for addresses in cases:
            lines.append(f"{len(addresses)} " + " ".join(map(str, addresses)))
        input_data = "\n".join(lines) + "\n"

        # 預期值用正確演算法即時計算，與受測程式輸出逐行比對。
        expected = [str(self.expected_min_sum(addresses)) for addresses in cases]
        actual = self.run_solution(input_data)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
