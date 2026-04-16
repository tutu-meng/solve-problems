import itertools
from debug_625 import get_circle_points

def check_k10():
    r2 = 625
    pts = get_circle_points(r2)
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
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
            
    hp_counts = {}
    for c in centers:
        for p in pts:
            hp = (c[0] + p[0], c[1] + p[1])
            hp_counts[hp] = hp_counts.get(hp, 0) + 1
            
    H = [p for p, cnt in hp_counts.items() if cnt >= 2]
    
    odd_sums = set()
    for i in range(1 << 10):
        bits = bin(i).count('1')
        if bits % 2 != 0:
            cx, cy = 0, 0
            for j in range(10):
                if (i >> j) & 1:
                    cx += comb[j][0]
                    cy += comb[j][1]
            odd_sums.add((cx, cy))
            
    extra = [p for p in H if p not in odd_sums]
    print(f"Extra harmony points: {len(extra)}")
    if extra:
        print(f"Example extra: {extra[0]}")
        # find which centers share this
        shared_by = [c for c in centers if (extra[0][0]-c[0])**2 + (extra[0][1]-c[1])**2 == r2]
        print(f"Shared by centers: {shared_by}")
        print(f"Distance squared between centers: {(shared_by[0][0]-shared_by[1][0])**2 + (shared_by[0][1]-shared_by[1][1])**2}")

check_k10()
