import sys

def check_triangle(a, b, c, k_target):
    """
    Checks if T_k exists for k=1..k_target but not for k_target+1.
    T_k exists iff T_{k-1} is acute.
    """
    # cos A, cos B, cos C
    # We use floats but need to be careful with precision.
    # Standard 64-bit float has ~16 digits.
    # We multiply error by ~2 each step. 2^20 ~ 10^6.
    # 10^-16 * 10^6 = 10^-10. Still very good.
    
    # Pre-check triangle inequality
    if a + b <= c or a + c <= b or b + c <= a:
        return False
        
    c0 = (b*b + c*c - a*a) / (2.0 * b * c)
    d0 = (a*a + c*c - b*b) / (2.0 * a * c)
    e0 = (a*a + b*b - c*c) / (2.0 * a * b)
    
    # T_1 exists if T_0 is acute
    if c0 <= 0 or d0 <= 0 or e0 <= 0:
        return False
        
    curr_c, curr_d, curr_e = c0, d0, e0
    
    for j in range(1, k_target):
        # T_j is acute? If so, T_{j+1} exists.
        # Next cosines
        curr_c = 1.0 - 2.0 * curr_c * curr_c
        curr_d = 1.0 - 2.0 * curr_d * curr_d
        curr_e = 1.0 - 2.0 * curr_e * curr_e
        
        if curr_c <= 0 or curr_d <= 0 or curr_e <= 0:
            return False # T_j is not acute, so T_{j+1} does not exist.
            
    # If we are here, T_1..T_{k_target} exist and T_{k_target-1} was acute.
    # Now check if T_{k_target} exists AND is obtuse.
    # "T_{k_target} exists" is guaranteed if T_{k_target-1} is acute.
    # We need T_{k_target+1} to NOT exist, which means T_{k_target} must be NOT acute.
    
    # Calculate T_{k_target} cosines
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
        # P = 3n. Most equilateral is (n, n, n), but that always exists.
        # Next is (n-1, n, n+1).
        if n >= 2:
            yield (n-1, n, n+1)
        # Also maybe (n-1, n-1, n+2)? No, deviation is larger.
    elif rem == 1:
        # P = 3n + 1. Most equilateral is (n, n, n+1).
        if n >= 1:
            yield (n, n, n+1)
    elif rem == 2:
        # P = 3n + 2. Most equilateral is (n, n+1, n+1).
        if n >= 1:
            yield (n, n+1, n+1)

def find_smallest(k_target):
    p = 3
    # Start searching. For large k, we can optimize the starting P.
    # But for a quick check, let's just run.
    # Optimization: for k=20, P is at least 10^6.
    if k_target > 5:
        p = 1000000
        
    while True:
        for a, b, c in get_candidate_triangles(p):
            if check_triangle(a, b, c, k_target):
                return p, (a, b, c)
        p += 1
        if p % 100000 == 0:
            print(f"Checked up to P={p}", file=sys.stderr)

if __name__ == "__main__":
    # Regression test
    print(f"Smallest P for k=2: {find_smallest(2)}")
    
    # Target k=20
    print(f"Smallest P for k=20: {find_smallest(20)}")
