#!/usr/bin/env python3
"""Trace the beaver game to understand the cycle structure."""

def simulate_trace(N, max_steps=500):
    """Simulate with detailed tracing."""
    bananas_on_line = {}
    beaver_pos = 0
    beaver_carry = N
    
    for step in range(max_steps):
        x = beaver_pos
        has_x = bananas_on_line.get(x, 0) > 0
        has_x1 = bananas_on_line.get(x + 1, 0) > 0
        
        # Get state of bananas on line
        active = sorted([k for k, v in bananas_on_line.items() if v > 0])
        
        if step < 100:
            rule = ""
            if has_x and has_x1:
                rule = "A"
            elif has_x and not has_x1:
                rule = "B"
            elif not has_x and has_x1:
                rule = "C"
            else:
                if beaver_carry >= 3:
                    rule = "D"
                else:
                    rule = "END"
            print(f"Step {step}: pos={x}, carry={beaver_carry}, bananas={active}, rule={rule}")
        
        if has_x and has_x1:
            bananas_on_line[x + 1] = 0
            beaver_carry += 1
            beaver_pos = x - 1
        elif has_x and not has_x1:
            bananas_on_line[x] = 0
            beaver_carry += 1
            beaver_pos = x + 2
        elif not has_x and has_x1:
            bananas_on_line[x + 1] = 0
            bananas_on_line[x] = 1
            beaver_pos = x + 2
        else:
            if beaver_carry >= 3:
                bananas_on_line[x - 1] = bananas_on_line.get(x - 1, 0) + 1
                bananas_on_line[x] = bananas_on_line.get(x, 0) + 1
                bananas_on_line[x + 1] = bananas_on_line.get(x + 1, 0) + 1
                beaver_carry -= 3
                beaver_pos = x - 2
            else:
                print(f"GAME ENDS at step {step}: pos={x}, carry={beaver_carry}")
                return x
    
    return None

print("=== Tracing N=10 ===")
simulate_trace(10)
print()

print("=== Tracing N=20 ===")
simulate_trace(20)
