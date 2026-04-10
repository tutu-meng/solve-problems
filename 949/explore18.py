"""
Use the n=6 equiv classes to compute G(6, k) for various k.
Then try to find pattern.
"""
from itertools import combinations_with_replacement, product as iprod
from functools import lru_cache
from collections import Counter
import math

def solve_game(words, n):
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
    initial = tuple((1, n) for _ in range(k))
    return not minimax(initial, 0)

# n=6: 18 equiv classes
# From the output:
n = 6
reps_6 = [
    0,   # [32] L-ending: LLLLLL = 0
    11,  # [8]: LLRRLR = 001101 = 13? Let me compute properly
]

# Actually let me just extract from the output
# LLLLLL=0, LLRRLR=?, etc.
def parse_word(s, n):
    w = 0
    for c in s:
        w = (w << 1) | (1 if c == 'R' else 0)
    return w

class_info = [
    (32, "LLLLLL"),
    (8, "LLRRLR"),
    (5, "LLRLLR"),
    (3, "LRRLRR"),
    (2, "LLLRRR"),
    (2, "LRLLLR"),
    (1, "LLLLLR"),
    (1, "LLLLRR"),
    (1, "LLLRLR"),
    (1, "LLRRRR"),
    (1, "LRLRRR"),
    (1, "LRRRRR"),
    (1, "RLLLLR"),
    (1, "RLLRLR"),
    (1, "RLRLRR"),
    (1, "RLRRRR"),
    (1, "RRLRRR"),
    (1, "RRRRRR"),
]

reps = [parse_word(info[1], n) for info in class_info]
sizes = [info[0] for info in class_info]
num_types = len(class_info)

print(f"n={n}: {num_types} types, total words = {sum(sizes)}")

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
        if count % 5000 == 0:
            print(f"  Progress: {count}...")
    print(f"G({n}, {k}) = {total} (checked {count} multisets)")
