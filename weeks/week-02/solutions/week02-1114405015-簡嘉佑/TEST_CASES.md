# TEST_CASES

## Case 1（一般情況）

- 對應測試：`tests/test_task1.py::test_sample_case`
- 輸入：`5 3 5 2 9 2 8 3 1`
- 預期輸出：
  - `dedupe: 5 3 2 9 8 1`
  - `asc: 1 2 2 3 3 5 5 8 9`
  - `desc: 9 8 5 5 3 3 2 2 1`
  - `evens: 2 2 8`
- 實際輸出：符合預期
- 結果：PASS
- 關鍵修改點：確認去重邏輯不能直接輸出 set。

## Case 2（邊界：空輸入）

- 對應測試：`tests/test_task1.py::test_empty_input`
- 輸入：空行
- 預期輸出：四行皆為空列表結果
- 實際輸出：符合預期
- 結果：PASS
- 關鍵修改點：解析輸入時先做 `strip()`，空字串直接回傳空列表。

## Case 3（Task 2 輸入範例 1）

- 對應測試：`tests/test_task2.py::test_sample_case`
- 輸入：
  ```text
  6 3
  amy 88 20
  bob 88 19
  zoe 92 21
  ian 88 19
  leo 75 20
  eva 92 20
  ```
- 預期輸出：
  ```text
  eva 92 20
  zoe 92 21
  bob 88 19
  ```
- 實際輸出：符合預期
- 結果：PASS
- 關鍵修改點：排序 key 改為 `(-score, age, name)`，再取前 `k` 名。

## Case 4（反例：平手姓名排序）

- 對應測試：`tests/test_task2.py::test_tie_break_by_name`
- 輸入：`[(zoe,80,19), (amy,80,19), (bob,80,19)]`
- 預期輸出：`amy -> bob -> zoe`
- 實際輸出：符合預期
- 結果：PASS
- 關鍵修改點：補上第三層排序條件 `name`。

## Case 5（Task 3 輸入範例 2）

- 對應測試：`tests/test_task3.py::test_sample_case`
- 輸入：
  ```text
  8
  alice login
  bob login
  alice view
  alice logout
  bob view
  bob view
  chris login
  bob logout
  ```
- 預期輸出：
  ```text
  bob 4
  alice 3
  chris 1
  top_action: login 3
  ```
- 實際輸出：符合預期
- 結果：PASS
- 關鍵修改點：使用 `Counter` 統計後，以「次數降冪、名稱升冪」排序。

## Case 6（Task 3 邊界：空紀錄）

- 對應測試：`tests/test_task3.py::test_empty_records`
- 輸入：`m = 0`
- 預期輸出：使用者統計為空、`top_action` 為 `("None", 0)`
- 實際輸出：符合預期
- 結果：PASS
- 關鍵修改點：在 action 統計前先判斷是否為空，避免索引錯誤。
