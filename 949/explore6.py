"""
n=4 equivalence classes:
  Class 14 (8 words): LLLL, LLRL, LRLL, LRRL, RLLL, RLRL, RRLL, RRRL 
    -> All end with 'L' but NOT matching LLLR, RLLR, LRLR, RRLR patterns
    -> Actually: all words ending in 'L' that have L at position 4 (last)
    Wait: LLRL ends in L (pos 4 = L). LLLR ends in R. 
    So class 14 = all words ending in L. That's 8 words. ✓
  
  Class 15: RRRR -> all R
  Class 1: LLLR 
  Class 3: LLRR
  Class 7: LRRR
  Class 9: RLLR
  Class 11: RLRR
  Class 13: LRLR, RRLR -> 2 words

So words ending in L are all equivalent (8 words = 1 class).
Words ending in R are split into 7 classes.

Let me check: for n=2, what are the classes?
"""
from itertools import product as iprod
from functools import lru_cache
from collections import defaultdict

def solve_game_bf(words, n):
    k = len(words)
    @lru_cache(maxsize=None)
    def minimax(state, turn):
        intervals = state
        if all(l == r for l, r in intervals):
            ls = sum(1 for i, (l, r) in enumerate(intervals)
                     if (words[i] >> (n - l)) & 1 == 0)
            return ls > k - ls
        if turn == 0:
            ranges = [list(range(l, r + 1)) if l < r else [l] for l, r in intervals]
            for combo in iprod(*ranges):
                if all(combo[i] == intervals[i][0] for i in range(k)):
                    continue
                new_state = tuple((combo[i], intervals[i][1]) for i in range(k))
                if minimax(new_state, 1):
                    return True
            return False
        else:
            ranges = [list(range(l, r + 1)) if l < r else [r] for l, r in intervals]
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
    return not result

def find_equiv_classes(n, k):
    n_words = 1 << n
    equiv = list(range(n_words))
    
    def find(x):
        while equiv[x] != x:
            equiv[x] = equiv[equiv[x]]
            x = equiv[x]
        return x
    
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            equiv[rx] = ry
    
    for w1 in range(n_words):
        for w2 in range(w1+1, n_words):
            equivalent = True
            for others in iprod(range(n_words), repeat=k-1):
                combo1 = (w1,) + others
                combo2 = (w2,) + others
                if solve_game_bf(combo1, n) != solve_game_bf(combo2, n):
                    equivalent = False
                    break
            if equivalent:
                union(w1, w2)
    
    classes = defaultdict(list)
    for w in range(n_words):
        classes[find(w)].append(w)
    return classes

def word_str(w, n):
    s = ''
    for i in range(n):
        s += 'R' if (w >> (n-1-i)) & 1 else 'L'
    return s

for n in [2, 4, 6]:
    k = 3
    print(f"\n=== n={n}, k={k} ===")
    classes = find_equiv_classes(n, k)
    print(f"Number of equiv classes: {len(classes)}")
    for cls_id in sorted(classes):
        members = classes[cls_id]
        strs = [word_str(w, n) for w in members]
        print(f"  [{len(members)}]: {', '.join(strs[:10)}" + ("..." if len(strs)>10 else "") + ")")
