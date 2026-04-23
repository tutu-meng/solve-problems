def final_state(N):
    bananas = {}
    x = 0
    carry = N
    
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
            if carry >= 3:
                bananas[x-1] = bananas.get(x-1, 0) + 1
                bananas[x] = bananas.get(x, 0) + 1
                bananas[x+1] = bananas.get(x+1, 0) + 1
                carry -= 3
                x = x - 2
            else:
                break
                
    m = min(list(bananas.keys())) if bananas else 0
    M = max(list(bananas.keys())) if bananas else 0
    res = "".join(str(bananas.get(i,0)) for i in range(m, M+1))
    return x, m, res

for N in range(3, 20):
    x, m, s = final_state(N)
    print(f"N={N:2d}: BB={x:2d}, min={m}, state={s}")
