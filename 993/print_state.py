def run(N):
    bananas = {}
    x = 0
    carry = N
    
    def print_state(step):
        min_p = min(list(bananas.keys()) + [x]) if bananas else x
        max_p = max(list(bananas.keys()) + [x]) if bananas else x
        s = ""
        for p in range(min_p, max_p + 1):
            if p == x:
                s += "[" + str(bananas.get(p, 0)) + "]"
            else:
                s += " " + str(bananas.get(p, 0)) + " "
        print(f"Step {step}: pos={x}, carry={carry}, state={s}")
        
    for step in range(30):
        print_state(step)
        has_x = bananas.get(x, 0) > 0
        has_x1 = bananas.get(x+1, 0) > 0
        
        if has_x and has_x1:
            bananas[x+1] -= 1  # Wait, wait, Case 1 says "pick up at x+1"
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
                print(f"Ends at step {step}")
                print_state(step)
                return x

run(20)
