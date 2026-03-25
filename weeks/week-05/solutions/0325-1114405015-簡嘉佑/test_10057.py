"""UVA 10057 單元測試 — A Weird Calculator

題目摘要：
  給定 n 個無號整數 X1, X2, ..., Xn，
  找一個整數 A 使得下式的值最小：
    |X1 - A| + |X2 - A| + ... + |Xn - A|

  對每組測資輸出三個整數（以空白隔開放在同一行）：
    1. A     ：讓算式達到最小值的整數（若有多個可行值，取最小）
    2. cnt   ：在所有 |Xi - A| 中，等於最小值（0）的個數
              （即陣列中有幾個元素恰好等於 A）
    3. poss  ：能讓算式達到最小值的 A 共有幾種可能整數

數學觀念：
  統計學定理：絕對偏差總和在 A = 中位數 時最小。

  ┌─────────────────────────────────────────────────────────────────┐
  │ 設排序後陣列為 X[0] ≤ X[1] ≤ … ≤ X[n-1]，索引從 0 開始。       │
  │                                                                   │
  │ ‧ n 為奇數：只有一個中位數 X[n//2]，A 唯一。                   │
  │ ‧ n 為偶數：下中位數 X[n//2-1] 到上中位數 X[n//2] 之間（含）   │
  │             的所有整數，都能讓總和相同（且最小）。              │
  │             可行 A 數量 = X[n//2] - X[n//2-1] + 1              │
  │                                                                   │
  │ 統一寫法（0-indexed）：                                           │
  │   lower_idx = (n - 1) // 2  → 下中位數索引（含奇偶）           │
  │   upper_idx = n // 2         → 上中位數索引（含奇偶）           │
  │   A    = X[lower_idx]                                            │
  │   poss = X[upper_idx] - X[lower_idx] + 1                        │
  │                                                                   │
  │ 因為 A 必為陣列中某個元素，所以個別最小差值恆為 0，             │
  │ cnt = 陣列中等於 A 的元素個數（即 A 的出現頻率）。              │
  └─────────────────────────────────────────────────────────────────┘

  範例驗證（n=4, X=[1,2,5,8]）：
    排序：[1, 2, 5, 8]
    lower=X[1]=2，upper=X[2]=5
    A=2，cnt=1（只有一個 2），poss=5-2+1=4
    → 輸出：2 1 4

輸入格式：
  多組測資，直到 EOF。
  每組第一行為 n（0 < n < 1000），
  接下來 n 個整數，所有數字均 < 65536。

輸出格式：
  每組測資輸出一行，包含三個整數以空白分隔：A cnt poss。

使用方式：
  python test_10057.py                          # 測試 10057.py（預設）
  TARGET_SOLUTION=10057-manual.py python test_10057.py  # 測試手打版本
"""

