import random
def simulate(c, d, T):
    state = {0: T}
    active = [0] if T >= 2 else []
    
    steps = 0
    min_pos = 0
    while active:
        steps += 1
        
        p = active.pop()
        if state.get(p, 0) < 2:
            continue
            
        num = state[p] // 2
        state[p] %= 2
        
        for p_new in (p - d, p - d - c):
            state[p_new] = state.get(p_new, 0) + num
            if state[p_new] >= 2 and p_new not in active:
                active.append(p_new)
            if p_new < min_pos:
                min_pos = p_new
                if min_pos < -5000:
                    return False
    return True

monotonic = True
for T in range(1, 200):
    if simulate(1, 2, T) and not simulate(1, 2, T - 1):
        monotonic = False
        print("Not monotonic at", T)

print("Monotonicity:", monotonic)
