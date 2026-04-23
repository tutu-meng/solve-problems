def run(N):
    bananas = {}
    x = 0
    carry = N
    steps = 0
    max_b = 0
    
    while True:
        steps += 1
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
                return x, max_b, carry, bananas

        # check max bananas
        for pos, count in bananas.items():
            if count > max_b:
                max_b = count
        
        if steps > 500000:
            return None, max_b, carry, bananas

for i in range(100):
    res = run(i)
    if res and res[1] > 1:
        print(f"N={i} has max bananas={res[1]}")
        break

print(f"BB(1000) = {run(1000)[0]}, max bananas = {run(1000)[1]}")
