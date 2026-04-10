"""
Find game equivalence classes for n=6 by directly testing word distinguishability.
Since brute force over all (k-1)-tuples is O(64^2 * 64^2) = too slow for k=3,
let me sample random (k-1)-tuples to build fingerprints.

Actually for n=6, k=3: each game is on 3 words of length 6.
There are 64 words. Testing all 64^2 = 4096 pairs as the "other 2 words" 
for each of 64 words = 64 * 4096 = 262144 games. Each game has 
state space of about (21)^3 = 9261 * 2 ≈ 18000. Should be barely doable.
"""
from itertools import product as iprod
from functools import lru_cache
from collections import defaultdict
import time

def make_solver(n, words):
    k = len(words)
    memo = {}
    
    def minimax(state, turn):
        key = (state, turn)
        if key in memo:
            return memo[key]
        
        if all(l == r for l, r in state):
            ls = sum(1 for i, (l, r) in enumerate(state)
                     if (words[i] >> (n - l)) & 1 == 0)
            result = ls > k - ls
            memo[key] = result
            return result
        
        if turn == 0:
            for combo in iprod(*(range(l, r + 1) if l < r else [l] for l, r in state)):
                if all(combo[i] == state[i][0] for i in range(k)):
                    continue
                new_state = tuple((combo[i], state[i][1]) for i in range(k))
                if minimax(new_state, 1):
                    memo[key] = True
                    return True
            memo[key] = False
            return False
        else:
            for combo in iprod(*(range(l, r + 1) if l < r else [r] for l, r in state)):
                if all(combo[i] == state[i][1] for i in range(k)):
                    continue
                new_state = tuple((state[i][0], combo[i]) for i in range(k))
                if not minimax(new_state, 0):
                    memo[key] = False
                    return False
            memo[key] = True
            return True
    
    return minimax

def solve_game(words, n):
    k = len(words)
    mm = make_solver(n, words)
    initial = tuple((1, n) for _ in range(k))
    return not mm(initial, 0)  # True = Right wins

def word_str(w, n):
    return ''.join('R' if (w >> (n-1-i)) & 1 else 'L' for i in range(n))

# Build fingerprints for n=6 with k=3
n = 6
k = 3
n_words = 1 << n

print(f"Building fingerprints for n={n}, k={k}...")
start = time.time()

# For each word w, compute fingerprint = {(w2, w3) -> outcome}
# But we use SORTED multisets since ordering doesn't matter
fingerprints = {}
game_cache = {}

for w in range(n_words):
    fp = []
    for w2 in range(n_words):
        for w3 in range(w2, n_words):
            combo = tuple(sorted([w, w2, w3]))
            if combo not in game_cache:
                game_cache[combo] = solve_game(combo, n)
            fp.append(game_cache[combo])
    fingerprints[w] = tuple(fp)
    if w % 10 == 0:
        print(f"  w={w}/{n_words}, time={time.time()-start:.1f}s")

classes = defaultdict(list)
for w, fp in fingerprints.items():
    classes[fp].append(w)

print(f"\nTime: {time.time()-start:.1f}s")
print(f"Number of equiv classes: {len(classes)}")
for fp, members in sorted(classes.items(), key=lambda x: -len(x[1])):
    strs = [word_str(w, n) for w in members[:8]]
    extra = f"...+{len(members)-8}" if len(members) > 8 else ""
    last_chars = set(s[-1] for s in strs)
    print(f"  [{len(members)}] last={last_chars}: {', '.join(strs)} {extra}")
