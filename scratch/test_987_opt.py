import math
import itertools

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
    n = len(S)
    if n == 0: return 1
    
    adj = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            type1 = T[S[i]]
            type2 = T[S[j]]
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
    # counts c_i forms a profile
    for comb in itertools.combinations_with_replacement(range(10), N):
        c = [0]*10
        for x in comb: c[x] += 1
        
        # arbitrary ordered T
        T = []
        for x in comb: T.append(x)
        
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
            
        div = 1
        for count in c:
            div *= math.factorial(count)
            
        ans += ways_T // div
        
    print(f"N={N}, Ans: {ans}")

solve(1)
solve(2)
solve(8)
