def test_block(k):
    print(f"--- k = {k} ---")
    bananas = {i: 1 for i in range(k)}
    x = 0
    carry = 100
    
    def state_str():
        if not bananas: return ""
        m, M = min(list(bananas.keys()) + [x]), max(list(bananas.keys()) + [x])
        return " ".join([f"{i}:" + ("["+str(bananas.get(i,0))+"]" if i==x else " "+str(bananas.get(i,0))+" ") for i in range(m, M+1)])

    print(f"Init: {state_str()}")
    for step in range(15):
        has_x = bananas.get(x, 0) > 0
        has_x1 = bananas.get(x+1, 0) > 0
        
        if has_x and has_x1:
            bananas[x+1] -= 1
            carry += 1
            x = x - 1
        elif has_x and not has_x1:
            bananas[x] -= 1
            carry += 1
            x = x + 2
        elif not has_x and has_x1:
            bananas[x+1] -= 1
            bananas[x] = bananas.get(x, 0) + 1
            x = x + 2
        else:
            break
        print(f"S{step+1}: {state_str()}  (C:{carry-100})")

for i in range(2, 7):
    test_block(i)
