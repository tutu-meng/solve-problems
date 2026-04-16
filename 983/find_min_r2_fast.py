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

def check_r2_fast(r2):
    pts = get_circle_points(r2)
    if len(pts) < 20: return False
    
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    print(f"R^2={r2}, points={len(pts)}")
    
    # We want to find 10 vectors such that no 4, 6, 8, 10 vectors sum to u - v.
    # Actually, if we just generate the 512 centers, and count the harmony points, it's very fast!
    # The slow part is itertools.combinations(vectors, 10).
    # If vectors has length 12, there are 66 combinations.
    # Generating 512 centers takes 512 * 10 operations.
    # Finding harmony points takes 512 * points operations.
    
    for comb in itertools.combinations(vectors, 10):
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
            print(f"FOUND PERFECT SET! R^2={r2}")
            return True
            
        # Try random signs
        import random
        for _ in range(50):
            signs = [random.choice([1, -1]) for _ in range(10)]
            scomb = [(v[0]*s, v[1]*s) for v, s in zip(comb, signs)]
            centers2 = set()
            for i in range(1 << 10):
                bits = bin(i).count('1')
                if bits % 2 == 0:
                    cx, cy = 0, 0
                    for j in range(10):
                        if (i >> j) & 1:
                            cx += scomb[j][0]
                            cy += scomb[j][1]
                    centers2.add((cx, cy))
            if len(centers2) == 512:
                hp_counts2 = {}
                for c in centers2:
                    for p in pts:
                        hp = (c[0] + p[0], c[1] + p[1])
                        hp_counts2[hp] = hp_counts2.get(hp, 0) + 1
                H2 = [p for p, cnt in hp_counts2.items() if cnt >= 2]
                if len(H2) == 512:
                    print(f"FOUND PERFECT SET! R^2={r2} with signs")
                    return True
                    
    return False

# List of R^2 with >= 20 points
r2_list = []
for r2 in range(1, 2000):
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

print(f"Candidate R^2: {r2_list}")

for r2 in r2_list:
    if check_r2_fast(r2):
        break