import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class TestUVA10057(unittest.TestCase):
    """UVA 10057（絕對偏差最小化 / 中位數問題）單元測試。"""

    # 透過環境變數 TARGET_SOLUTION 指定受測檔案，預設為 10057.py。
    # 這樣同一份測試就能同時驗證 10057.py 和 10057-manual.py。
    SOLUTION_FILE = Path(__file__).with_name(
        os.getenv("TARGET_SOLUTION", "10057.py")
    )

    # ------------------------------------------------------------------ #
    # 輔助方法                                                             #
    # ------------------------------------------------------------------ #

    def run_solution(self, input_data: str) -> list[str]:
        """執行受測程式，以 stdin 傳入題目輸入，回傳整理後的輸出行列表。

        先確認受測檔案存在，再透過 subprocess 模擬 OJ 的 stdin/stdout 環境。
        """
        # 若受測檔案不存在，提前給出明確錯誤訊息。
        self.assertTrue(
            self.SOLUTION_FILE.exists(),
            f"找不到受測檔案：{self.SOLUTION_FILE}，請先建立 10057.py",
        )

        # check=False：不讓 subprocess 自動拋出例外，
        # 改由下方的 assertEqual 輸出可讀性更高的錯誤訊息。
        completed = subprocess.run(
            [sys.executable, str(self.SOLUTION_FILE)],
            input=input_data,
            text=True,
            capture_output=True,  # 同時捕捉 stdout 與 stderr，避免混進終端機
            check=False,
        )

        # 程式必須正常結束（return code = 0），非零代表程式崩潰。
        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )

        # 去除空白行與前後空白，避免格式差異影響比對。
        return [line.strip() for line in completed.stdout.splitlines() if line.strip()]

    @staticmethod
    def oracle(xs: list[int]) -> tuple[int, int, int]:
        """以排序 + 中位數公式計算三個輸出值，作為測試的參考正解。

        Returns:
            (a_val, cnt_min_diff, cnt_possible)
            a_val         : 下中位數，即可行 A 範圍的最小值
            cnt_min_diff  : 陣列中等於 a_val 的元素個數（個別最小差值為 0）
            cnt_possible  : 可使總和最小的 A 的整數種數
        """
        n = len(xs)
        xs_sorted = sorted(xs)  # 先排序，後續透過索引取中位數

        # 下中位數索引：
        #   n=1 → (1-1)//2=0；n=2 → 0；n=3 → 1；n=4 → 1；n=5 → 2
        lower_idx = (n - 1) // 2

        # 上中位數索引：
        #   n=1 → 1//2=0；n=2 → 1；n=3 → 1；n=4 → 2；n=5 → 2
        upper_idx = n // 2

        # A 取下中位數（可行 A 範圍的最小整數）。
        a_val = xs_sorted[lower_idx]

        # 因為 a_val 是陣列中的某個元素，所以個別最小差值必為 0，
        # 故 cnt = 陣列中等於 a_val 的元素個數。
        cnt_min_diff = xs_sorted.count(a_val)

        # 可行 A 的整數個數 = 上中位數 - 下中位數 + 1。
        # n 為奇數時 upper_idx == lower_idx，結果恆為 1。
        cnt_possible = xs_sorted[upper_idx] - xs_sorted[lower_idx] + 1

        return a_val, cnt_min_diff, cnt_possible

    @staticmethod
    def build_input(cases: list[list[int]]) -> str:
        """把測試案例清單組成題目要求的輸入格式字串。

        格式：每組測資先輸出 n，再於下一行輸出 n 個整數（空白分隔）。
        題目讀到 EOF 為止，不需額外的結束標記。
        """
        lines: list[str] = []
        for xs in cases:
            # 第一行：元素個數 n
            lines.append(str(len(xs)))
            # 第二行：n 個整數，以空白分隔
            lines.append(" ".join(map(str, xs)))
        return "\n".join(lines) + "\n"

    def assert_cases(
        self,
        actual: list[str],
        cases: list[list[int]],
        label: str = "",
    ) -> None:
        """逐行比較受測程式輸出與 oracle 計算結果。

        每行預期格式為「A cnt poss」（三個整數，空白分隔）。
        先確認行數相符，再逐行比對三個值。
        """
        prefix = f"[{label}]" if label else ""

        # 確認輸出行數正確。
        self.assertEqual(
            len(actual),
            len(cases),
            msg=f"{prefix}輸出行數 {len(actual)} 與案例數 {len(cases)} 不符",
        )

        for idx, (xs, line) in enumerate(zip(cases, actual)):
            exp_a, exp_cnt, exp_poss = self.oracle(xs)

            # 每行應恰好包含三個欄位。
            parts = line.split()
            self.assertEqual(
                len(parts),
                3,
                msg=f"{prefix}第 {idx + 1} 組輸出欄位數不是 3：{line!r}",
            )

            # 解析輸出的三個整數。
            try:
                got_a, got_cnt, got_poss = int(parts[0]), int(parts[1]), int(parts[2])
            except ValueError:
                self.fail(f"{prefix}第 {idx + 1} 組輸出無法解析為三個整數：{line!r}")

            # 逐字段比對，錯誤時顯示輸入資料方便除錯。
            self.assertEqual(
                got_a, exp_a,
                msg=f"{prefix}第 {idx + 1} 組 A 值錯誤（input={xs}，預期={exp_a}，輸出={got_a}）",
            )
            self.assertEqual(
                got_cnt, exp_cnt,
                msg=f"{prefix}第 {idx + 1} 組 cnt 錯誤（input={xs}，預期={exp_cnt}，輸出={got_cnt}）",
            )
            self.assertEqual(
                got_poss, exp_poss,
                msg=f"{prefix}第 {idx + 1} 組 poss 錯誤（input={xs}，預期={exp_poss}，輸出={got_poss}）",
            )

    # ------------------------------------------------------------------ #
    # 測試案例                                                             #
    # ------------------------------------------------------------------ #

    def test_basic_case(self) -> None:
        """固定案例：涵蓋各種典型情境，驗證關鍵邊界與邏輯。

        設計依據：
          ‧ n=1：最小案例，A 必為唯一元素。
          ‧ n 奇數、唯一中位數：poss 必為 1。
          ‧ n 偶數、下中位數 ≠ 上中位數：poss > 1。
          ‧ 重複元素：cnt > 1 且 poss 可能為 1。
          ‧ 輸入未排序：程式應自行排序。
          ‧ 接近上限值（65535）：測試大數值正確性。
        """
        cases: list[list[int]] = [
            # ── n=1，單一元素 ─────────────────────────────────────
            [5],                   # A=5, cnt=1, poss=1

            # ── n=3，奇數，唯一中位數 ─────────────────────────────
            [1, 2, 10],            # sorted→[1,2,10], A=2, cnt=1, poss=1
            [10, 2, 1],            # 輸入順序不同，答案應與上一組相同

            # ── n=5，奇數 ─────────────────────────────────────────
            [3, 1, 4, 1, 5],       # sorted→[1,1,3,4,5], A=3, cnt=1, poss=1

            # ── n=2，偶數，下≠上 ──────────────────────────────────
            [3, 7],                # A=3, cnt=1, poss=7-3+1=5
            [4, 4],                # 兩個相同，A=4, cnt=2, poss=1

            # ── n=4，偶數，下≠上 ──────────────────────────────────
            [1, 2, 5, 8],          # A=2, cnt=1, poss=5-2+1=4

            # ── n=4，偶數，重複中位數（下=上）────────────────────
            [1, 2, 2, 5],          # A=2, cnt=2（兩個2）, poss=2-2+1=1

            # ── 大數值，接近題目上限 65535 ────────────────────────
            [65530, 65533, 65535], # A=65533, cnt=1, poss=1

            # ── 全部相同 ──────────────────────────────────────────
            [7, 7, 7, 7],          # A=7, cnt=4, poss=1
        ]

        input_data = self.build_input(cases)
        actual = self.run_solution(input_data)
        # 以 oracle 逐組比對三個輸出值。
        self.assert_cases(actual, cases, label="固定案例")

    def test_random_cases(self) -> None:
        """隨機產生 40 組陣列，以 oracle 公式全部比對。

        固定亂數種子 10057，確保每次執行產生相同資料，便於重現比對。
        n 範圍：1 ～ 20；元素值範圍：0 ～ 65535（符合題目限制）。
        """
        # 固定亂數種子，確保測試可重現。
        random.seed(10057)

        cases: list[list[int]] = []
        for _ in range(40):
            # n 介於 1 ～ 20，涵蓋奇偶兩種情形。
            n = random.randint(1, 20)
            # 元素值符合題目「小於 65536」的限制（即 0 ～ 65535）。
            xs = [random.randint(0, 65535) for _ in range(n)]
            cases.append(xs)

        input_data = self.build_input(cases)
        actual = self.run_solution(input_data)
        # 與 oracle 逐組比對；任何一組不符即判定失敗。
        self.assert_cases(actual, cases, label="隨機案例")


if __name__ == "__main__":
    # verbosity=2：逐個顯示測試方法名稱與 ok/FAIL，方便在終端機直接確認結果。
    unittest.main(verbosity=2)
