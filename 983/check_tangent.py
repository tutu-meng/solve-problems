import itertools
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

def check_r2_exact(r2):
    pts = get_circle_points(r2)
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    if len(vectors) < 10: return
    
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
                
        if len(centers) < 500: continue
        
        hp_counts = {}
        for c in centers:
            for p in pts:
                hp = (c[0] + p[0], c[1] + p[1])
                hp_counts[hp] = hp_counts.get(hp, 0) + 1
                
        H = [p for p, cnt in hp_counts.items() if cnt >= 2]
        
        if len(H) == len(centers):
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
            else:
                print(f"R^2={r2} size={len(centers)} IS PERFECT BUT TANGENT!")
    return False

check_r2_exact(325)
check_r2_exact(425)
