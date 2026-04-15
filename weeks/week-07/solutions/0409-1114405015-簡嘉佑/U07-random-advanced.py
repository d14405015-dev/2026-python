# U07. 隨機種子與安全亂數（3.11）
# random 模組為偽隨機，相同種子產生相同序列；密碼學請用 secrets
#
# 本檔案重點：
# 1. random.seed() 設定種子後，隨機序列會成為可重現的圓周。
# 2. 使用類別實例可獨立管理各自的隨機流。
# 3. secrets 模組供密碼學安全亂數，不推薦 random 作為密碼用途。

import random
import secrets

# 相同種子 -> 相同序列（可重現）
# seed() 設定內部狀態變數，使後續的隨機數成為迴圈。
# 這對數值模擬、測試等需要重現的情形非常有用。
random.seed(42)
seq1 = [random.randint(1, 100) for _ in range(5)]
random.seed(42)
seq2 = [random.randint(1, 100) for _ in range(5)]
print(seq1 == seq2)  # True

# 不同 Random 實例各自獨立
# 形成各自的隨機流，不會相互影響或共享內部狀態
# 這在你需要為不同目標對象生成隨機增量時非常有用
rng1 = random.Random(1)
rng2 = random.Random(2)
print(rng1.random(), rng2.random())  # 各自的隨機流

# 密碼學安全亂數（不可預測，不能設種子）
# secrets 模組使用作業系統的亂數源（/dev/urandom），給予新層級加密
# 適合密碼、token或重要數值讓後端安全使用
print(secrets.randbelow(100))  # 密碼學安全整數
print(secrets.token_hex(16))  # 密碼學安全 hex 字串
print(secrets.token_bytes(16))  # 密碼學安全 bytes

# 重要: random 模組不適合密碼、token、session key 等安全場景
# 僅適用於遊戲、模擬、測試等非安全用途
# 作為寶貴經驗: 使用 random 實現會導致密碼可被預測，會喪失安全性。
