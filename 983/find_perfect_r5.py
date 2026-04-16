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

def find_perfect(r2):
    pts = get_circle_points(r2)
    # try to form a graph of all possible centers from a starting point
    # actually, just do BFS to generate connected components of centers
    queue = [frozenset([(0,0)])]
    visited = set(queue)
    
    found = set()
    
    # Precompute possible neighbor steps
    steps = set()
    for p1 in pts:
        for p2 in pts:
            if p1 != p2:
                steps.add((p1[0]-p2[0], p1[1]-p2[1]))
                
    while queue:
        C = queue.pop(0)
        n = len(C)
        
        hp_counts = {}
        for c in C:
            for p in pts:
                hp = (c[0]+p[0], c[1]+p[1])
                hp_counts[hp] = hp_counts.get(hp, 0) + 1
        
        H = [p for p, cnt in hp_counts.items() if cnt >= 2]
        
        if len(H) == n and n >= 2:
            if n not in found:
                print(f"Perfect set of size {n} for R^2={r2}!")
                found.add(n)
                
        if n >= 6: continue
        
        # add a neighbor
        for c in C:
            for s in steps:
                nc = (c[0]+s[0], c[1]+s[1])
                if nc not in C:
                    new_C = frozenset(list(C) + [nc])
                    if new_C not in visited:
                        visited.add(new_C)
                        queue.append(new_C)

find_perfect(5)
