"""
Data so far:
G(2, 3) = 14
G(2, 5) = 182
G(4, 3) = 496
G(6, 3) = 20490

Let me look for formulas.

For n=2 with k=3 words, there are 3 types: 
  Type A (LL, RL): 2 words -> always gives L (count = 2) 
  Type B (LR): 1 word -> Left trim=R, Right trim=L
  Type C (RR): 1 word -> always gives R (count = 1)

Total words: 4 (= 2^2)

From the game analysis, Right wins in these multisets:
  (A, C, C): 1*C(3,1) = 3 orderings per base combo, but a=1,c=2 -> 3!/1!2! = 3
  (B, B, B): 1 ordering
  (B, B, C): 3
  (B, C, C): 3  
  (A₂, C, C) wait... RL is type A, so (RL, RR, RR) has 3 orderings

Actually from enumeration:
  14 = 3 + 1 + 3 + 3 + 3 + 1 = 14

For n=2, k=3 = 14. For k=5 = 182.
2^(2*3) = 64. 2^(2*5) = 1024. 

14/64 = 7/32. 182/1024 = 91/512.
7 = C(4,2) + 1 = 7. 91 = C(7+6+...?) Hmm.

Let me think in terms of types. n=2 has 3 equiv classes, sizes [2, 1, 1].
Call them type 0 (size 2, always L), type 1 (size 1, anti), type 2 (size 1, always R).

For G(2, k), the answer depends on how many words of each type give Right a win.
And the number of ordered k-tuples is:
  sum over (a,b,c) with a+b+c=k, right_wins(a,b,c) * k!/(a!b!c!) * 2^a * 1^b * 1^c

Let me compute right_wins(a,b,c) for all (a,b,c) with a+b+c=3:
"""

from itertools import product as iprod
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

# For n=2, the word representatives of each equiv class are:
# Class A (always L): LL=0, RL=2 -> representative 0 (LL)
# Class B (anti): LR=1 -> representative 1 (LR)
# Class C (always R): RR=3 -> representative 3 (RR)
# Class sizes: A=2, B=1, C=1

n = 2
reps = [0, 1, 3]  # LL, LR, RR
rep_sizes = [2, 1, 1]

# Test ALL multisets of types for k=3 and k=5
for k in [3, 5, 7]:
    total = 0
    for combo_types in iprod(range(3), repeat=k):
        # Map to multiset
        combo_sorted = tuple(sorted(combo_types))
        if combo_sorted != combo_types:
            continue  # Only process sorted
        
        # Map type indices to word representatives
        words = tuple(reps[t] for t in combo_sorted)
        rw = solve_game(words, n)
        
        if rw:
            cnt = Counter(combo_sorted)
            orderings = math.factorial(k)
            for c in cnt.values():
                orderings //= math.factorial(c)
            # Multiply by product of class sizes
            size_factor = 1
            for t in combo_sorted:
                size_factor *= rep_sizes[t]
            total += orderings * size_factor
    
    print(f"G({n}, {k}) = {total}")

print()
# For n=4: 8 equiv classes
# Class sizes (from earlier): 
# [8]: all ending in L -> representative LLLL=0
# [2]: LRLR, RRLR -> rep LRLR=5
# [1]: LLLR=1, LLRR=3, LRRR=7, RLLR=9, RLRR=11, RRRR=15

n = 4
reps_4 = [0, 5, 1, 3, 7, 9, 11, 15]
sizes_4 = [8, 2, 1, 1, 1, 1, 1, 1]
num_types = len(reps_4)

for k in [3]:
    total = 0
    count = 0
    from itertools import combinations_with_replacement as cwr
    for combo_types in cwr(range(num_types), k):
        words = tuple(reps_4[t] for t in combo_types)
        rw = solve_game(words, n)
        if rw:
            cnt = Counter(combo_types)
            orderings = math.factorial(k)
            for c in cnt.values():
                orderings //= math.factorial(c)
            size_factor = 1
            for t in combo_types:
                size_factor *= sizes_4[t]
            total += orderings * size_factor
        count += 1
    print(f"G({n}, {k}) = {total} (checked {count} multisets)")
