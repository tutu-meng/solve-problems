#!/usr/bin/env python3
"""Deeper analysis of the beaver game."""

def simulate(N):
    """Simulate the beaver game with N bananas. Return final position."""
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
                return beaver_pos
        
        steps += 1
        if steps > 5 * 10**7:
            return None

# Let me look at the values more carefully
# Compute for a wider range
print("Looking at larger N values:")
for n in [500, 1000, 1500, 2000, 2500, 3000]:
    bb = simulate(n)
    if bb is not None:
        print(f"BB({n}) = {bb}, ratio = {bb/n:.6f}")

print()

# Let's look at the relationship more carefully
# BB(1000) = 1499 = 1.499 * 1000
# Let's check BB(N)/N for large N
print("\nChecking BB(N) for N = 100k for various k:")
for k in range(1, 21):
    n = 100 * k
    bb = simulate(n)
    if bb is not None:
        print(f"BB({n}) = {bb}, N*3/2 = {3*n//2}, diff from 3N/2 = {bb - 3*n//2}, BB(N) mod 2 = {bb % 2}, N mod 2 = {n % 2}")

# Check if BB(1000) = 1499 = 3*1000/2 - 1 = 1500 - 1
print(f"\n3*1000/2 - 1 = {3*1000//2 - 1}")
print(f"BB(1000) = 1499")
print(f"Match: {3*1000//2 - 1 == 1499}")

# So maybe BB(N) ≈ 3N/2 for large even N?
# Let's check more carefully
print("\nFor even N:")
for n in range(100, 2001, 2):
    bb = simulate(n)
    if bb is not None:
        diff = bb - 3*n//2
        if n % 100 == 0:
            print(f"BB({n}) = {bb}, 3N/2 = {3*n//2}, diff = {diff}")
