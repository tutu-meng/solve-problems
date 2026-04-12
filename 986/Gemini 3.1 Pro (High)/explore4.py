def final_state(c, d, T):
    state = {0: T}
    active = [0] if T >= 2 else []
    
    steps = 0
    while active:
        steps += 1
        if steps > 500000:
            return None
        
        p = active.pop()
        if state.get(p, 0) < 2:
            continue
            
        num = state[p] // 2
        state[p] %= 2
        
        for p_new in (p - d, p - d - c):
            state[p_new] = state.get(p_new, 0) + num
            if state[p_new] >= 2 and p_new not in active:
                active.append(p_new)
                
    return state

c, d = 1, 5
T = 59
st = final_state(c, d, T)
if st:
    keys = sorted(st.keys())
    print(f"c={c}, d={d}, T={T}")
    s = ""
    for i in range(keys[0], keys[-1] + 1):
        s += str(st.get(i, 0)) + " "
    print(s)

def get_interval(c, d, T):
    st = final_state(c, d, T)
    if st:
        keys = sorted(st.keys())
        return keys[-1] - keys[0] + 1
    return -1

for c in range(1, 4):
    for d in range(1, 4):
        # find max T
        G_val = 1
        while final_state(c, d, G_val) is not None:
            G_val += 1
        G_val -= 1
        st = final_state(c, d, G_val)
        keys = sorted(st.keys())
        s = "".join(str(st.get(i, 0)) for i in range(keys[0], keys[-1] + 1))
        print(f"G({c}, {d}) = {G_val}, length = {keys[-1] - keys[0] + 1}, string: {s}")
