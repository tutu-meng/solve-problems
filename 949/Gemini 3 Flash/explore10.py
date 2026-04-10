"""
Key observation: the game on k words of length n has a recursive structure.

On Left's first move, Left can trim 0 to n-1 letters from the left of each word.
This transforms each word from length n to a shorter word. 
Similarly Right trims from the right.

Let me think about this differently: what if I represent each word not by 
its full string, but by a "game value" computed recursively?

Actually, let me try the most direct approach: compute G(n,k) using a 
game solver that works with word TYPE counts rather than individual words.

For this, I need to:
1. Classify words by type (game equivalence class)
2. For each multiset of types, determine game outcome
3. Count ordered tuples by type distribution

Step 1: I need to figure out the right notion of "type".

Let me try a recursive approach. For a word of length n, define its 
"game class" inductively:
- For length 1: class is L or R
- For length n > 1: class is determined by the classes of all suffixes 
  (positions 2..n, 3..n, ..., n) and all prefixes (1..n-1, 1..n-2, ..., 1)

Actually, since in the compound game the players trim SIMULTANEOUSLY 
across all words, and Left trims from the left (advancing to a suffix)
while Right trims from the right (retreating to a prefix), the game 
structure is about the "suffix game values" and "prefix game values".

Let me try yet another approach: just compute G(n, k) directly but 
smartly for larger n.

For the direct computation, the key bottleneck is the game solver for 
k words. If I can solve the game efficiently (polynomial in k given the 
word types), then I just need to combine with counting.

Let me try to find G(n, k) for n=2,4,6,8 with k=3 and k=5.
I'll use memoization over sorted word tuples.
"""
from itertools import product as iprod, combinations_with_replacement
from functools import lru_cache
from collections import Counter
import math

def solve_game(words, n):
    """Determine if Right wins. Words is a sorted tuple of word integers."""
    k = len(words)
    
    @lru_cache(maxsize=None)
    def minimax(state, turn):
        if all(l == r for l, r in state):
            ls = sum(1 for i, (l, r) in enumerate(state)
                     if (words[i] >> (n - l)) & 1 == 0)
            return ls > k - ls
        
        if turn == 0:  # Left
            ranges = [range(l, r + 1) if l < r else [l] for l, r in state]
            for combo in iprod(*ranges):
                if all(combo[i] == state[i][0] for i in range(k)):
                    continue
                new_state = tuple((combo[i], state[i][1]) for i in range(k))
                if minimax(new_state, 1):
                    return True
            return False
        else:  # Right
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
    return not result  # True = Right wins

def G_compute(n, k):
    """Compute G(n, k) using multiset optimization."""
    n_words = 1 << n
    total = 0
    
    # Iterate over multisets (sorted tuples)
    for combo in combinations_with_replacement(range(n_words), k):
        rw = solve_game(combo, n)
        if rw:
            # Count orderings
            cnt = Counter(combo)
            orderings = math.factorial(k)
            for c in cnt.values():
                orderings //= math.factorial(c)
            total += orderings
    
    return total

print("G(2, 3) =", G_compute(2, 3), "(expected 14)")
print("G(4, 3) =", G_compute(4, 3), "(expected 496)")
# G(6, 3) should be doable
print("Computing G(6, 3)...")
print("G(6, 3) =", G_compute(6, 3))
