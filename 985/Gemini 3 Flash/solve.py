import sys

def check_triangle(a, b, c, k_target):
    if a + b <= c or a + c <= b or b + c <= a:
        return False
        
    c0 = (b*b + c*c - a*a) / (2.0 * b * c)
    d0 = (a*a + c*c - b*b) / (2.0 * a * c)
    e0 = (a*a + b*b - c*c) / (2.0 * a * b)
    
    if c0 <= 0 or d0 <= 0 or e0 <= 0:
        return False
        
    curr_c, curr_d, curr_e = c0, d0, e0
    for _ in range(1, k_target):
        # T_j is acute
        curr_c = 1.0 - 2.0 * curr_c * curr_c
        curr_d = 1.0 - 2.0 * curr_d * curr_d
        curr_e = 1.0 - 2.0 * curr_e * curr_e
        if curr_c <= 0 or curr_d <= 0 or curr_e <= 0:
            return False
            
    # T_k_target exists and is NOT acute
    curr_c = 1.0 - 2.0 * curr_c * curr_c
    curr_d = 1.0 - 2.0 * curr_d * curr_d
    curr_e = 1.0 - 2.0 * curr_e * curr_e
    if curr_c <= 0 or curr_d <= 0 or curr_e <= 0:
        return True
    return False

def get_candidate_triangles(p):
    n = p // 3
    rem = p % 3
    if rem == 0:
        if n >= 2: yield (n-1, n, n+1)
    elif rem == 1:
        if n >= 1: yield (n, n, n+1)
    elif rem == 2:
        if n >= 1: yield (n, n+1, n+1)

def find_smallest(k_target, start_p=3):
    p = start_p
    while True:
        for a, b, c in get_candidate_triangles(p):
            if check_triangle(a, b, c, k_target):
                return p, (a, b, c)
        p += 1
        if p % 1000000 == 0:
            print(f"Checked up to P={p}", file=sys.stderr)

if __name__ == "__main__":
    # Regression
    print(f"Smallest P for k=2: {find_smallest(2)}")
    # Target (checking from P=1)
    print(f"Smallest P for k=20: {find_smallest(20, 1)}")
