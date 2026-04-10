"""
Find equivalence classes for n=6, 8 using the game-type approach.
For efficiency, just compute the game fingerprint based on sub-interval values.
"""
from functools import lru_cache
from collections import defaultdict

def get_game_type_key(w, n):
    """Compute game type key: the L,R values for all sub-intervals [l,r] with l >= 2."""
    def get_bit(pos):
        return 'R' if (w >> (n - pos)) & 1 else 'L'
    
    L = {}
    R = {}
    for l in range(1, n+1):
        L[(l, l)] = get_bit(l)
        R[(l, l)] = get_bit(l)
    
    for length in range(2, n+1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            L[(l, r)] = 'L' if any(R[(lp, r)] == 'L' for lp in range(l+1, r+1)) else 'R'
            R[(l, r)] = 'R' if any(L[(l, rp)] == 'R' for rp in range(l, r)) else 'L'
    
    # Key: all sub-interval values for l >= 2 (excluding intervals starting at pos 1)
    key = []
    for length in range(1, n):
        for l in range(2, n - length + 2):
            r = l + length - 1
            key.append((L[(l,r)], R[(l,r)]))
    return tuple(key)

def word_str(w, n):
    return ''.join('R' if (w >> (n-1-i)) & 1 else 'L' for i in range(n))

for n in [2, 4, 6, 8]:
    types = defaultdict(list)
    for w in range(1 << n):
        key = get_game_type_key(w, n)
        types[key].append(w)
    
    # Each type-key class consists of pairs {w, w XOR top_bit}
    # because only position 1 differs within a class.
    # The game equivalence might further merge some of these.
    
    # Count distinct classes and report
    print(f"\nn={n}: {len(types)} suffix-type classes from {1<<n} words")
    
    # How many of these classes end in L vs R?
    l_classes = 0
    r_classes = 0
    for key, members in types.items():
        last_chars = set(word_str(w, n)[-1] for w in members)
        if last_chars == {'L'}:
            l_classes += 1
        elif last_chars == {'R'}:
            r_classes += 1
        else:
            print(f"  MIXED class: {[word_str(w, n) for w in members]}")
    print(f"  L-ending classes: {l_classes}, R-ending classes: {r_classes}")
    print(f"  Total type-classes: {l_classes + r_classes}")
    
    # Show the actual class structure
    if n <= 6:
        for key, members in sorted(types.items(), key=lambda x: len(x[1]), reverse=True):
            strs = [word_str(w, n) for w in members[:5]]
            extra = f"...+{len(members)-5}" if len(members) > 5 else ""
            print(f"  [{len(members)}]: {', '.join(strs)} {extra}")
