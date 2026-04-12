import math

def check_T_spread(c, d, T):
    state = {0: T}
    p = 0
    min_p_seen = 0
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
        p -= 1
    for v in state.values():
        if v >= 2:
            return -1 # escaped
    return min_p_seen

def G_with_spread(c, d):
    low = 1
    high = 1
    
    # Binary search using a very large cutoff internally to find G safely
    def safe_check(T):
        state = {0: T}
        p = 0
        min_p = 0
        while p >= min_p:
            if p in state:
                val = state[p]
                if val >= 2:
                    num = val // 2
                    state[p] = val % 2
                    p1 = p - d
                    p2 = p - d - c
                    state[p1] = state.get(p1, 0) + num
                    state[p2] = state.get(p2, 0) + num
                    if p2 < min_p:
                        min_p = p2
                        if min_p < -500000:
                            return False
            p -= 1
        for v in state.values():
            if v >= 2: return False
        return True

    while safe_check(high):
        high *= 2
    ans = 1
    while low <= high:
        mid = (low + high) // 2
        if safe_check(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    spread = check_T_spread(c, d, ans)
    return ans, spread

max_spread = 0
for c in range(1, 15):
    for d in range(1, 15):
        if math.gcd(c, d) == 1:
            ans, spread = G_with_spread(c, d)
            if spread < max_spread:
                max_spread = spread

print("Max spread for c,d <= 15 is", max_spread)
