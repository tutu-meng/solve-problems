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
    
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    print(f"R^2={r2}, vectors={len(vectors)}")
    
    # We can try all subsets of 10, 11, 12 vectors
    for k in range(10, len(vectors) + 1):
        for comb in itertools.combinations(vectors, k):
            centers_counts = {}
            for i in range(1 << k):
                bits = bin(i).count('1')
                if bits % 2 == 0:
                    cx, cy = 0, 0
                    for j in range(k):
                        if (i >> j) & 1:
                            cx += comb[j][0]
                            cy += comb[j][1]
                    centers_counts[(cx, cy)] = centers_counts.get((cx, cy), 0) + 1
            centers = set(centers_counts.keys())
            
            if len(centers) < 500: continue
            
            # calculate harmony points: points that appear >= 2 times as c + v
            hp_counts = {}
            for c in centers:
                for v in comb:
                    hp = (c[0] + v[0], c[1] + v[1])
                    hp_counts[hp] = hp_counts.get(hp, 0) + 1
                    hp2 = (c[0] - v[0], c[1] - v[1])
                    hp_counts[hp2] = hp_counts.get(hp2, 0) + 1
            
            H = [p for p, cnt in hp_counts.items() if cnt >= 2]
            
            if len(H) == len(centers):
                # Check tangency
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
                    print(f"FOUND PERFECT SET! R^2={r2}, size={len(centers)}")
                    return True

check_r2(325)
check_r2(425)
check_r2(625)
