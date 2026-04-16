# QUESTION-10062 測試紀錄

## 測試時間

- 日期：2026-04-16

## 測試檔案

- 解答程式：10062.py
- 簡單版本：10062-easy.py
- 手打版本：10062-manual.py
- 單元測試：test_10062.py

## 測試指令

```bash
c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest weeks/week-07/solutions/0408/test_10062.py -v
```

## 測試說明

- test_10062.py 會自動尋找同資料夾中的 10062.py、10062-easy.py 與 10062-manual.py。
- 每一個測試案例都會對三個解答檔各跑一次，並逐行比對標準輸出。
- 因此下列 6 個測試全部通過，代表正式版、easy 版與手打版都通過相同測資。

## 測試結果

```text
test_already_sorted ... ok
test_another_mixed_order_case ... ok
test_completely_descending ... ok
test_mixed_order_case ... ok
test_single_cow ... ok
test_two_cows_reverse_order ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.729s

OK
```

## 結論

- 正式版解答測試通過。
- easy 版本解答測試通過。
- 手打版本解答測試通過。
- 目前資料夾中的程式與測試可作為提交內容的一部分。