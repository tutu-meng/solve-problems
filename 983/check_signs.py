import itertools
from debug_625 import get_circle_points

def check_signs():
    r2 = 625
    pts = get_circle_points(r2)
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    # Try different sign combinations for the 10 vectors
    # We can fix the first one to be positive (symmetry)
    # So 2^9 = 512 combinations
    import random
    
    for _ in range(100): # try random sign flips
        signs = [random.choice([1, -1]) for _ in range(10)]
        comb = [(v[0]*s, v[1]*s) for v, s in zip(vectors, signs)]
        
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
            continue # had a zero relation
            
        hp_counts = {}
        for c in centers:
            for p in pts:
                hp = (c[0] + p[0], c[1] + p[1])
                hp_counts[hp] = hp_counts.get(hp, 0) + 1
                
        H = [p for p, cnt in hp_counts.items() if cnt >= 2]
        if len(H) == 512:
            print(f"FOUND PERFECT SET WITH SIGNS {signs}!")
            return
            
    print("No perfect set found with random signs")

check_signs()
