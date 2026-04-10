"""
For n=4, determine the game outcome formula.
8 types: 
  0: [8 words, all L-ending] = "always L" type (like type A)
  7: [1 word: RRRR] = "always R" type (like type C)
  Others: various contested types

For each pair of types, I need to understand the game interaction.
Let me compute the full game outcome table for all multisets.
"""
from itertools import product as iprod, combinations_with_replacement
from functools import lru_cache
from collections import Counter
import math

def solve_game(words, n):
    k = len(words)
    @lru_cache(maxsize=None)
    def mm(state, turn):
        if all(l == r for l, r in state):
            ls = sum(1 for i,(l,r) in enumerate(state) if (words[i]>>(n-l))&1==0)
            return ls > k - ls
        if turn == 0:
            for combo in iprod(*(range(l,r+1) if l<r else [l] for l,r in state)):
                if all(combo[i]==state[i][0] for i in range(k)): continue
                ns = tuple((combo[i],state[i][1]) for i in range(k))
                if mm(ns, 1): return True
            return False
        else:
            for combo in iprod(*(range(l,r+1) if l<r else [r] for l,r in state)):
                if all(combo[i]==state[i][1] for i in range(k)): continue
                ns = tuple((state[i][0],combo[i]) for i in range(k))
                if not mm(ns, 0): return False
            return True
    init = tuple((1,n) for _ in range(k))
    r = mm(init, 0)
    mm.cache_clear()
    return not r

# n=4 types
n = 4
reps = [0, 5, 1, 3, 7, 9, 11, 15]
rep_names = ['LLLL(A)', 'LRLR', 'LLLR', 'LLRR', 'LRRR', 'RLLR', 'RLRR', 'RRRR(C)']
sizes = [8, 2, 1, 1, 1, 1, 1, 1]

# For k=3, compute game outcome for all multisets of 3 types
k = 3
outcomes = {}  # type_multiset -> Right wins?
for combo in combinations_with_replacement(range(8), k):
    words = tuple(reps[t] for t in combo)
    rw = solve_game(words, n)
    outcomes[combo] = rw

# Print game outcome table
print(f"n={n}, k={k}: Game outcomes by type multiset")
print(f"{'Multiset':30s} {'Winner':8s}")
for combo, rw in sorted(outcomes.items()):
    names = ', '.join(rep_names[t] for t in combo)
    cnt = Counter(combo)
    type_str = ','.join(f"t{t}={c}" for t,c in sorted(cnt.items()))
    print(f"  ({type_str:20s}): {'RIGHT' if rw else 'Left':5s}  [{names}]")

# Now let me see if there's a pattern.
# For n=2: the key was that types decompose into A(always L), B(poison), C(always R)
# and the formula depends on counts of each.

# For n=4: let me check if there's a similar decomposition.
# Type 0 = always L (L-ending). Type 7 = always R (RRRR).
# What about the middle types?

# Let me check: for k=1, what is each type's outcome?
print("\n\nSingle-word outcomes (k=1):")
for t in range(8):
    words = (reps[t],)
    rw = solve_game(words, n)
    print(f"  Type {t} ({rep_names[t]}): {'RIGHT' if rw else 'Left'} wins")
