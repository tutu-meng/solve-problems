def simulate(c, d, T):
    state = {0: T}
    steps = 0
    while True:
        steps += 1
        if steps > 20000:
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

print("d: 1 2 3 4 5 6 7 8")
for c in range(1, 9):
    line = f"c={c}: "
    for d in range(1, 9):
        line += f"{G(c, d):4} "
    print(line)
