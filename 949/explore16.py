"""
Compute G(4,5) using equivalence classes.
For n=4, we have 8 game equivalence classes:
  Class 0: [8 words] LLLL, LLRL, LRLL, LRRL, RLLL, RLRL, RRLL, RRRL (all L-ending)
  Class 1: [2 words] LRLR, RRLR  
  Class 2: [1 word] LLLR
  Class 3: [1 word] LLRR
  Class 4: [1 word] LRRR
  Class 5: [1 word] RLLR
  Class 6: [1 word] RLRR
  Class 7: [1 word] RRRR

Total: 8+2+1+1+1+1+1+1 = 16 = 2^4 ✓

For k=5, we need to enumerate multisets of 5 classes from 8 types.
C(8+4, 5) = C(12, 5) = 792 multisets. Very manageable!
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

n = 4
# Representatives and sizes for each class
reps =  [0, 5, 1, 3, 7, 9, 11, 15]
sizes = [8, 2, 1, 1, 1, 1, 1, 1]
num_types = 8

for k in [3, 5]:
    total = 0
    count = 0
    for combo_types in combinations_with_replacement(range(num_types), k):
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
        count += 1
    print(f"G({n}, {k}) = {total} (checked {count} multisets)")
