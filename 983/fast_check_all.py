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

def solve():
    r2_list = []
    for r2 in range(1, 5000):
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
            
    print(f"Candidate R^2 up to 5000: {r2_list}")
    
    for r2 in r2_list:
        pts = get_circle_points(r2)
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
                
        # To avoid the slow combinations, we can generate all combinations of 10 vectors
        found_perfect = False
        for comb in itertools.combinations(vectors, 10):
            # check all sum epsilon_i v_i with sum |epsilon_i| even and >= 4
            # We can use recursion to generate sums
            
            def check_sums(idx, current_x, current_y, num_nonzero):
                if idx == 10:
                    if num_nonzero >= 4 and num_nonzero % 2 == 0:
                        if (current_x, current_y) in D:
                            return False # Failed
                    return True
                    
                # choice 0
                if not check_sums(idx + 1, current_x, current_y, num_nonzero):
                    return False
                # choice 1
                if not check_sums(idx + 1, current_x + comb[idx][0], current_y + comb[idx][1], num_nonzero + 1):
                    return False
                # choice -1
                if not check_sums(idx + 1, current_x - comb[idx][0], current_y - comb[idx][1], num_nonzero + 1):
                    return False
                    
                return True
                
            if check_sums(0, 0, 0, 0):
                print(f"FOUND PERFECT SET! R^2={r2} with vectors {comb}")
                # let's verify size 512
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
                    print(f"CONFIRMED SIZE 512 for R^2={r2}")
                    return r2
    return None

if __name__ == '__main__':
    solve()
