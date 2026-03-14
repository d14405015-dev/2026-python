# TEST_LOG

## 2026-03-14 測試紀錄（Red）

- 執行目錄：`weeks/week-02/solutions/week02-1114405015-簡嘉佑`
- 執行指令：`c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py" -v`
- 測試總數：6
- 通過數：6
- 失敗數：2（Task 2/Task 3 模組匯入錯誤）
- 結果：FAIL（尚未全數通過）

### 測試摘要

```text
test_all_same_numbers (test_task1.TestTask1SequenceClean.test_all_same_numbers) ... ok
test_all_unique_numbers (test_task1.TestTask1SequenceClean.test_all_unique_numbers) ... ok
test_empty_input (test_task1.TestTask1SequenceClean.test_empty_input) ... ok
test_negative_and_zero (test_task1.TestTask1SequenceClean.test_negative_and_zero) ... ok
test_order_sensitive_dedupe_and_evens (test_task1.TestTask1SequenceClean.test_order_sensitive_dedupe_and_evens) ... ok
test_sample_case (test_task1.TestTask1SequenceClean.test_sample_case) ... ok
ERROR: test_task2 (unittest.loader._FailedTest.test_task2)
ERROR: test_task3 (unittest.loader._FailedTest.test_task3)
```

### 從失敗到通過的關鍵修改

- 新增 `task2_student_ranking.py`、`task3_log_summary.py`，補上 Task 2/3 核心邏輯。
- 新增 `tests/test_task2.py`、`tests/test_task3.py`，完成三題測試覆蓋。

## 2026-03-14 測試紀錄（Green）

- 執行目錄：`weeks/week-02/solutions/week02-1114405015-簡嘉佑`
- 執行指令：`c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py" -v`
- 測試總數：6
- 通過數：6
- 失敗數：0
- 結果：PASS（全部通過）

### 測試摘要

```text
test_all_same_numbers (test_task1.TestTask1SequenceClean.test_all_same_numbers) ... ok
test_all_unique_numbers (test_task1.TestTask1SequenceClean.test_all_unique_numbers) ... ok
test_empty_input (test_task1.TestTask1SequenceClean.test_empty_input) ... ok
test_negative_and_zero (test_task1.TestTask1SequenceClean.test_negative_and_zero) ... ok
test_order_sensitive_dedupe_and_evens (test_task1.TestTask1SequenceClean.test_order_sensitive_dedupe_and_evens) ... ok
test_sample_case (test_task1.TestTask1SequenceClean.test_sample_case) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.005s

OK
```

### 本次修正摘要

- 新增 `task1_sequence_clean.py`，實作去重（保留順序）、升冪排序、降冪排序、偶數過濾。
- 加上命令列輸入輸出介面，確保可被測試程式以腳本模式驗證。

## 2026-03-14 測試紀錄（Green, Full Suite）

- 執行目錄：`weeks/week-02/solutions/week02-1114405015-簡嘉佑`
- 執行指令：`c:/Users/user/Desktop/1114405015/.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py" -v`
- 測試總數：12
- 通過數：12
- 失敗數：0
- 結果：PASS（全部通過）

### 測試摘要

```text
test_all_same_numbers (test_task1.TestTask1SequenceClean.test_all_same_numbers) ... ok
test_all_unique_numbers (test_task1.TestTask1SequenceClean.test_all_unique_numbers) ... ok
test_empty_input (test_task1.TestTask1SequenceClean.test_empty_input) ... ok
test_negative_and_zero (test_task1.TestTask1SequenceClean.test_negative_and_zero) ... ok
test_order_sensitive_dedupe_and_evens (test_task1.TestTask1SequenceClean.test_order_sensitive_dedupe_and_evens) ... ok
test_sample_case (test_task1.TestTask1SequenceClean.test_sample_case) ... ok
test_sample_case (test_task2.TestTask2StudentRanking.test_sample_case) ... ok
test_tie_break_by_age (test_task2.TestTask2StudentRanking.test_tie_break_by_age) ... ok
test_tie_break_by_name (test_task2.TestTask2StudentRanking.test_tie_break_by_name) ... ok
test_empty_records (test_task3.TestTask3LogSummary.test_empty_records) ... ok
test_sample_case (test_task3.TestTask3LogSummary.test_sample_case) ... ok
test_tie_user_count_and_action (test_task3.TestTask3LogSummary.test_tie_user_count_and_action) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.007s

OK
```

### 本次修正摘要

- 新增 Task 2 與 Task 3 程式檔，補齊作業要求的三題主程式。
- 新增 `tests/test_task2.py`、`tests/test_task3.py`，補齊每題至少 3 筆測試。
- 新增 `README.md`、`TEST_CASES.md`、`AI_USAGE.md`，完成交付文件框架。
