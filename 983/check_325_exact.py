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

def check_r2(r2):
    pts = get_circle_points(r2)
    if len(pts) < 20: return
    
    # Get one from each opposite pair
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    print(f"R^2={r2}, vectors={len(vectors)}")
    
    if len(vectors) < 10: return
    
    # pick 10 vectors
    for comb in itertools.combinations(vectors, 10):
        # generate all centers (even subset sums)
        centers = set()
        for i in range(1 << 10):
            bits = bin(i).count('1')
            if bits % 2 == 0:
                cx, cy = 0, 0
                for j in range(10):
                    if (i >> j) & 1:
                        cx += comb[j][0]
                        cy += comb[j][1]
                centers.add((cx, cy))
        
        # generate all harmony points (odd subset sums)
        points = set()
        for i in range(1 << 10):
            bits = bin(i).count('1')
            if bits % 2 != 0:
                cx, cy = 0, 0
                for j in range(10):
                    if (i >> j) & 1:
                        cx += comb[j][0]
                        cy += comb[j][1]
                points.add((cx, cy))
                
        print(f"Comb size: centers={len(centers)}, points={len(points)}")
        
        # count tangencies
        tangent = False
        for c1 in centers:
            for c2 in centers:
                if c1 != c2:
                    dx = c1[0] - c2[0]
                    dy = c1[1] - c2[1]
                    if dx*dx + dy*dy == 4*r2:
                        tangent = True
                        break
            if tangent: break
            
        if not tangent:
            print(f"NO TANGENCY! Size={len(centers)}")

check_r2(325)
