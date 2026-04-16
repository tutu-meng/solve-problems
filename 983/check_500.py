import itertools
from debug_625 import get_circle_points

def check_500():
    r2 = 625
    pts = get_circle_points(r2)
    for u in pts:
        for v in pts:
            if u != v:
                dist2 = (u[0]-v[0])**2 + (u[1]-v[1])**2
                if dist2 == 500:
                    print(f"u={u}, v={v}, dot={u[0]*v[0] + u[1]*v[1]}")
                    return

check_500()
