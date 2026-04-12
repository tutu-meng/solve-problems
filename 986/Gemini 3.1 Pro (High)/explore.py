def simulate(c, d, T):
    state = {0: T}
    steps = 0
    while True:
        steps += 1
        if steps > 10000:
            return False # Doesn't terminate (glider)
        
        # Find max position with >= 2
        p = None
        for pos in sorted(state.keys(), reverse=True):
            if state[pos] >= 2:
                p = pos
                break
        
        if p is None:
            return True # Terminated
            
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

print("G(2, 1) =", G(2, 1))
print("G(1, 2) =", G(1, 2))
print("G(3, 1) =", G(3, 1))
print("G(2, 2) =", G(2, 2))
print("G(1, 3) =", G(1, 3))

for c in range(1, 6):
    for d in range(1, 6):
        print(f"G({c}, {d}) = {G(c, d)}")
