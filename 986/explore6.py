def check_T(c, d, T):
    state = {0: T}
    p = 0
    min_p_seen = 0
    
    while True:
        if p not in state or state[p] < 2:
            p -= 1
            if len(state) == 0 or p < min(state.keys()):
                break
            continue
            
        num = state[p] // 2
        state[p] %= 2
        
        state[p - d] = state.get(p - d, 0) + num
        state[p - d - c] = state.get(p - d - c, 0) + num
        
        if p - d - c < -20000:
            return False
            
        p -= 1
        
    return True

print(check_T(2, 1, 7))
print(check_T(2, 1, 8))
