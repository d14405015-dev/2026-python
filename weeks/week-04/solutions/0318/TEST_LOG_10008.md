# TEST LOG — QUESTION 10008

## 環境
- Python: 3.14.3
- pytest: 9.0.3
- 平台: Windows
- 執行日期: 2026-04-16

## 執行指令
```
python -m pytest test_10008.py -v
```

## 測試結果
```
collected 7 items

test_10008.py::TestQuestion10008::test_case1_basic PASSED
test_10008.py::TestQuestion10008::test_case2_single_letter PASSED
test_10008.py::TestQuestion10008::test_case3_empty_lines PASSED
test_10008.py::TestQuestion10008::test_case4_only_numbers_and_spaces PASSED
test_10008.py::TestQuestion10008::test_case5_all_same_count PASSED
test_10008.py::TestQuestion10008::test_case6_multiline_accumulate PASSED
test_10008.py::TestQuestion10008::test_case7_longer_sentence PASSED

==================== 7 passed, 21 subtests passed in 0.87s ====================
```

## 子測試說明
每個測試案例對 `10008.py`、`10008-easy.py`、`10008-manual.py` 各跑一次（共 21 個子測試），全部通過。

## 測試案例說明
| # | 測試名稱 | 描述 | 預期輸出重點 |
|---|---------|------|------------|
| 1 | test_case1_basic | Hello World 大小寫混合 | L 3, O 2, 其餘 1 |
| 2 | test_case2_single_letter | 只有字母 a | A 1 |
| 3 | test_case3_empty_lines | 多列含空行，A=B=3 | 次數相同按字母序 |
| 4 | test_case4_only_numbers_and_spaces | 只有數字與空白 | 無輸出 |
| 5 | test_case5_all_same_count | abcde 各 1 次 | A B C D E 各 1 |
| 6 | test_case6_multiline_accumulate | 跨列累加 aA/Bb/CC | A=B=C=2 |
| 7 | test_case7_longer_sentence | The quick brown fox | O 2, 其餘 1 |
