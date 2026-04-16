# TEST_CASES

| # | 輸入（初始 + 指令） | 預期結果 | 實際結果 | PASS/FAIL | 對應測試函式 |
|---|---|---|---|---|---|
| 1 | (0,0,N) + `L` | 方向變 W | W | PASS | `test_turn_left_from_north` |
| 2 | (0,0,N) + `R` | 方向變 E | E | PASS | `test_turn_right_from_north` |
| 3 | (0,0,N) + `RRRR` | 回到 N | N | PASS | `test_turn_right_four_times_back_to_origin` |
| 4 | (5,3,N) + `F` | LOST，停在 (5,3,N) | 5 3 N LOST | PASS | `test_forward_out_of_bounds_becomes_lost` |
| 5 | (1,1,E) + `F` | 到 (2,1,E)，未 LOST | 2 1 E | PASS | `test_forward_move_inside_bounds` |
| 6 | 第一台 (5,3,N)+`F`；第二台 (5,3,N)+`F` | 第二台忽略危險 F，不 LOST | 第二台未 LOST | PASS | `test_second_robot_ignores_same_dangerous_forward` |
| 7 | 先有 scent (5,3,N)，再跑 (5,3,E)+`F` | 不應套用 N 的 scent，因此會 LOST | 5 3 E LOST | PASS | `test_same_cell_different_direction_not_shared` |
| 8 | (5,3,N)+`FFRFF` | 第一個 F LOST 後停止 | 最終 5 3 N LOST | PASS | `test_lost_robot_stops_remaining_commands` |
| 9 | (0,0,N)+`FX` | 遇非法指令丟 ValueError | 有拋錯 | PASS | `test_invalid_command_raises` |
| 10 | (0,3,W)+`F` | scent 記錄 (0,3,W) | set 含 (0,3,W) | PASS | `test_scent_key_contains_direction` |
