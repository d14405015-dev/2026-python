"""Task 3: Log Summary 單元測試。"""

from __future__ import annotations

import unittest

from task3_log_summary import summarize_logs


class TestTask3LogSummary(unittest.TestCase):
    """驗證使用者統計排序與全域 top_action。"""

    def test_sample_case(self):
        records = [
            ("alice", "login"),
            ("bob", "login"),
            ("alice", "view"),
            ("alice", "logout"),
            ("bob", "view"),
            ("bob", "view"),
            ("chris", "login"),
            ("bob", "logout"),
        ]
        user_summary, top_action = summarize_logs(records)
        self.assertEqual(user_summary, [("bob", 4), ("alice", 3), ("chris", 1)])
        self.assertEqual(top_action, ("login", 3))

    def test_empty_records(self):
        user_summary, top_action = summarize_logs([])
        self.assertEqual(user_summary, [])
        self.assertEqual(top_action, ("None", 0))

    def test_tie_user_count_and_action(self):
        records = [
            ("alice", "view"),
            ("bob", "view"),
            ("alice", "login"),
            ("bob", "login"),
        ]
        user_summary, top_action = summarize_logs(records)
        self.assertEqual(user_summary, [("alice", 2), ("bob", 2)])
        # action 次數同分時採字母序，login 應在 view 前面
        self.assertEqual(top_action, ("login", 2))


if __name__ == "__main__":
    unittest.main()
