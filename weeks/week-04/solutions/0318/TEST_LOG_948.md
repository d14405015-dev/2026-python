# TEST LOG — QUESTION 948

## 環境
- Python: 3.14.3
- pytest: 9.0.3
- 平台: Windows
- 執行日期: 2026-04-16

## 執行指令
```
python -m pytest test_948.py -v
```

## 測試結果（含手打版 948-manual.py）
```
collected 6 items

test_948.py::TestQuestion948::test_case1_find_heavy_coin PASSED
test_948.py::TestQuestion948::test_case2_ambiguous_one_weighing PASSED
test_948.py::TestQuestion948::test_case3_coin_not_weighed PASSED
test_948.py::TestQuestion948::test_case4_find_heavy_coin_excluded PASSED
test_948.py::TestQuestion948::test_case5_three_weighings_narrow_down PASSED
test_948.py::TestQuestion948::test_case6_multiple_test_cases PASSED

==================== 6 passed, 18 subtests passed in 0.82s ====================
```

## 子測試說明
每個測試案例對 `948.py`、`948-easy.py`、`948-manual.py` 各跑一次（共 18 個子測試），全部通過。

## 測試案例說明
| # | 測試名稱 | 描述 | 預期輸出 |
|---|---------|------|---------|
| 1 | test_case1_find_heavy_coin | 3 枚硬幣，兩次秤重，確認硬幣 2 偏重 | `2` |
| 2 | test_case2_ambiguous_one_weighing | 4 枚硬幣，一次秤重，4 種可能無法確定 | `0` |
| 3 | test_case3_coin_not_weighed | 硬幣 1 vs 2 等重，假幣必是硬幣 3 | `3` |
| 4 | test_case4_find_heavy_coin_excluded | 5 枚硬幣，= 排除 4 枚後確認硬幣 5 偏重 | `5` |
| 5 | test_case5_three_weighings_narrow_down | 6 枚硬幣，三次秤重縮小至硬幣 3 偏重 | `3` |
| 6 | test_case6_multiple_test_cases | M=3 多組，驗證空白列分隔格式 | `2` / `0` / `3` |
