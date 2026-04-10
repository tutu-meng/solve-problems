"""
Key insight: In the single-word game, every position 2..n (Left first) 
and 1..n-1 (Right first) is reachable. So what matters for the compound
game is the content at those positions.

For the compound game on k words, both players choose positions for each word.
The surviving position for word i is p_i.
Left advances from left (p_i >= start), Right from right (p_i <= end).

Since LEFT can advance left boundary of each word by any amount (0 to n-1) 
and RIGHT can retreat right boundary, the game is about who "closes" each word
and at what position.

Let me study: for k words, compute a "compound game value" based on 
which words Right wins, and verify against brute force.
"""
from itertools import product as iprod
from functools import lru_cache

def solve_game_bf(words, n):
    """Brute force minimax."""
    k = len(words)
    
    @lru_cache(maxsize=None)
    def minimax(state, turn):
        intervals = state
        if all(l == r for l, r in intervals):
            ls = 0
            for i, (l, r) in enumerate(intervals):
                if (words[i] >> (n - l)) & 1 == 0:
                    ls += 1
            return ls > k - ls  # True = Left wins
        
        if turn == 0:  # Left's turn
            ranges = []
            for l, r in intervals:
                ranges.append(list(range(l, r + 1)) if l < r else [l])
            
            for combo in iprod(*ranges):
                if all(combo[i] == intervals[i][0] for i in range(k)):
                    continue
                new_state = tuple((combo[i], intervals[i][1]) for i in range(k))
                if minimax(new_state, 1):
                    return True
            return False
        else:  # Right's turn
            ranges = []
            for l, r in intervals:
                ranges.append(list(range(l, r + 1)) if l < r else [r])
            
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
    return not result  # True = Right wins

# For n=2: study what determines the outcome
# Each word is characterized by (w[1], w[2]) = (left_char, right_char)
# When Left trims a word: position 2 survives (right char)
# When Right trims a word: position 1 survives (left char)

# For n=4, k=3: study which triples give Right wins
# Represent each word by its character at each position
n = 4
k = 3
print(f"Studying n={n}, k={k}")
print(f"Total words: {1<<n}, total tuples: {(1<<n)**k}")

right_wins = 0
# Group words by their L-count at each position
# word -> tuple of L/R at positions 1..n
for combo in iprod(range(1<<n), repeat=k):
    if solve_game_bf(combo, n):
        right_wins += 1

print(f"Right wins: {right_wins}")

# Now let's classify by just the number of L's at each position across the k words
from collections import defaultdict
signature_counts = defaultdict(lambda: [0, 0])  # [left_wins, right_wins]

for combo in iprod(range(1<<n), repeat=k):
    # For each position p in 1..n, count L's among the k words
    sig = []
    for p in range(1, n+1):
        l_count = sum(1 for w in combo if (w >> (n-p)) & 1 == 0)
        sig.append(l_count)
    sig = tuple(sig)
    
    rw = solve_game_bf(combo, n)
    signature_counts[sig][1 if rw else 0] += 1

print(f"\nNumber of distinct position-count signatures: {len(signature_counts)}")
print("Signature (L-counts at pos 1..n) -> [Left wins, Right wins]")
for sig in sorted(signature_counts.keys()):
    lw, rw = signature_counts[sig]
    total = lw + rw
    if rw > 0 and lw > 0:
        print(f"  {sig}: L={lw}, R={rw} (mixed!)")
    elif rw > 0:
        print(f"  {sig}: R={rw}")
