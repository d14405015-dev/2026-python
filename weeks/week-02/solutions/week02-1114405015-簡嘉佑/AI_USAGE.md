# AI_USAGE

## 1. 我詢問 AI 的問題

- Task 1 去重且保留順序的最佳做法是什麼？
- Task 2 多條件排序 key 要怎麼設計？
- Task 3 使用 Counter 時如何處理空輸入？
- unittest 要如何覆蓋正常、邊界、反例三種案例？

## 2. 我採用的 AI 建議

- 使用 `sorted(..., key=...)` 實作多條件排序。
- 使用 `Counter` 統計 user/action 次數。
- 測試採 `unittest` 並把案例拆成可讀的 `test_...` 函式。

## 3. 我拒絕的 AI 建議

- 拒絕 Task 1 直接用 `set` 當去重輸出，因為會破壞順序，不符題目規格。

## 4. AI 可能誤導但我已修正的案例

- AI 曾建議 Task 3 在 `m = 0` 時不輸出 `top_action`，我改為輸出預設值 `top_action: None 0`，確保格式一致且程式穩定。
