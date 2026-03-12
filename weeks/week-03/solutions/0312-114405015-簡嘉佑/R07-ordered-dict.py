# R7. OrderedDict（1.7）

# OrderedDict 是一種「會記住插入順序」的字典。
#
# 補充：在 Python 3.7+ 一般 dict 也會保留插入順序，
# 但在舊版 Python（或需要明確表達順序語意）時，
# OrderedDict 仍是常見教學與相容性做法。
from collections import OrderedDict
import json


# 建立 OrderedDict 物件
d = OrderedDict()

# 依序插入鍵值：先 foo，再 bar
# OrderedDict 會記住這個順序
d['foo'] = 1; d['bar'] = 2

# 轉成 JSON 字串時，鍵的輸出順序會依目前字典順序：
# 預期像是 {"foo": 1, "bar": 2}
# 若改變插入順序，JSON 輸出順序也會跟著改變
json.dumps(d)
