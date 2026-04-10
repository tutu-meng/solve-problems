"""
Hypothesis: The game equivalence class of a word is determined by 
the suffix w[2..n] (positions 2 through n). 

Let me verify this for n=4:
- LRLR and RRLR have same suffix [2..4] = RLR. They're equivalent. ✓
- LLLR and RLLR have suffix LLR and LLR. But they're NOT equivalent! ✗

So it's NOT just the suffix. Let me think differently.

The actual difference between LLLR and RLLR:
- LLLR: R(1,4)=L  (Right cannot win going first on full word)
- RLLR: R(1,4)=R  (Right can win going first on full word)

The (L,R) pair for the full word [1,n] is:
  LLLR: (L, L) 
  LRLR: (L, R) -- same class as RRLR
  RRLR: (L, R) -- same class as LRLR ✓
  LLRR: (R, L)
  LRRR: (R, R)
  RLLR: (L, R) -- same as LRLR but different class!
  RLRR: (R, R) -- same as LRRR but different class!
  RRRR: (R, R)

So just (L,R) for [1,n] isn't enough either. 

Let me look at what differentiates LRLR from RLLR (both have L(1,4)=L, R(1,4)=R):
The sub-intervals [2,3] and [2,4]:
  LRLR: L(2,3)=L, L(2,4)=L, R(2,3)=R, R(2,4)=R  
  RLLR: L(2,3)=L, L(2,4)=L, R(2,3)=L, R(2,4)=L

The R-values at [2,3] and [2,4] differ! So the SUFFIX game matters.

Maybe the equivalence class is determined by the game values of 
intervals NOT starting at position 1? Let me check.
"""

def get_game_type(w, n):
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
    return L, R

def word_str(w, n):
    s = ''
    for i in range(n):
        s += 'R' if (w >> (n-1-i)) & 1 else 'L'
    return s

n = 4
n_words = 1 << n

# For each word, compute the game values for intervals [l, r] with l >= 2
# (i.e., excluding intervals starting at position 1)
print(f"Computing game types excluding position 1 for n={n}:")
suffix_types = {}
for w in range(n_words):
    L, R = get_game_type(w, n)
    # Extract values for l >= 2 only
    key = []
    for length in range(1, n):
        for l in range(2, n - length + 2):
            r = l + length - 1
            key.append((L[(l,r)], R[(l,r)]))
    key = tuple(key)
    if key not in suffix_types:
        suffix_types[key] = []
    suffix_types[key].append(word_str(w, n))

print(f"Number of distinct suffix-type classes: {len(suffix_types)}")
for key, members in sorted(suffix_types.items(), key=lambda x: -len(x[1])):
    print(f"  [{len(members)}]: {', '.join(members)}")

# Now check if this matches the game equivalence classes
# Known equiv classes for n=4:
# [8]: all ending in L
# [2]: LRLR, RRLR
# [1] each: LLLR, LLRR, LRRR, RLLR, RLRR, RRRR

# The suffix-type should split into exactly these groups if our hypothesis is correct.
