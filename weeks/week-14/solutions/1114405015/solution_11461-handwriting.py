import math

while True:
    a, b = map(int, input().split())
    if a == 0 and b == 0:
        break

    right = math.isqrt(b)
    left = math.isqrt(a - 1) + 1

    if right < left:
        print(0)
    else:
        print(right - left + 1)
