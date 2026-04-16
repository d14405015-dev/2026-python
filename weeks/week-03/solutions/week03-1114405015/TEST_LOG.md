# TEST_LOG

## Run 1（Red）

- Command:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- Summary:
  - total: 15
  - passed: 13
  - failed: 2
- Issue:
  - `test_same_cell_different_direction_not_shared`、`test_scent_allows_following_commands` 失敗，原因是測試預期值與題目規則不一致。
- Fix:
  - 修正測試預期：同格不同方向不共用 scent；第一個危險 `F` 被忽略後仍會繼續執行後續指令。

## Run 2（Green）

- Command:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- Summary:
  - total: 15
  - passed: 15
  - failed: 0
- Change Note:
  - scent 與越界判定修正後，旋轉/越界/scent 三類測試全綠。
