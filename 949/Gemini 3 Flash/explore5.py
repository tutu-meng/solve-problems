"""
Let's try a different approach: for each word, compute a game-theoretic 
"value" that captures how it behaves in the compound game.

Hypothesis: maybe what matters is, for each word, the set of positions 
where the word value changes between consecutive positions (the boundary structure).

Alternative: Let's directly study which word profiles lead to Right wins.
For n=4, k=3, try classifying by the word's "profile" = its actual L/R string.
"""
from itertools import product as iprod
from functools import lru_cache
from collections import defaultdict

def solve_game_bf(words, n):
    k = len(words)
    @lru_cache(maxsize=None)
    def minimax(state, turn):
        intervals = state
        if all(l == r for l, r in intervals):
            ls = sum(1 for i, (l, r) in enumerate(intervals) 
                     if (words[i] >> (n - l)) & 1 == 0)
            return ls > k - ls
        
        if turn == 0:
            ranges = [list(range(l, r + 1)) if l < r else [l] for l, r in intervals]
            for combo in iprod(*ranges):
                if all(combo[i] == intervals[i][0] for i in range(k)):
                    continue
                new_state = tuple((combo[i], intervals[i][1]) for i in range(k))
                if minimax(new_state, 1):
                    return True
            return False
        else:
            ranges = [list(range(l, r + 1)) if l < r else [r] for l, r in intervals]
            for combo in iprod(*ranges):
                if all(combo[i] == intervals[i][1] for i in range(k)):
                    continue
                new_state = tuple((intervals[i][0], combo[i]) for i in range(k))
                if not minimax(new_state, 0):
                    return False
            return True
    
    initial = tuple((1, n) for _ in range(k))
    result = minimax(initial, 0)
    minimax.cache_clear()
    return not result

# n=4: each word is a 4-bit number
# Let's compute, for every PAIR of words, the game outcome (k=1 is trivial)
# For k=1: Left always picks position 2..n, and the single word result is w[position].
# Not meaningful for k=1 since k must be odd.

# Let's see if the game outcome depends on the MULTISET of words, 
# or also their ordering.
n = 4
k = 3
print(f"Checking if game depends on word ordering for n={n}, k={k}...")

from itertools import permutations

# Check a few cases
disagreements = 0
for combo in iprod(range(1 << n), repeat=k):
    base_result = solve_game_bf(combo, n)
    for perm in permutations(combo):
        if perm == combo:
            continue
        perm_result = solve_game_bf(perm, n)
        if perm_result != base_result:
            disagreements += 1
            break

print(f"Disagreements due to ordering: {disagreements}")
print("(0 means outcome depends only on multiset of words)")

# Now classify words into equivalence classes for the compound game.
# Two words w1, w2 are equivalent if swapping them in any game doesn't change outcome.
# Let's check: for n=4, are there words that are always interchangeable?

print(f"\n--- Checking word equivalence classes for n={n} ---")
# For each pair of words, check if they're interchangeable
n_words = 1 << n
equiv = list(range(n_words))  # union-find

def find(x):
    while equiv[x] != x:
        equiv[x] = equiv[equiv[x]]
        x = equiv[x]
    return x

def union(x, y):
    rx, ry = find(x), find(y)
    if rx != ry:
        equiv[rx] = ry

# This is expensive but let's try for n=4
# w1 and w2 are equivalent if for ALL other words w3, 
# the game on {w1, w3, w3} (any k-1 other words) gives same result
# as {w2, w3, w3}
# For k=3: check if replacing w1 with w2 in any pair gives same result

for w1 in range(n_words):
    for w2 in range(w1+1, n_words):
        equivalent = True
        # Check all possible (k-1)-tuples of other words
        for others in iprod(range(n_words), repeat=k-1):
            combo1 = (w1,) + others
            combo2 = (w2,) + others
            if solve_game_bf(combo1, n) != solve_game_bf(combo2, n):
                equivalent = False
                break
        if equivalent:
            union(w1, w2)

# Count equivalence classes
classes = defaultdict(list)
for w in range(n_words):
    classes[find(w)].append(w)

print(f"Number of equivalence classes: {len(classes)}")
for cls_id, members in sorted(classes.items()):
    strs = []
    for w in members:
        s = ''
        for i in range(n):
            s += 'R' if (w >> (n-1-i)) & 1 else 'L'
        strs.append(s)
    print(f"  Class {cls_id}: {strs}")
