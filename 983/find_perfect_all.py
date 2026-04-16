import math
import itertools

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

def check_M_all(r2):
    pts = get_circle_points(r2)
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    if len(vectors) < 10: return False
    
    combs = list(itertools.combinations(vectors, 10))
    print(f"Checking R^2={r2}, points={len(pts)}, combinations={len(combs)}")
    
    for comb in combs:
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
        if len(centers) < 512:
            continue
            
        hp_counts = {}
        for c in centers:
            for p in pts:
                hp = (c[0] + p[0], c[1] + p[1])
                hp_counts[hp] = hp_counts.get(hp, 0) + 1
        H = [p for p, cnt in hp_counts.items() if cnt >= 2]
        
        if len(H) == 512:
            # check tangency
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
                print(f"FOUND PERFECT SET! R^2={r2}")
                return True
    return False

r2_list = []
for r2 in range(1, 6926):
    limit = int(math.isqrt(r2))
    cnt = 0
    for dx in range(-limit, limit + 1):
        dy2 = r2 - dx*dx
        if dy2 < 0: continue
        dy = int(math.isqrt(dy2))
        if dy * dy == dy2:
            cnt += 1
            if dy != 0: cnt += 1
    if cnt >= 20:
        r2_list.append(r2)

for r2 in r2_list:
    if check_M_all(r2):
        break
