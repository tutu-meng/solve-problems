def simulate(c, d, T):
    state = {0: T}
    steps = 0
    while True:
        steps += 1
        if steps > 100000:
            return False
        
        p = None
        for pos in sorted(state.keys(), reverse=True):
            if state[pos] >= 2:
                p = pos
                break
        
        if p is None:
            return True
            
        state[p] -= 2
        if state[p] == 0:
            del state[p]
        state[p - d] = state.get(p - d, 0) + 1
        state[p - d - c] = state.get(p - d - c, 0) + 1

def G(c, d):
    T = 1
    while simulate(c, d, T):
        T += 1
    return T - 1

print("G(1, 9) =", G(1, 9))
print("G(1, 10) =", G(1, 10))
print("G(1, 11) =", G(1, 11))
print("G(1, 12) =", G(1, 12))
