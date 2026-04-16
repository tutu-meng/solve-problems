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

def check_perfect(r2):
    base_pts = get_circle_points(r2)
    k = len(base_pts) // 2
    if k < 2: return
    
    # Let's use the property that points must sum to 0 mod 2.
    # To find ALL perfect sets for small r2, we can just do BFS with small limit.
    print(f"R^2 = {r2}, {len(base_pts)} points")

for r2 in range(1, 26):
    check_perfect(r2)
