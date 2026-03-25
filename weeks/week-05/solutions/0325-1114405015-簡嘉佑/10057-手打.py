# UVA 10057 - 手打版本
# 觀念：絕對偏差總和在中位數處最小。
# 排序後：lower=(n-1)//2, upper=n//2
# A=xs[lower], cnt=xs.count(A), poss=xs[upper]-xs[lower]+1
import sys

tokens = sys.stdin.read().split()
idx = 0
while idx < len(tokens):
    n = int(tokens[idx]); idx += 1
    xs = [int(tokens[idx + k]) for k in range(n)]
    idx += n
    xs.sort()
    lower = (n - 1) // 2
    upper = n // 2
    a = xs[lower]
    cnt = xs.count(a)
    poss = xs[upper] - xs[lower] + 1
    print(f"{a} {cnt} {poss}")
