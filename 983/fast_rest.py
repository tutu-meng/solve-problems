import math
import itertools
import sys

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

def check_M_fast(r2):
    pts = get_circle_points(r2)
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    if len(vectors) < 10: return False
    
    # Pre-generate D
    D = set()
    for u in pts:
        for v in pts:
            D.add((u[0]-v[0], u[1]-v[1]))
            
    combs = list(itertools.combinations(vectors, 10))
    print(f"Checking R^2={r2}, points={len(pts)}, combinations={len(combs)}", flush=True)
    
    for comb in combs:
        def dfs(idx, cx, cy, num_nonzero):
            if idx == 10:
                if num_nonzero >= 4 and num_nonzero % 2 == 0:
                    if (cx, cy) in D:
                        return False
                return True
            
            if not dfs(idx+1, cx, cy, num_nonzero): return False
            if not dfs(idx+1, cx+comb[idx][0], cy+comb[idx][1], num_nonzero+1): return False
            if not dfs(idx+1, cx-comb[idx][0], cy-comb[idx][1], num_nonzero+1): return False
            
            return True
            
        if dfs(0, 0, 0, 0):
            print(f"FOUND PERFECT SET CANDIDATE! R^2={r2}", flush=True)
            # Verify 512 centers
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
            if len(centers) == 512:
                print(f"SIZE CONFIRMED 512! R^2={r2}", flush=True)
                return True
                
    return False

r2_list = []
for r2 in range(5000, 6926):
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
    if check_M_fast(r2):
        print(f"MINIMUM IS {r2}")
        sys.exit(0)
