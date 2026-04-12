import math

def path_count(R_list, L_list, E, n, k):
    ways = 1
    # Node 0 has no choices, only R exits. Wait, if E == 0, total exits = R_0. We choose R_0. (Comb(R_0, R_0) = 1).
    for i in range(1, n):
        R = R_list[i]
        L = L_list[i]
        
        if i < E:
            # last exit right
            ways *= math.comb(R + L - 1, R - 1)
        elif i > E:
            # last exit left
            ways *= math.comb(R + L - 1, R)
        else: # i == E
            ways *= math.comb(R + L, R)
            
    return ways

def J_math(n, k):
    total = 0
    for E in range(n + 1):
        R = [0] * (n + 1)
        L = [0] * (n + 1)
        
        possible = True
        R[0] = k - 1 if E == 0 else k
        if R[0] < 0:
            continue
            
        for i in range(1, n):
            L[i] = R[i-1] - 1 if i <= E else R[i-1]
            if L[i] < 0:
                possible = False; break
                
            req_R = (k + i) - L[i] - (1 if E == i else 0)
            if req_R < 0:
                possible = False; break
            R[i] = req_R
        
        if not possible:
            continue
            
        ways = path_count(R, L, E, n, k)
        total += ways
    return total

print("J(2, 1) =", J_math(2, 1))
print("J(3, 2) =", J_math(3, 2))
print("J(6, 1) =", J_math(6, 1))
print("J(6, 5) =", J_math(6, 5))
