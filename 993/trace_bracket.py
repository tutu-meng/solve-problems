def trace_k(k):
    bananas = {i: 1 for i in range(k)}
    x = 0
    carry = 100
    
    while True:
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
            
    m = min(list(bananas.keys()))
    M = max(max(list(bananas.keys())), x)
    res = ""
    for i in range(-1, M+1):
        if i == x:
            res += "[" + str(bananas.get(i,0)) + "]"
        else:
            res += " " + str(bananas.get(i,0)) + " "
    return x, carry-100, res

for k in range(1, 10):
    x, c, s = trace_k(k)
    print(f"k={k}: x={x}, dC={c}, state={s}")
