import time

def check_T(c, d, T):
    state_keys = [0] * 16000
    state_vals = [0] * 16000
    state_map = {0: T}
    
    p = 0
    # Process monotonically
    while p >= -12000:
        if p in state_map:
            val = state_map[p]
            if val >= 2:
                num = val // 2
                state_map[p] = val % 2
                
                p1 = p - d
                p2 = p - d - c
                state_map[p1] = state_map.get(p1, 0) + num
                state_map[p2] = state_map.get(p2, 0) + num
        p -= 1
        
    for k, v in state_map.items():
        if v >= 2:
            return False
    return True

start = time.time()
for T in range(1, 100):
    check_T(1, 2, T)
print(time.time() - start)
