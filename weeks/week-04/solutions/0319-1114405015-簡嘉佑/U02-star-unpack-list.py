# U2. 星號解包為何能處理「不定長」且結果固定是 list（1.2）

# 範例資料只有姓名與 email，沒有電話欄位
record = ('Dave', 'dave@example.com')
# 一般欄位由 name、email 接收；其餘多出的元素交給 *phones
name, email, *phones = record
# 因為沒有剩餘元素可放入 phones，所以結果是空 list
# phones == []  仍是 list
