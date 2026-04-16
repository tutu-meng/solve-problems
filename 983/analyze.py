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

def analyze_r2(r2):
    pts = get_circle_points(r2)
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    print(f"R^2={r2}, vectors={len(vectors)}")
    if len(vectors) < 10: return
    
    comb = vectors[:10]
    
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
            
    print(f"Centers: {len(centers)}")
    
    hp_counts = {}
    for c in centers:
        for p in pts:
            hp = (c[0] + p[0], c[1] + p[1])
            hp_counts[hp] = hp_counts.get(hp, 0) + 1
            
    H = [p for p, cnt in hp_counts.items() if cnt >= 2]
    print(f"Harmony points: {len(H)}")

analyze_r2(325)
analyze_r2(425)
analyze_r2(625)
