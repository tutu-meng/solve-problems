"""
Pattern for n=4 R-ending words:
  LLLR (class by itself)
  LRLR, RRLR (a pair) 
  LLRR (alone)
  LRRR (alone)
  RLLR (alone)
  RLRR (alone)
  RRRR (alone)

Let me look at even positions (2, 4) = R-trimming positions:
  LLLR: pos 2=L, pos 4=R -> "LR"
  LRLR: pos 2=R, pos 4=R -> "RR"
  RRLR: pos 2=R, pos 4=R -> "RR"  <- same as LRLR! ✓ they're in same class
  LLRR: pos 2=L, pos 4=R -> "LR" (same as LLLR but they're different classes!)
  
Hmm, not just even positions. Let me look at positions 2,3,4 (all except 1):
  LLLR: positions 2,3,4 = L,L,R
  LRLR: positions 2,3,4 = R,L,R
  RRLR: positions 2,3,4 = R,L,R  ✓ same!
  LLRR: positions 2,3,4 = L,R,R  
  
So the class is determined by positions 2..n? Let me verify.
  LLLR -> LLR   RLLR -> LLR  (but they're in different classes!)

Wait no, LLLR is class alone and RLLR is class alone. They have same 2..4 = LLR but different classes. So it's NOT just positions 2..n.

Hmm. Let me look more carefully.

Maybe it's the SUFFIX structure that matters. Let me look at each word's 
suffix composition:
  LLLR -> suffixes: R, LR, LLR, LLLR
  RLLR -> suffixes: R, LR, LLR, RLLR  
Same suffixes except the full word!

For the game, what matters is all sub-intervals. Let me look at what differs.
"""

# Let me check what the actual game type (L/R values for all sub-intervals) looks like.
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
            found_L = False
            for lp in range(l+1, r+1):
                if R[(lp, r)] == 'L':
                    found_L = True
                    break
            L[(l, r)] = 'L' if found_L else 'R'
            
            found_R = False
            for rp in range(l, r):
                if L[(l, rp)] == 'R':
                    found_R = True
                    break
            R[(l, r)] = 'R' if found_R else 'L'
    
    return L, R

def word_str(w, n):
    s = ''
    for i in range(n):
        s += 'R' if (w >> (n-1-i)) & 1 else 'L'
    return s

n = 4
# Compare game types of words in same class vs different class
print("Comparing LLLR (w=1) and RLLR (w=9):")
L1, R1 = get_game_type(1, n)  # LLLR = 0001 = 1
L2, R2 = get_game_type(9, n)  # RLLR = 1001 = 9

for length in range(1, n+1):
    for l in range(1, n - length + 2):
        r = l + length - 1
        l_same = L1[(l,r)] == L2[(l,r)]
        r_same = R1[(l,r)] == R2[(l,r)]
        if not l_same or not r_same:
            print(f"  [{l},{r}]: LLLR: L={L1[(l,r)]} R={R1[(l,r)]}, RLLR: L={L2[(l,r)]} R={R2[(l,r)]}")

print("\nComparing LRLR (w=5) and RRLR (w=13):")
L1, R1 = get_game_type(5, n)  # LRLR = 0101 = 5
L2, R2 = get_game_type(13, n) # RRLR = 1101 = 13

for length in range(1, n+1):
    for l in range(1, n - length + 2):
        r = l + length - 1
        l_same = L1[(l,r)] == L2[(l,r)]
        r_same = R1[(l,r)] == R2[(l,r)]
        if not l_same or not r_same:
            print(f"  [{l},{r}]: LRLR: L={L1[(l,r)]} R={R1[(l,r)]}, RRLR: L={L2[(l,r)]} R={R2[(l,r)]}")

# Print full game types for the R-ending words
print("\nFull game types for R-ending words:")
for w in [1, 5, 3, 7, 9, 11, 13, 15]:
    L, R = get_game_type(w, n)
    ws = word_str(w, n)
    # Show L(1,n) and R(1,n), and the key distinguishing intervals
    print(f"  {ws}: L(1,4)={L[(1,4)]}, R(1,4)={R[(1,4)]}")
    for length in range(1, n+1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            print(f"    [{l},{r}]: L={L[(l,r)]} R={R[(l,r)]}")
    print()
