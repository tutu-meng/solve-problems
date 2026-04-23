def test_k_ones(k, initial_carry):
    bananas = {i: 1 for i in range(k)}
    x = 0
    carry = initial_carry
    step = 0
    
    while carry > 0 or (bananas.get(x, 0) == 0 and bananas.get(x+1, 0) == 0):
        # We stop when beaver escapes the block or drops
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
                break
            else:
                break
        step += 1
        
        # print state if small enough
        if step > 1000: break
        
    return step, x, carry, bananas

# Let's run for a few k
for k in range(2, 6):
    print(f"k={k}")
    step, x, carry, ban = test_k_ones(k, 10)
    print(f" After {step} steps: x={x}, carry_change={carry-10}, bananas={dict(sorted(ban.items()))}")
