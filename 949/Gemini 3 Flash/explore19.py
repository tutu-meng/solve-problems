"""
Let me try a fundamentally different approach. Instead of solving the minimax
game directly, let me look for a PATTERN in G(n, k).

Known values:
  G(2,3) = 14
  G(2,5) = 182
  G(2,7) = 2550
  G(2,9) = 36014
  G(4,3) = 496
  G(4,5) = 79274
  G(6,3) = 20490
  G(8,5) = 26359197010 (given)
  
Let me check: 
  2^(n*k) = total ordered tuples
  G/total = fraction Right wins

  G(2,3)/4^3 = 14/64 = 7/32
  G(2,5)/4^5 = 182/1024 = 91/512
  G(2,7)/4^7 = 2550/16384 = 1275/8192
  
  7, 91, 1275
  91/7 = 13
  1275/91 = 14.01... Not exact.
  
  Let me look at G(n,k) / 2^nk more carefully.
  
  G(4,3)/16^3 = 496/4096 = 31/256
  G(6,3)/64^3 = 20490/262144
  
  31/256 and 20490/262144...
  20490/262144 = 10245/131072
  
  Let me try: G(n, k) = sum over some formula involving n, k.
  
  Or maybe relate G(n, k) to choosing among specific types.
  
  For n=2, k-words, the game has 3 types with counts [2, 1, 1].
  Let me denote a = count of type-A words (size 2, always L),
  b = count of type-B (size 1, anti/LR), c = count of type-C (size 1, always R).
  
  Right wins iff the game outcome has majority R.
  
  Let me compute the game outcome for each (a,b,c):
"""

from itertools import product as iprod, combinations_with_replacement
from functools import lru_cache
from collections import Counter
import math

def solve_game(words, n):
    k = len(words)
    @lru_cache(maxsize=None)
    def minimax(state, turn):
        if all(l == r for l, r in state):
            ls = sum(1 for i, (l, r) in enumerate(state)
                     if (words[i] >> (n - l)) & 1 == 0)
            return ls > k - ls
        if turn == 0:
            ranges = [range(l, r + 1) if l < r else [l] for l, r in state]
            for combo in iprod(*ranges):
                if all(combo[i] == state[i][0] for i in range(k)):
                    continue
                new_state = tuple((combo[i], state[i][1]) for i in range(k))
                if minimax(new_state, 1):
                    return True
            return False
        else:
            ranges = [range(l, r + 1) if l < r else [r] for l, r in state]
            for combo in iprod(*ranges):
                if all(combo[i] == state[i][1] for i in range(k)):
                    continue
                new_state = tuple((state[i][0], combo[i]) for i in range(k))
                if not minimax(new_state, 0):
                    return False
            return True
    initial = tuple((1, n) for _ in range(k))
    result = minimax(initial, 0)
    minimax.cache_clear()
    return not result

# For n=2: determine game outcome for each (a,b,c) multiset
# Types: 0=LL(always L), 1=LR(poison), 2=RR(always R)
reps = [0, 1, 3]

print("n=2 game outcomes by type distribution:")
print("(a, b, c) -> Right wins?")
for k in range(1, 12, 2):
    print(f"\n  k={k}:")
    for combo in combinations_with_replacement(range(3), k):
        cnt = Counter(combo)
        a, b, c = cnt.get(0,0), cnt.get(1,0), cnt.get(2,0)
        words = tuple(reps[t] for t in combo)
        rw = solve_game(words, 2)
        if rw:
            print(f"    ({a},{b},{c}): RIGHT wins")

# Try to find the pattern: when does Right win?
print("\n\nPattern analysis for n=2:")
print("Right wins when:")
for k in range(1, 16, 2):
    rw_list = []
    for combo in combinations_with_replacement(range(3), k):
        cnt = Counter(combo)
        a, b, c = cnt.get(0,0), cnt.get(1,0), cnt.get(2,0)
        words = tuple(reps[t] for t in combo)
        rw = solve_game(words, 2)
        if rw:
            rw_list.append((a, b, c))
    
    # Check pattern: Right wins iff c + ceil(b/2) > k/2?
    # or c + floor(b/2) >= (k+1)/2?
    threshold = (k + 1) // 2
    
    for a, b, c in rw_list:
        # Various formulas
        f1 = c + (b + 1) // 2  # c + ceil(b/2)
        f2 = c + b // 2  # c + floor(b/2)
        f3 = c + b  # total R-favorable
        # Check which formula works
        pass
    
    # Print compact
    print(f"  k={k}: {rw_list}")
