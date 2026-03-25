import sys

nums = list(map(int, sys.stdin.read().split()))
if not nums:
    raise SystemExit

t = nums[0]
pos = 1
out = []

for _ in range(t):
    r = nums[pos]
    pos += 1

    arr = nums[pos : pos + r]
    pos += r

    arr.sort()
    pivot = arr[r // 2]

    dist = 0
    for v in arr:
        dist += abs(v - pivot)

    out.append(str(dist))

print("\n".join(out))
