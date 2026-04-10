# Problem 949: Left vs Right II
# 
# Implementation Plan
#
# This is a 100% difficulty Project Euler problem. Key observations so far:
#
# 1. Game outcome depends on multiset of words (not ordering) - VERIFIED
# 2. For n=2: 3 equiv classes, sizes [2, 1, 1]
# 3. For n=4: 8 equiv classes, sizes [8, 2, 1, 1, 1, 1, 1, 1]  
# 4. The number of equiv classes grows with n - need a pattern
# 5. Position 1 matters for some words (LLLR ≠ RLLR in game)
# 6. All L-ending words are equivalent regardless of n
#
# Data:
# G(2,3)=14   G(2,5)=182   G(2,7)=2550
# G(4,3)=496
# G(6,3)=20490
# G(8,5)=26359197010  (given)
#
# Strategy: Need to find equivalence classes for n=20, compute game outcome
# for each multiset of classes, and count.
#
# The key question is: what determines whether two words are game-equivalent?
# For the compound game of k words, the game value of a single word depends 
# on ALL its sub-interval game values.
#
# Alternative approach: Can we find a closed-form formula relating G(n,k) 
# to simpler quantities? The sequence G(2,k) for k=3,5,7 might reveal something.

# G(2,3) = 14, G(2,5) = 182, G(2,7) = 2550
# 14 * 13 = 182. ✓
# 182 * 14.01... = 2550. Hmm: 2550/182 = 14.01...

# Actually: 14 = 2*(4^3 - 3^3)/4 = 2*(64-27)/4 = 18.5. No.
# Let me check: 4^3 = 64. 14/64 = 7/32.
# 4^5 = 1024. 182/1024 = 91/512.
# 4^7 = 16384. 2550/16384 = 1275/8192.

# 7 = 7, 91 = 7*13, 1275 = 7*13*? 1275/91 = 14.01... not exact!
# Actually 1275/7 = 182.14... Hmm.

# Let me verify: Does 2550 = sum over right-winning multisets of 
# (ord_count * size_factor)?
# With 3 types of sizes [2, 1, 1], for k=7.

# Let me just double-check G(2,7) numerically.
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

# For n=2, k=3,5,7: type reps = [0(LL), 1(LR), 3(RR)], sizes = [2, 1, 1]
n = 2
reps = [0, 1, 3]
sizes = [2, 1, 1]

for k in [3, 5, 7, 9]:
    total = 0
    for combo_types in combinations_with_replacement(range(3), k):
        words = tuple(reps[t] for t in combo_types)
        rw = solve_game(words, n)
        if rw:
            cnt = Counter(combo_types)
            orderings = math.factorial(k)
            for c in cnt.values():
                orderings //= math.factorial(c)
            size_factor = 1
            for t in combo_types:
                size_factor *= sizes[t]
            total += orderings * size_factor
    print(f"G({n}, {k}) = {total}")

# Also enumerate which (a,b,c) multisets win for Right
print("\nDetailed for G(2,7):")
for combo_types in combinations_with_replacement(range(3), 7):
    words = tuple(reps[t] for t in combo_types)
    rw = solve_game(words, n)
    if rw:
        cnt = Counter(combo_types)
        a, b, c = cnt.get(0, 0), cnt.get(1, 0), cnt.get(2, 0)
        orderings = math.factorial(7) // (math.factorial(a) * math.factorial(b) * math.factorial(c))
        sf = (2**a) * (1**b) * (1**c)
        print(f"  a={a}, b={b}, c={c}: orderings={orderings}, size_factor={sf}, contrib={orderings*sf}")
