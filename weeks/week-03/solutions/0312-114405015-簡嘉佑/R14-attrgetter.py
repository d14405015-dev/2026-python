# R14. 物件排序 attrgetter（1.14）

# `attrgetter` 來自 `operator` 模組。
# 它的用途是：快速建立一個「取物件屬性」的函式，
# 常搭配 sorted(..., key=...) 做排序。
from operator import attrgetter


# 定義一個簡單的 User 類別。
class User:
    # 建構子：建立物件時把傳入的 user_id 存成屬性。
    def __init__(self, user_id):
        self.user_id = user_id


# 建立三個 User 物件，user_id 分別是 23、3、99。
users = [User(23), User(3), User(99)]

# 依據 `user_id` 屬性做遞增排序。
# `attrgetter('user_id')` 等價於：lambda obj: obj.user_id
# 排序後順序會是：3, 23, 99
sorted(users, key=attrgetter('user_id'))
