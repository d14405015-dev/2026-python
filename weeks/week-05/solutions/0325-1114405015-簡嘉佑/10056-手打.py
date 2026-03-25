import sys

tokens = sys.stdin.read().split()
idx = 0
s = int(tokens[idx]); idx += 1
for _ in range(s):
    n = int(tokens[idx]);   idx += 1
    p = float(tokens[idx]); idx += 1
    i = int(tokens[idx]);   idx += 1
    q = 1.0 - p
    if p >= 1.0:
        prob = 1.0 if i == 1 else 0.0
    else:
        prob = (q ** (i - 1)) * p / (1.0 - q ** n)
    print(f"{prob:.4f}")
