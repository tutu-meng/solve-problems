"""
Problem 949: Left vs Right word game solver.
Brute-force minimax to verify G(2,3)=14 and G(4,3)=496.
"""
from itertools import product
from functools import lru_cache

def solve_game(words, n):
    """Determine if Right wins when Left plays first, given k words of length n."""
    k = len(words)
    
    # State: tuple of (li, ri) for each word (1-indexed), plus turn (0=Left, 1=Right)
    # Terminal: all li == ri
    # Left advances li's, Right retreats ri's
    
    @lru_cache(maxsize=None)
    def minimax(state, turn):
        intervals = state
        # Check terminal
        if all(l == r for l, r in intervals):
            # Count L's and R's
            ls = 0
            for i, (l, r) in enumerate(intervals):
                pos = l  # l == r, 0-indexed position in word
                if (words[i] >> (n - pos)) & 1 == 0:  # 0 = L
                    ls += 1
            rs = k - ls
            return 'L' if ls > rs else 'R'
        
        if turn == 0:  # Left's turn: advance some li's
            # Generate all possible moves
            # For each word, new_li can be from li to ri (advance by 0 to ri-li)
            # At least one must advance
            ranges = []
            for l, r in intervals:
                if l < r:
                    ranges.append(list(range(l, r + 1)))  # new l from l to r
                else:
                    ranges.append([l])  # already done, can't change
            
            for combo in product(*ranges):
                if all(combo[i] == intervals[i][0] for i in range(k)):
                    continue  # must advance at least one
                new_state = tuple((combo[i], intervals[i][1]) for i in range(k))
                val = minimax(new_state, 1)
                if val == 'L':
                    return 'L'  # Left found winning move
            return 'R'
        
        else:  # Right's turn: retreat some ri's
            ranges = []
            for l, r in intervals:
                if l < r:
                    ranges.append(list(range(l, r + 1)))  # new r from l to r
                else:
                    ranges.append([r])
            
            for combo in product(*ranges):
                if all(combo[i] == intervals[i][1] for i in range(k)):
                    continue
                new_state = tuple((intervals[i][0], combo[i]) for i in range(k))
                val = minimax(new_state, 0)
                if val == 'R':
                    return 'R'
            return 'L'
    
    initial = tuple((1, n) for _ in range(k))
    result = minimax(initial, 0)
    minimax.cache_clear()
    return result == 'R'

def G(n, k):
    count = 0
    total = (1 << n) ** k
    for idx, combo in enumerate(product(range(1 << n), repeat=k)):
        if solve_game(combo, n):
            count += 1
        if idx % 10000 == 9999:
            print(f"  Progress: {idx+1}/{total}")
    return count

print("Computing G(2, 3)...")
g23 = G(2, 3)
print(f"G(2, 3) = {g23} (expected 14)")

print("\nComputing G(4, 3)...")
g43 = G(4, 3)
print(f"G(4, 3) = {g43} (expected 496)")
