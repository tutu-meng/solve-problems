"""
Classify words of length n by their game-theoretic type.
The type of a word is determined by L(l,r) and R(l,r) for all sub-intervals.
Two words with the same type are interchangeable in any compound game.
"""
from itertools import product as iprod
from functools import lru_cache
from collections import Counter

def get_word_type(w, n):
    """Compute the game type of word w of length n.
    Returns tuple of (L_values, R_values) for all sub-intervals."""
    
    def get_bit(pos):  # 1-indexed
        return 'R' if (w >> (n - pos)) & 1 else 'L'
    
    # L(l, r) = winner when Left moves first on interval [l, r]
    # R(l, r) = winner when Right moves first on interval [l, r]
    L = {}
    R = {}
    
    for l in range(1, n+1):
        L[(l, l)] = get_bit(l)
        R[(l, l)] = get_bit(l)
    
    for length in range(2, n+1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            
            # L(l, r): Left advances l to l' in [l+1, r]
            # L wins if exists l' s.t. R(l', r) = L
            found_L = False
            for lp in range(l+1, r+1):
                if R[(lp, r)] == 'L':
                    found_L = True
                    break
            L[(l, r)] = 'L' if found_L else 'R'
            
            # R(l, r): Right retreats r to r' in [l, r-1]
            # R wins if exists r' s.t. L(l, r') = R
            found_R = False
            for rp in range(l, r):
                if L[(l, rp)] == 'R':
                    found_R = True
                    break
            R[(l, r)] = 'R' if found_R else 'L'
    
    # The type is the collection of all L and R values
    type_key = []
    for length in range(1, n+1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            type_key.append((L[(l,r)], R[(l,r)]))
    return tuple(type_key)

def classify_words(n):
    """Classify all 2^n words of length n by game type."""
    type_to_words = {}
    for w in range(1 << n):
        t = get_word_type(w, n)
        if t not in type_to_words:
            type_to_words[t] = []
        type_to_words[t].append(w)
    return type_to_words

for n in [2, 4, 8]:
    types = classify_words(n)
    print(f"\nn={n}: {len(types)} distinct types from {1 << n} words")
    for t, words in sorted(types.items(), key=lambda x: -len(x[1])):
        # Show word type and count
        word_strs = []
        for w in words[:5]:
            s = ''
            for i in range(n):
                s += 'R' if (w >> (n-1-i)) & 1 else 'L'
            word_strs.append(s)
        extra = f"... +{len(words)-5} more" if len(words) > 5 else ""
        # Just show L(1,n) and R(1,n) for the full word
        lr_full = t[-1]  # Last entry is the full interval
        print(f"  Type (L={lr_full[0]}, R={lr_full[1]}): {len(words)} words. e.g. {', '.join(word_strs)} {extra}")
