from exact_eval import M0, M1, F0, Fraction

def mult(M, V):
    res = [Fraction(0, 1)] * len(V)
    for i in range(len(M)):
        for j in range(len(V)):
            if M[i][j] != 0 and V[j] != 0:
                res[i] += M[i][j] * V[j]
    return res

def compute_F(N):
    res = [Fraction(int(x)) for x in F0]
    if N == 0:
        return res
    
    bits = bin(N)[2:]
    for b in bits:
        if b == '0':
            res = mult(M0, res)
        else:
            res = mult(M1, res)
    return res

import time
t0 = time.time()
v_1000 = compute_F(1000)
print(f"BB(1000) = {v_1000[1].numerator}, time: {time.time()-t0:.2f}s")
v_10000 = compute_F(10000)
print(f"BB(10000) = {v_10000[1].numerator}")
v_50000 = compute_F(50000)
print(f"BB(50000) = {v_50000[1].numerator}")
ans = compute_F(10**18)
print(f"BB(10**18) = {ans[1].numerator}")
