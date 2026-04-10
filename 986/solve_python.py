import math
def check_T(c, d, T):
    state = {0: T}
    p = 0
    min_p_seen = 0
    cutoff = -50000
    while p >= min_p_seen:
        if p in state:
            val = state[p]
            if val >= 2:
                num = val // 2
                state[p] = val % 2
                p1 = p - d
                p2 = p - d - c
                state[p1] = state.get(p1, 0) + num
                state[p2] = state.get(p2, 0) + num
                if p2 < min_p_seen:
                    min_p_seen = p2
                    if min_p_seen < cutoff:
                        return False
        p -= 1
    for v in state.values():
        if v >= 2:
            return False
    return True

def G(c, d):
    low = 1
    high = 1
    while check_T(c, d, high):
        high *= 2
    ans = 1
    while low <= high:
        mid = (low + high) // 2
        if check_T(c, d, mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    return ans

for c in range(1, 20):
    print(G(c, 1), end=" ")
