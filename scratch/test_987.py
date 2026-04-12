import math
import itertools
from collections import defaultdict

straights_types = [
    [0,1,2,3,4],
    [1,2,3,4,5],
    [2,3,4,5,6],
    [3,4,5,6,7],
    [4,5,6,7,8],
    [5,6,7,8,9],
    [6,7,8,9,10],
    [7,8,9,10,11],
    [8,9,10,11,12],
    [9,10,11,12,0]
]

def P(n, k):
    if k < 0 or k > n: return 0
    return math.perm(n, k)

def get_colorings(S, T):
    # S is a list of indices into T
    n = len(S)
    if n == 0: return 1
    
    # build adjacency matrix
    adj = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            # check overlap
            type1 = T[S[i]]
            type2 = T[S[j]]
            if set(straights_types[type1]).intersection(straights_types[type2]):
                adj[i][j] = adj[j][i] = True
                
    # count 4-colorings using backtracking
    colors = [-1]*n
    ans = [0]
    
    def dfs(u):
        if u == n:
            ans[0] += 1
            return
        # try colors 0..3
        for c in range(4):
            ok = True
            for v in range(u):
                if adj[u][v] and colors[v] == c:
                    ok = False
                    break
            if ok:
                colors[u] = c
                dfs(u+1)
                
    dfs(0)
    return ans[0]

def solve(N):
    total = 0
    # Iterating over combinations with replacement of types
    for comb in itertools.combinations_with_replacement(range(10), N):
        # find number of ordered T's that give this comb
        # meaning we compute for this unordered comb, and then no need to divide by N!
        # wait! 
        # For a fixed unordered combination of types, how many ways to assign suits?
        # Actually, it's easier to just compute for the unordered combination. 
        # But wait, straights are distinct objects if they end up picking different cards.
        # So we should think about it this way:
        # We are forming N subsets of 5 cards. Order of the subsets doesn't matter.
        # If we assume the N straights are ordered (from 1 to N), then we have N! permutations.
        # However, if two straights are of the exact same type, they might be symmetric?
        # Let's just do ordered T, sum up, and divide by N!.
        pass

    ans = 0
    for T in itertools.product(range(10), repeat=N):
        # check max 4 per rank
        C = [0]*13
        valid = True
        for t in T:
            for r in straights_types[t]:
                C[r] += 1
                if C[r] > 4: valid = False
        if not valid: continue
        
        ways_T = 0
        for i in range(1 << N):
            S = []
            for j in range(N):
                if (i >> j) & 1:
                    S.append(j)
            
            colorings = get_colorings(S, T)
            if colorings == 0: continue
            
            k_r = [0]*13
            m_r = [0]*13
            for j in range(N):
                if j in S:
                    for r in straights_types[T[j]]: k_r[r] += 1
                else:
                    for r in straights_types[T[j]]: m_r[r] += 1
            
            prod = 1
            for r in range(13):
                prod *= P(4 - k_r[r], m_r[r])
                
            sign = 1 if len(S) % 2 == 0 else -1
            ways_T += sign * colorings * prod
            
        ans += ways_T
        
    print(f"N={N}, Ans: {ans // math.factorial(N)}")

solve(1)
solve(2)
