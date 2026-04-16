# QUESTION-10101 測試紀錄

## 測試時間

- 日期：2026-04-16

## 測試檔案

- 正式解答：10101.py
- 簡單版本：10101-easy.py
- 手打版本：10101-manual.py
- 單元測試：test_10101.py

## 測試指令

```bash
c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest weeks/week-07/solutions/0408/test_10101.py -v
```

## 測試說明

- test_10101.py 會自動尋找同資料夾中的 10101.py、10101-easy.py 與 10101-manual.py。
- 測試不綁定單一答案字串，而是驗證輸出是否為「合法的一根木棒移動解」。
- 若某測資無解，測試會要求程式輸出 No。

## 測試結果

```text
test_addition_case ... ok
test_already_true_equation ... ok
test_hash_suffix_ignored ... ok
test_multi_digit_case ... ok
test_no_solution_case ... ok
test_subtraction_case ... ok
test_with_zero ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.842s

OK
```

## 結論

- 正式版解答測試通過。
- easy 版本解答測試通過。
- 手打版本解答測試通過。
- 目前 10101 的程式、測試與測試紀錄已可作為提交內容的一部分。
