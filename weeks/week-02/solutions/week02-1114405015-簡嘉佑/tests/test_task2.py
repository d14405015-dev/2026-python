"""Task 2: Student Ranking 單元測試。"""

from __future__ import annotations

import unittest

from task2_student_ranking import rank_students


class TestTask2StudentRanking(unittest.TestCase):
    """驗證 score / age / name 三層排序規則。"""

    def test_sample_case(self):
        students = [
            ("amy", 88, 20),
            ("bob", 88, 19),
            ("zoe", 92, 21),
            ("ian", 88, 19),
            ("leo", 75, 20),
            ("eva", 92, 20),
        ]
        got = rank_students(students, 3)
        self.assertEqual(got, [("eva", 92, 20), ("zoe", 92, 21), ("bob", 88, 19)])

    def test_tie_break_by_age(self):
        students = [("ann", 90, 22), ("ben", 90, 20), ("cat", 90, 21)]
        got = rank_students(students, 3)
        self.assertEqual(got, [("ben", 90, 20), ("cat", 90, 21), ("ann", 90, 22)])

    def test_tie_break_by_name(self):
        students = [("zoe", 80, 19), ("amy", 80, 19), ("bob", 80, 19)]
        got = rank_students(students, 3)
        self.assertEqual(got, [("amy", 80, 19), ("bob", 80, 19), ("zoe", 80, 19)])


if __name__ == "__main__":
    unittest.main()
