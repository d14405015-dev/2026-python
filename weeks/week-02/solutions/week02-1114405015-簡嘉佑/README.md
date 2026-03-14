# Week 02 作業說明

## 0. 交付檔案清單（與題目順序一致）

```text
week02-1114405015-簡嘉佑/
├── task1_sequence_clean.py
├── task2_student_ranking.py
├── task3_log_summary.py
├── tests/
│   ├── test_task1.py
│   ├── test_task2.py
│   └── test_task3.py
├── TEST_CASES.md
├── TEST_LOG.md
├── AI_USAGE.md
└── README.md
```

## 1. 完成題目清單

- [x] Task 1: Sequence Clean
- [x] Task 2: Student Ranking
- [x] Task 3: Log Summary

## 2. 執行方式

- Python 版本：3.14（建議使用專案虛擬環境）
- 執行 Task 1：`python task1_sequence_clean.py`
- 執行 Task 2：`python task2_student_ranking.py`
- 執行 Task 3：`python task3_log_summary.py`
- 執行測試：`python -m unittest discover -s tests -p "test_*.py" -v`

## 3. 資料結構選擇理由

- Task 1：用 `list` 保存順序、用 `set` 只做「是否出現過」查詢，加速去重判斷。
- Task 2：用 `list[tuple]` 搭配 `sorted(key=...)` 一次完成多條件排序。
- Task 3：用 `Counter` 快速統計 user 與 action 次數，再用排序控制輸出規則。

## 4. 錯誤與修正

- 曾把 Task 1 去重寫成直接輸出 `set`，導致順序錯誤；修正為用 `seen + dedupe list` 保留首次出現順序。

## 5. Red → Green → Refactor 摘要

- Task 1：先寫排序與去重測試（Red），補上核心函式後通過（Green），再拆成 parse/format 函式（Refactor）。
- Task 2：先寫同分年齡與姓名平手規則測試（Red），改用單一 key 排序後通過（Green），再整理輸入輸出函式（Refactor）。
- Task 3：先寫空輸入與同次數排序測試（Red），實作 Counter + 排序後通過（Green），最後抽離格式化輸出（Refactor）。
