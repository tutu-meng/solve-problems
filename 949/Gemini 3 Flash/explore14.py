"""
Plan: The game outcome depends on the multiset of words. 
The suffix-type (positions 2..n) determines the game behavior.
Position 1 doesn't matter (Left can always trim it on first move).

So each word is characterized by its suffix w[2..n], a string of length n-1.
Two words with the same suffix are game-equivalent.
Each suffix has exactly 2 words (L__ and R__).

So we have 2^(n-1) types, each of multiplicity 2.

For k=7 words of n=20, we have 2^19 = 524288 types.
The number of multisets of 7 from 524288 types is ~10^38. Still too many.

But wait - in the game on k words, does the FULL suffix matter, or just 
some coarser property?

For n=4 with k=3, the game equivalence classes were:
  [8]: all L-ending words (4 suffix types merged into 1 game class)
  [2]: LRLR, RRLR (1 suffix type)
  [1] x 6: other R-ending words (6 distinct game classes from 3 suffix types)

Wait, the 4 L-ending suffix types (..LL, ..RL) merged into 1. And among 
R-ending, LRLR and RRLR merged (same suffix LR but different full game behavior..?
No, they have the same suffix: LRLR -> suffix RLR, RRLR -> suffix RLR. Same suffix!

Oh wait, I was wrong. LRLR has suffix RLR and RRLR has suffix RLR. They ARE 
the same suffix! So they should be in the same suffix class already.

But earlier the suffix-type classification gave 8 classes for n=4, each of size 2.
LRLR = 0101, suffix = 101 = RLR. RRLR = 1101, suffix = 101 = RLR. 
They have the SAME suffix. So they're in the same suffix class.

But the suffix-type classification I computed gave them in the same class 
{LRLR, RRLR}. This IS the suffix class!

So game equivalence for n=4:
  L-ending suffixes: all merged into 1 game class (4 suffix types -> 1)
  R-ending suffixes: 
    suffix LLR -> LLLR, RLLR (game class of size 2)
    suffix LRR -> LLRR, RLRR (game class of size 2)
    suffix RLR -> LRLR, RRLR (game class of size 2)
    suffix RRR -> LRRR, RRRR (game class of size 2)

Wait, but earlier the game equivalence had LLLR alone and RLLR alone (different 
game classes). Let me recheck...

From my n=4 equivalence class computation:
  [8]: LLLL, LLRL, LRLL, LRRL, RLLL, RLRL, RRLL, RRRL  (all 8 L-ending words)
  [2]: LRLR, RRLR  (suffix RLR)
  [1]: LLLR  (suffix LLR, but partner RLLR is SEPARATE)
  [1]: LLRR  (suffix LRR, but partner RLRR is SEPARATE)
  [1]: LRRR  (suffix RRR, but partner RRRR is SEPARATE)
  [1]: RLLR
  [1]: RLRR
  [1]: RRRR

So within suffix class LLR, LLLR and RLLR are NOT equivalent!
Only in suffix class RLR are LRLR and RRLR equivalent.

This means position 1 DOES matter for some word types, even though 
both players can reach any position 2..n!

This is puzzling. Let me re-verify that LLLR and RLLR are truly 
NOT game-equivalent for k=3.
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

# Check: is there a pair (w2, w3) where replacing LLLR<->RLLR changes outcome?
n = 4
LLLR = 1  # 0001
RLLR = 9  # 1001

diffs = []
for w2 in range(16):
    for w3 in range(w2, 16):
        combo1 = tuple(sorted([LLLR, w2, w3]))
        combo2 = tuple(sorted([RLLR, w2, w3]))
        r1 = solve_game(combo1, n)
        r2 = solve_game(combo2, n)
        if r1 != r2:
            from itertools import product
            def ws(w):
                return ''.join('R' if (w>>(n-1-i))&1 else 'L' for i in range(n))
            diffs.append((ws(w2), ws(w3), r1, r2))

print(f"Cases where LLLR and RLLR differ:")
for w2s, w3s, r1, r2 in diffs[:10]:
    print(f"  w2={w2s}, w3={w3s}: LLLR->{r1}, RLLR->{r2}")
print(f"Total differing cases: {len(diffs)}")

# Also check LRLR vs RRLR for completeness
LRLR = 5  # 0101
RRLR = 13 # 1101
diffs2 = []
for w2 in range(16):
    for w3 in range(w2, 16):
        combo1 = tuple(sorted([LRLR, w2, w3]))
        combo2 = tuple(sorted([RRLR, w2, w3]))
        r1 = solve_game(combo1, n)
        r2 = solve_game(combo2, n)
        if r1 != r2:
            diffs2.append(True)

print(f"\nLRLR vs RRLR: {len(diffs2)} differing cases (should be 0)")
