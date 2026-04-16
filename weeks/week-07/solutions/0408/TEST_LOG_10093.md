# QUESTION-10093 測試紀錄

## 測試時間

- 日期：2026-04-16

## 測試檔案

- 正式解答：10093.py
- 簡單版本：10093-easy.py
- 手打版本：10093-manual.py
- 單元測試：test_10093.py

## 測試指令

```bash
c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest weeks/week-07/solutions/0408/test_10093.py -v
```

## 測試說明

- test_10093.py 會自動尋找同資料夾中的 10093.py、10093-easy.py 與 10093-manual.py。
- 測試中的 brute_force() 對小型測資用枚舉法算出正確答案，避免人工手算出錯。
- 每個測試案例對三個解答檔各跑一次，逐一比對輸出。

## 測試結果

```text
test_2x2_all_plain ... ok
test_3x3_all_plain ... ok
test_all_mountain ... ok
test_mixed_terrain ... ok
test_mountains_as_blockers ... ok
test_single_col_all_plain ... ok
test_single_mountain ... ok
test_single_plain ... ok
test_single_row_all_plain ... ok

----------------------------------------------------------------------
Ran 9 tests in 1.118s

OK
```

## 結論

- 正式版解答測試通過。
- easy 版本解答測試通過。
- 手打版本解答測試通過。
- 目前 10093 的程式、測試與測試紀錄已可作為提交內容的一部分。
