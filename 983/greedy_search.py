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

def check_r2_greedy(r2):
    pts = get_circle_points(r2)
    if len(pts) < 20: return False
    
    vectors = []
    seen = set()
    for p in pts:
        if p not in seen and (-p[0], -p[1]) not in seen:
            vectors.append(p)
            seen.add(p)
            
    # D is the set of all u - v
    D = set()
    for u in pts:
        for v in pts:
            D.add((u[0]-v[0], u[1]-v[1]))
            
    # Greedy choice of 10 vectors
    # We want to pick v_1, ..., v_10 such that no even subset sum (length >= 4) is in D
    
    def find_independent(current_chosen, idx):
        if len(current_chosen) == 10:
            return current_chosen
        if idx >= len(vectors):
            return None
            
        # Try to add vectors[idx]
        new_v = vectors[idx]
        
        # Check if adding new_v creates a relation
        # We need to check all combinations of coefficients for current_chosen + [new_v]
        # where the coefficient of new_v is non-zero (1 or -1)
        # Actually, just generate all even subset sums of the new set, and check if in D
        valid = True
        
        # We can just generate all sums of length 4, 6, 8, 10
        def check_sums(i, cx, cy, num_nonzero, must_include_new):
            if i == len(current_chosen):
                # now for the new_v
                for coef in [1, -1]:
                    nx, ny = cx + coef * new_v[0], cy + coef * new_v[1]
                    nnz = num_nonzero + 1
                    if nnz >= 4 and nnz % 2 == 0:
                        if (nx, ny) in D:
                            return False
                # also check without new_v if must_include_new is False
                if not must_include_new:
                    # but we already checked those when building current_chosen!
                    pass
                return True
                
            # try 0
            if not check_sums(i + 1, cx, cy, num_nonzero, must_include_new): return False
            # try 1
            if not check_sums(i + 1, cx + current_chosen[i][0], cy + current_chosen[i][1], num_nonzero + 1, must_include_new): return False
            # try -1
            if not check_sums(i + 1, cx - current_chosen[i][0], cy - current_chosen[i][1], num_nonzero + 1, must_include_new): return False
            
            return True
            
        if check_sums(0, 0, 0, 0, True):
            res = find_independent(current_chosen + [new_v], idx + 1)
            if res: return res
            
        # Try skipping
        res = find_independent(current_chosen, idx + 1)
        if res: return res
        
        return None
        
    res = find_independent([], 0)
    if res:
        print(f"FOUND PERFECT SET! R^2={r2} with vectors {res}")
        return r2
    return None

def solve():
    r2_list = []
    for r2 in range(1, 10000):
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
            
    print(f"Candidate R^2 up to 10000: {len(r2_list)} candidates")
    
    for r2 in r2_list:
        if check_r2_greedy(r2):
            break

if __name__ == '__main__':
    solve()
