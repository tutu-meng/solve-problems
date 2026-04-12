import math
import itertools

# In Poker a straight is exactly five cards of sequential rank NOT all of the same suit.
# An ace can rank either high (A-K-Q-J-10) or low (5-4-3-2-A).
# 10 types of straights (A=0, 2=1, ..., K=12).
straights_types = [
    [0,1,2,3,4],    # A-2-3-4-5 (Low Ace)
    [1,2,3,4,5],
    [2,3,4,5,6],
    [3,4,5,6,7],
    [4,5,6,7,8],
    [5,6,7,8,9],
    [6,7,8,9,10],
    [7,8,9,10,11],
    [8,9,10,11,12],
    [9,10,11,12,0]  # 10-J-Q-K-A (High Ace)
]

def P(n, k):
    if k < 0 or k > n: return 0
    return math.perm(n, k)

def get_colorings(S, T):
    """
    Counts ways to assign colors (suits) to the subset of straights indexed by S
    such that overlapping straights in S have different colors.
    """
    n = len(S)
    if n == 0: return 1
    
    adj = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            type1 = T[S[i]]
            type2 = T[S[j]]
            # Check if any rank is shared
            if set(straights_types[type1]).intersection(straights_types[type2]):
                adj[i][j] = adj[j][i] = True
                
    colors = [-1]*n
    ans = [0]
    
    def dfs(u):
        if u == n:
            ans[0] += 1
            return
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
    ans = 0
    # Iterate over combinations with replacement of types (unordered sets of types)
    for comb in itertools.combinations_with_replacement(range(10), N):
        c = [0]*10
        for x in comb: c[x] += 1
        
        # T is the ordered list of types for this combination
        T = list(comb)
        
        # Pre-check: no rank can be covered by more than 4 straights (since only 4 suits)
        C = [0]*13
        valid = True
        for t in T:
            for r in straights_types[t]:
                C[r] += 1
                if C[r] > 4: valid = False
        if not valid: continue
        
        ways_T = 0
        # Inclusion-Exclusion Principle:
        # Number of ways where none of the N straights are straight-flushes.
        # Sum over S (subset of straights that are straight-flushes) of (-1)^|S| * Ways(S is flush)
        for i in range(1 << N):
            S = []
            for j in range(N):
                if (i >> j) & 1:
                    S.append(j)
            
            # colorings is the number of ways to assign suits to straights in S
            # such that they don't share the same card (since they already share rank).
            colorings = get_colorings(S, T)
            if colorings == 0: continue
            
            k_r = [0]*13 # count of SF straights at rank r
            m_r = [0]*13 # count of non-SF straights at rank r
            for j in range(N):
                if j in S:
                    for r in straights_types[T[j]]: k_r[r] += 1
                else:
                    for r in straights_types[T[j]]: m_r[r] += 1
            
            # For each rank, the non-SF straights pick suits from the remaining 4 - k_r suits.
            prod = 1
            for r in range(13):
                prod *= P(4 - k_r[r], m_r[r])
                
            sign = 1 if len(S) % 2 == 0 else -1
            ways_T += sign * colorings * prod
            
        # Account for symmetries of the same type
        div = 1
        for count in c:
            div *= math.factorial(count)
            
        ans += ways_T // div
        
    return ans

if __name__ == "__main__":
    import sys
    N = 8
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    print(solve(N))
