# QUESTION-10071 測試紀錄

## 測試時間

- 日期：2026-04-16

## 測試檔案

- 正式解答：10071.py
- 簡單版本：10071-easy.py
- 手打版本：10071-manual.py
- 單元測試：test_10071.py

## 測試指令

```bash
c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest weeks/week-07/solutions/0408/test_10071.py -v
```

## 測試說明

- test_10071.py 會自動尋找同資料夾中的 10071.py、10071-easy.py 與 10071-manual.py。
- 每一個測試案例都會對三個解答檔各跑一次，並逐一比對正確答案。
- 正確答案由測試中的暴力法計算，避免人工手算 expected output 出錯。

## 測試結果

```text
test_negative_zero_positive ... ok
test_single_positive_number ... ok
test_single_zero ... ok
test_sparse_values ... ok
test_zero_and_one ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.633s

OK
```

## 結論

- 正式版解答測試通過。
- easy 版本解答測試通過。
- 手打版本解答測試通過。
- 目前 10071 的程式、測試與測試紀錄已可作為提交內容的一部分。
