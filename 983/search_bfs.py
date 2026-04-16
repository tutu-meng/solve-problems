import itertools

def get_circle_points(r2):
    pts = []
    limit = int(r2**0.5)
    for dx in range(-limit, limit + 1):
        dy2 = r2 - dx*dx
        if dy2 < 0: continue
        dy = int(dy2**0.5)
        if dy * dy == dy2:
            pts.append((dx, dy))
            if dy != 0:
                pts.append((dx, -dy))
    return pts

def search_for_perfect_sets(r2, max_size=15):
    pts = get_circle_points(r2)
    # the bipartite graph between centers and points.
    # to be perfect, |C| = |H|.
    # instead of full search, we can use the integer linear programming or BFS on subsets.
    
    # Just do a BFS on centers.
    # Start with one center (0,0).
    # Its harmony points must be among its circle points.
    
    visited = set()
    queue = [frozenset([(0,0)])]
    
    found_sizes = set()
    
    while queue:
        C = queue.pop(0)
        n = len(C)
        
        # calculate harmony points
        point_counts = {}
        for c in C:
            for p in pts:
                hp = (c[0] + p[0], c[1] + p[1])
                point_counts[hp] = point_counts.get(hp, 0) + 1
                
        H = [p for p, cnt in point_counts.items() if cnt >= 2]
        
        # Check connectivity
        if n >= 2:
            # simple connected check
            adj = {c: [] for c in C}
            for i, c1 in enumerate(C):
                for c2 in list(C)[i+1:]:
                    inter = 0
                    for p in pts:
                        hp = (c1[0] + p[0], c1[1] + p[1])
                        dx, dy = hp[0] - c2[0], hp[1] - c2[1]
                        if dx*dx + dy*dy == r2:
                            inter += 1
                    if inter == 2:
                        adj[c1].append(c2)
                        adj[c2].append(c1)
            
            # BFS from first
            c_list = list(C)
            q2 = [c_list[0]]
            v2 = {c_list[0]}
            while q2:
                curr = q2.pop(0)
                for nxt in adj[curr]:
                    if nxt not in v2:
                        v2.add(nxt)
                        q2.append(nxt)
            
            if len(v2) == n: # connected
                # check tangency
                tangent = False
                for c1 in C:
                    for c2 in C:
                        if c1 != c2:
                            dx, dy = c1[0] - c2[0], c1[1] - c2[1]
                            if dx*dx + dy*dy == 4*r2:
                                tangent = True
                                break
                    if tangent: break
                
                if not tangent:
                    if len(H) == n:
                        if n not in found_sizes:
                            found_sizes.add(n)
                            print(f"R^2={r2}, n={n}, C={C}")
                            
        if n >= max_size: continue
        
        # to expand C, add a center that harmonises with some center in C
        for c in C:
            for p1 in pts:
                for p2 in pts:
                    if p1 == p2: continue
                    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
                    nc = (c[0] + dx, c[1] + dy)
                    if nc not in C:
                        # try adding nc
                        new_C = frozenset(list(C) + [nc])
                        if new_C not in visited:
                            visited.add(new_C)
                            queue.append(new_C)

search_for_perfect_sets(5, 8)
