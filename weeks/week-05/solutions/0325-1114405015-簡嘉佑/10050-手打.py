import sys

nums = list(map(int, sys.stdin.read().split()))
if not nums:
    raise SystemExit

t = nums[0]
idx = 1
ans = []

for _ in range(t):
    n = nums[idx]
    idx += 1

    p = nums[idx]
    idx += 1

    hs = nums[idx : idx + p]
    idx += p

    lost = set()

    for h in hs:
        day = h
        while day <= n:
            if day % 7 not in (6, 0):
                lost.add(day)
            day += h

    ans.append(str(len(lost)))

print("\n".join(ans))
