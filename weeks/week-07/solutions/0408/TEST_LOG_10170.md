# QUESTION-10170 測試紀錄

## 測試時間

- 日期：2026-04-16

## 測試檔案

- 正式解答：10170.py
- 簡單版本：10170-easy.py
- 手打版本：10170-manual.py
- 單元測試：test_10170.py

## 測試指令

```bash
c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest weeks/week-07/solutions/0408/test_10170.py -v
```

## 測試說明

- test_10170.py 會自動尋找同資料夾中的 10170.py、10170-easy.py 與 10170-manual.py。
- 測試涵蓋單筆、邊界、多筆 EOF、大數值等情境。
- 預期值由測試內部的數學式與二分搜尋計算，避免手算誤差。

## 測試結果

```text
test_large_day_value ... ok
test_large_day_value_near_limit ... ok
test_multiple_cases_in_one_input ... ok
test_single_case_boundary_of_first_group ... ok
test_single_case_next_group ... ok
test_single_case_start_day ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.713s

OK
```

## 結論

- 正式版解答測試通過。
- easy 版本解答測試通過。
- 手打版本解答測試通過。
- 目前 10170 的程式、測試與測試紀錄已可作為提交內容的一部分。
