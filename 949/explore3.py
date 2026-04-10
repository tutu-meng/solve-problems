"""
For each word of length n, compute a simpler 'signature':
The set of positions that Left can guarantee as the final surviving position
when playing this word in isolation with Left first, and Right first.
"""
from functools import lru_cache

def word_positions(w, n):
    """For word w of length n, compute which positions Left can force
    and which positions Right can force, for both Left-first and Right-first."""
    
    def get_bit(pos):  # 1-indexed
        return 'R' if (w >> (n - pos)) & 1 else 'L'
    
    # L_set(l, r) = set of positions Left can force (as surviving) with Left first
    # R_set(l, r) = set of positions Right can force with Right first
    @lru_cache(maxsize=None)
    def L_set(l, r):
        if l == r:
            return frozenset([l])
        # Left trims a (1 to r-l) from left -> interval [l+a, r], Right's turn
        result = set()
        for a in range(1, r - l + 1):
            # After Left trims, Right moves. Right wants to pick worst for Left.
            # Left gets to pick 'a', then position is in R_set(l+a, r)
            result |= R_set(l + a, r)
        return frozenset(result)
    
    @lru_cache(maxsize=None)
    def R_set(l, r):
        if l == r:
            return frozenset([l])
        result = set()
        for b in range(1, r - l + 1):
            result |= L_set(l, r - b)
        return frozenset(result)
    
    return L_set(1, n), R_set(1, n)

for n in [2, 3, 4, 5, 6]:
    print(f"\n=== n={n} ===")
    for w in range(1 << n):
        s = ''
        for i in range(n):
            s += 'R' if (w >> (n-1-i)) & 1 else 'L'
        ls, rs = word_positions(w, n)
        print(f"  {s}: L_first_positions={sorted(ls)}, R_first_positions={sorted(rs)}")
