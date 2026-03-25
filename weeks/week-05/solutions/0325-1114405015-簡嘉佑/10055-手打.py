import sys

nums = list(map(int, sys.stdin.read().split()))
if not nums:
    raise SystemExit

n = nums[0]
q = nums[1]
idx = 2

state = [0] * (n + 1)
ans = []

for _ in range(q):
    v = nums[idx]
    idx += 1

    if v == 1:
        i = nums[idx]
        idx += 1
        state[i] ^= 1
    else:
        l = nums[idx]
        idx += 1
        r = nums[idx]
        idx += 1
        ans.append(str(sum(state[l : r + 1]) % 2))

print("\n".join(ans))
