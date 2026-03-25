import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class TestUVA10050(unittest.TestCase):
    """UVA 10050（Hartals）單元測試。"""

    # 可用環境變數 TARGET_SOLUTION 指定受測檔案，預設為 10050.py。
    SOLUTION_FILE = Path(__file__).with_name(os.getenv("TARGET_SOLUTION", "10050.py"))

    def run_solution(self, input_data: str) -> list[str]:
        """執行受測程式並回傳整理後的輸出行。"""
        self.assertTrue(
            self.SOLUTION_FILE.exists(),
            f"找不到受測檔案：{self.SOLUTION_FILE}，請先建立 10050.py",
        )

        # 使用 subprocess 模擬 OJ 的 stdin/stdout 執行環境。
        completed = subprocess.run(
            [sys.executable, str(self.SOLUTION_FILE)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )

        # 去除空白與空行，方便與預期結果逐行比對。
        return [line.strip() for line in completed.stdout.splitlines() if line.strip()]

    @staticmethod
    def expected_lost_days(n: int, parties: list[int]) -> int:
        """計算正確答案：排除週五、週六後的罷會工作天數。"""
        lost = set()

        for h in parties:
            day = h
            while day <= n:
                # 題目規則：第 6、7、13、14... 天是週五、週六，不計入損失工作天。
                if day % 7 not in (6, 0):
                    lost.add(day)
                day += h

        return len(lost)

    def test_basic_cases(self) -> None:
        """測試題目經典案例、重複週期與不同政黨組合。"""
        cases = [
            # 經典案例：題敘中的 N=14, h=[3,4,8]，答案應為 5。
            (14, [3, 4, 8]),
            # 只有一個政黨，每 2 天罷會，需排除週五與週六。
            (14, [2]),
            # 兩個相同週期，重複罷會日不可重複計算。
            (20, [3, 3]),
            # 混合多政黨，檢查跨週與重疊日處理。
            (30, [2, 5, 9]),
        ]

        lines = [str(len(cases))]
        expected = []
        for n, parties in cases:
            lines.append(str(n))
            lines.append(str(len(parties)))
            for h in parties:
                lines.append(str(h))
            expected.append(str(self.expected_lost_days(n, parties)))

        # 額外明確驗證題敘經典案例答案。
        self.assertEqual(self.expected_lost_days(14, [3, 4, 8]), 5)

        input_data = "\n".join(lines) + "\n"
        actual = self.run_solution(input_data)
        self.assertEqual(expected, actual)

    def test_random_cases(self) -> None:
        """隨機測資驗證，避免只通過少數固定樣本。"""
        random.seed(10050)

        cases: list[tuple[int, list[int]]] = []
        for _ in range(25):
            n = random.randint(7, 120)
            p = random.randint(1, 8)

            # 依題意 hi 不為 7 的倍數，這裡用 while 重抽避免違規。
            parties = []
            while len(parties) < p:
                h = random.randint(1, 20)
                if h % 7 != 0:
                    parties.append(h)

            cases.append((n, parties))

        lines = [str(len(cases))]
        expected = []
        for n, parties in cases:
            lines.append(str(n))
            lines.append(str(len(parties)))
            for h in parties:
                lines.append(str(h))
            expected.append(str(self.expected_lost_days(n, parties)))

        input_data = "\n".join(lines) + "\n"
        actual = self.run_solution(input_data)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
