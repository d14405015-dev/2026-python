# TEST LOG — QUESTION 10019

## 環境
- Python: 3.14.3
- pytest: 9.0.3
- 平台: Windows
- 執行日期: 2026-04-16

## 執行指令
```bash
python -m pytest test_10019.py -v
```

## 測試結果
```text
collected 6 items

test_10019.py::TestQuestion10019::test_input_with_extra_spaces PASSED
test_10019.py::TestQuestion10019::test_large_numbers PASSED
test_10019.py::TestQuestion10019::test_multiple_lines_until_eof PASSED
test_10019.py::TestQuestion10019::test_reversed_order PASSED
test_10019.py::TestQuestion10019::test_same_numbers PASSED
test_10019.py::TestQuestion10019::test_single_case PASSED

6 passed, 18 subtests passed in 0.74s
```

## 子測試說明
每個測試案例都會對以下兩個版本各跑一次：
- `10019.py`
- `10019-easy.py`

並包含手打版：
- `10019-manual.py`

共 6 × 3 = 18 個子測試，全部通過。

## 測試覆蓋重點
- 基本單筆差值
- 相同數值差為 0
- 反向輸入（大數在前）仍取絕對值
- 多筆輸入讀到 EOF
- 接近 64-bit 範圍的大數
- 含多餘空白的輸入解析
