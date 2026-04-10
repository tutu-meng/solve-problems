"""
Faster equivalence class finder using game outcome table.
Instead of checking all pairs, build a fingerprint for each word.
The fingerprint = outcomes when paired with all possible (k-1)-tuples.
"""
from itertools import product as iprod
from functools import lru_cache
from collections import defaultdict
import sys

def make_solver(n):
    """Create a memoized solver for given n."""
    @lru_cache(maxsize=None)
    def minimax(words, state, turn, k):
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
                if minimax(words, new_state, 1, k):
                    return True
            return False
        else:
            ranges = [list(range(l, r + 1)) if l < r else [r] for l, r in intervals]
            for combo in iprod(*ranges):
                if all(combo[i] == intervals[i][1] for i in range(k)):
                    continue
                new_state = tuple((intervals[i][0], combo[i]) for i in range(k))
                if not minimax(words, new_state, 0, k):
                    return False
            return True
    return minimax

def solve_bf(words, n, solver):
    k = len(words)
    initial = tuple((1, n) for _ in range(k))
    return not solver(words, initial, 0, k)  # True = Right wins

def word_str(w, n):
    s = ''
    for i in range(n):
        s += 'R' if (w >> (n-1-i)) & 1 else 'L'
    return s

# For each word, compute fingerprint: for all possible pairs (k=3),
# map (w2, w3) -> outcome when playing (w, w2, w3)
n = 4
k = 3
n_words = 1 << n
solver = make_solver(n)

print(f"Computing fingerprints for n={n}, k={k}...")
fingerprints = {}
for w in range(n_words):
    fp = []
    for others in iprod(range(n_words), repeat=k-1):
        combo = (w,) + others 
        # Use sorted multiset since ordering doesn't matter
        combo_sorted = tuple(sorted(combo))
        result = solve_bf(combo_sorted, n, solver)
        fp.append(result)
    fingerprints[w] = tuple(fp)

# Group by fingerprint
classes = defaultdict(list)
for w, fp in fingerprints.items():
    classes[fp].append(w)

print(f"Number of equiv classes: {len(classes)}")
for fp, members in sorted(classes.items(), key=lambda x: -len(x[1])):
    strs = [word_str(w, n) for w in members]
    # Check what the members have in common
    print(f"  [{len(members)}]: {', '.join(strs)}")

# Now let me look at the pattern for class membership.
# For each class, print the binary representation and check 
# if there's a simple characterization.
print()
print("Analyzing word structure within classes:")
for fp, members in sorted(classes.items(), key=lambda x: -len(x[1])):
    strs = [word_str(w, n) for w in members]
    # Look at last few characters
    last_chars = set(s[-1] for s in strs)
    last2 = set(s[-2:] for s in strs)
    print(f"  [{len(members)}]: last_char={last_chars}, last2={last2}, words={strs}")
