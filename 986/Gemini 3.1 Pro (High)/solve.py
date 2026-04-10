import math
from multiprocessing import Pool
import sys

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

def worker(args):
    c, d = args
    if math.gcd(c, d) != 1:
        return 0, 0, 0
    ans = G(c, d)
    return c, d, ans

if __name__ == '__main__':
    max_val = 160
    tasks = []
    for c in range(1, max_val + 1):
        for d in range(1, max_val + 1):
            if math.gcd(c, d) == 1:
                tasks.append((c, d))
                
    print(f"Total tasks: {len(tasks)}")
    
    dp_G = {}
    with Pool() as pool:
        for i, (c, d, ans) in enumerate(pool.imap_unordered(worker, tasks)):
            dp_G[(c, d)] = ans
            if i % 1000 == 0:
                print(f"Progress: {i}/{len(tasks)}")
                sys.stdout.flush()
                
    total_sum = 0
    for c in range(1, max_val + 1):
        for d in range(1, max_val + 1):
            g = math.gcd(c, d)
            total_sum += dp_G[(c // g, d // g)]
            
    print("FINAL SUM:", total_sum)
