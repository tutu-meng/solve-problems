import itertools

def check_k3():
    v1, v2, v3 = (1, 2), (2, 1), (-1, 2)
    vectors = [v1, v2, v3]
    
    centers = set()
    for i in range(8):
        bits = bin(i).count('1')
        if bits % 2 == 0:
            cx, cy = 0, 0
            for j in range(3):
                if (i >> j) & 1:
                    cx += vectors[j][0]
                    cy += vectors[j][1]
            centers.add((cx, cy))
            
    print(f"Centers: {centers}")
    
    r2 = 5
    from debug_625 import get_circle_points
    pts = get_circle_points(r2)
    
    hp_counts = {}
    for c in centers:
        for p in pts:
            hp = (c[0] + p[0], c[1] + p[1])
            hp_counts[hp] = hp_counts.get(hp, 0) + 1
            
    H = [p for p, cnt in hp_counts.items() if cnt >= 2]
    print(f"Harmony points size: {len(H)}")

check_k3()
