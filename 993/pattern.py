#!/usr/bin/env python3
"""Look at BB(N) for many consecutive values to find repeating patterns."""

def simulate(N):
    """Simulate the beaver game with N bananas. Return final position and carry."""
    bananas_on_line = {}
    beaver_pos = 0
    beaver_carry = N
    steps = 0
    
    while True:
        x = beaver_pos
        has_x = bananas_on_line.get(x, 0) > 0
        has_x1 = bananas_on_line.get(x + 1, 0) > 0
        
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
                return beaver_pos, beaver_carry, steps
        
        steps += 1
        if steps > 10**7:
            return None, None, None

# Compute BB(N) and BB(N) - BB(N-1) to find patterns
print("N, BB(N), carry, steps, BB(N)-BB(N-1)")
prev_bb = None
results = []
for n in range(0, 5001):
    bb, carry, steps = simulate(n)
    if bb is not None:
        diff = bb - prev_bb if prev_bb is not None else "N/A"
        results.append((n, bb, carry, steps, diff))
        if n <= 50 or n % 100 == 0:
            print(f"{n}, {bb}, {carry}, {steps}, {diff}")
        prev_bb = bb
    else:
        print(f"{n}: timeout!")
        break

# Look at second differences  
print("\n\n=== Looking at BB(N+1) - BB(N) differences ===")
diffs = []
for i in range(1, len(results)):
    d = results[i][1] - results[i-1][1]
    diffs.append((results[i][0], d))

# Look for periodicity in diffs
print("Checking periodicity of BB(N+1)-BB(N):")
for period in range(1, 200):
    matches = True
    count = 0
    for i in range(len(diffs) - period):
        if i >= 200:  # Start checking from offset 200
            if diffs[i][1] != diffs[i + period][1]:
                matches = False
                break
            count += 1
    if matches and count > 100:
        print(f"Period {period} works! (checked {count} pairs)")

# Also check if BB has periodicity with offset
print("\n\nChecking if BB(N+P) - BB(N) is constant for various P:")
for period in range(1, 200):
    vals = set()
    for i in range(500, min(1000, len(results) - period)):
        d = results[i + period][1] - results[i][1]
        vals.add(d)
    if len(vals) == 1:
        print(f"BB(N+{period}) - BB(N) = {vals.pop()} for N >= 500")
