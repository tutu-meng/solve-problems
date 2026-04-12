def F_brute(a, b):
    # largest gap is a*b - a - b
    max_gap = a * b - a - b
    
    # S is semigroup
    S = [False] * (max_gap + 1)
    S[0] = True
    for i in range(max_gap + 1):
        if S[i]:
            if i + a <= max_gap: S[i+a] = True
            if i + b <= max_gap: S[i+b] = True
            
    # G is gaps
    G = [i for i in range(1, max_gap + 1) if not S[i]]
    # 0 is always in config
    vertices = [0] + G
    
    # build adjacency matrix of the INCOMPARABILITY graph (non-attacking)
    n = len(vertices)
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            diff = vertices[j] - vertices[i]
            if diff > max_gap or not S[diff]:
                # not in S means non-attacking
                adj[i][j] = True
                adj[j][i] = True
    
    ans = 0
    # Find all cliques containing 0
    # Since 0 is connected to all elements in G (because difference is g in G, which is not in S),
    # we just need to find all cliques in G and add 0 to them.
    # So we just find all cliques in G.
    def dfs(idx, current_clique):
        nonlocal ans
        # sum of current config
        ans += sum(current_clique)
        for i in range(idx, n):
            v = vertices[i]
            # can we add v?
            can_add = True
            for u in current_clique:
                if u == 0: continue
                # we need to check if diff is in S
                diff = abs(v - u)
                if diff <= max_gap and S[diff]:
                    can_add = False
                    break
            if can_add:
                current_clique.append(v)
                dfs(i + 1, current_clique)
                current_clique.pop()
                
    dfs(1, [0]) # start with {0}
    return ans

print("F(3, 5) =", F_brute(3, 5))
print("F(5, 13) =", F_brute(5, 13))
