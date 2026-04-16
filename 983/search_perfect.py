import math

def get_circle_points(r2):
    pts = []
    limit = int(math.isqrt(r2))
    for dx in range(-limit, limit + 1):
        dy2 = r2 - dx*dx
        if dy2 < 0: continue
        dy = int(math.isqrt(dy2))
        if dy * dy == dy2:
            pts.append((dx, dy))
            if dy != 0:
                pts.append((dx, -dy))
    return pts

def find_perfect(r2, max_n=10):
    base_pts = get_circle_points(r2)
    if not base_pts:
        return
    
    possible_centers = set()
    for p in base_pts:
        for q in base_pts:
            if p != q:
                cx, cy = p[0] - q[0], p[1] - q[1]
                if cx == 0 and cy == 0: continue
                if cx*cx + cy*cy == 4*r2: continue
                possible_centers.add((cx, cy))
                
    possible_centers = list(possible_centers)
    
    visited = set()
    queue = [frozenset([(0,0)])]
    visited.add(frozenset([(0,0)]))
    
    found_sizes = set()
    
    while queue:
        C = queue.pop(0)
        n = len(C)
        
        if n > 1:
            point_counts = {}
            for c in C:
                for p in base_pts:
                    hp = (c[0] + p[0], c[1] + p[1])
                    point_counts[hp] = point_counts.get(hp, 0) + 1
            
            H = [p for p, cnt in point_counts.items() if cnt >= 2]
            
            if len(H) == n:
                if n not in found_sizes:
                    found_sizes.add(n)
                    print(f"R^2={r2}, Perfect set of size {n}")
                    
        if n >= max_n:
            continue
            
        for c in C:
            for pc in possible_centers:
                nc = (c[0] + pc[0], c[1] + pc[1])
                if nc not in C:
                    tangent = False
                    for c2 in C:
                        dx, dy = nc[0] - c2[0], nc[1] - c2[1]
                        if dx*dx + dy*dy == 4*r2:
                            tangent = True
                            break
                    if not tangent:
                        new_C = frozenset(list(C) + [nc])
                        if new_C not in visited:
                            visited.add(new_C)
                            queue.append(new_C)

for r2 in range(1, 20):
    find_perfect(r2, max_n=8)
