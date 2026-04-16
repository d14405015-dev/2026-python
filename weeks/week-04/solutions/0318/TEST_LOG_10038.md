# TEST LOG — QUESTION 10038

## 環境
- Python: 3.14.3
- pytest: 9.0.3
- 平台: Windows
- 執行日期: 2026-04-16

## 執行指令
```bash
python -m pytest test_10038.py -v
```

## 測試結果
```text
collected 7 items

test_10038.py::TestQuestion10038::test_large_jump_out_of_range PASSED
test_10038.py::TestQuestion10038::test_missing_difference PASSED
test_10038.py::TestQuestion10038::test_multiple_lines_until_eof PASSED
test_10038.py::TestQuestion10038::test_negative_values_jolly PASSED
test_10038.py::TestQuestion10038::test_repeated_difference PASSED
test_10038.py::TestQuestion10038::test_sample_like_mixed PASSED
test_10038.py::TestQuestion10038::test_single_element_is_jolly PASSED

7 passed, 21 subtests passed in 0.85s
```

## 子測試說明
每個測試案例都會對以下三個版本各跑一次：
- `10038.py`
- `10038-easy.py`
- `10038-manual.py`

共 7 × 3 = 21 個子測試，全部通過。

## 測試覆蓋重點
- 經典範例（Jolly / Not jolly）
- n=1 邊界
- 缺少必要差值
- 差值重複
- 負數序列
- 超範圍差值
- 多筆輸入直到 EOF
