"""
This is a 100% difficulty problem. Let me try to find the pattern computationally.

G(2,3)=14, G(4,3)=496, G(6,3)=20490.

Let me also try to compute G(2,5), G(4,5), G(2,7) to see if patterns emerge.
And also try G(8,3).

Then search for the pattern in these values.
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

def G_compute(n, k):
    n_words = 1 << n
    total = 0
    for combo in combinations_with_replacement(range(n_words), k):
        rw = solve_game(combo, n)
        if rw:
            cnt = Counter(combo)
            orderings = math.factorial(k)
            for c in cnt.values():
                orderings //= math.factorial(c)
            total += orderings
    return total

# Compute various G values
for n in [2, 4]:
    for k in [3, 5]:
        print(f"G({n}, {k}) = {G_compute(n, k)}")
