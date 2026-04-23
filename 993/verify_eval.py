import importlib.util
import os

# Load exactly to use Fractions
spec = importlib.util.spec_from_file_location("exact_eval", "exact_eval.py")
eval_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eval_mod)

M0 = eval_mod.M0
M1 = eval_mod.M1
F0 = eval_mod.F0

def mult(M, V):
    res = [0] * len(V)
    for i in range(len(M)):
        for j in range(len(V)):
            res[i] += M[i][j] * V[j]
    return res

def compute_F(N):
    if N == 0:
        return [eval(str(x)) if type(x) == str else x for x in F0]
    
    bits = bin(N)[2:]
    # reverse because bits are evaluated from MSB?
    # F(2n) = M0 F(n) -> N = 2n + b -> F(N) = M_b F(n)
    # Thus, if n = N // 2, b = N % 2.
    # We apply M_b on F(N//2).
    # So F(N) = M_{b[0]} M_{b[1]} ... F(0) where b[0] is LSB!
    
    # Wait, let's trace: F(13) = M_1 F(6) = M_1 M_0 F(3) = M_1 M_0 M_1 F(1) = M_1 M_0 M_1 M_1 F(0)
    # So we mult by M_1, then M_1, then M_0, then M_1, from F(0).
    # bits = "1101" -> msb to lsb is 1, 1, 0, 1.
    # LSB is 1, next 0, next 1, next 1.
    # sequence of multipliers is M_{msb}... M_{lsb}? No.
    # F(13) = M1( F(6) ) = M1( M0( F(3) ) ) = M1( M0( M1( F(1) ) ) ) = M1( M0( M1( M1( F(0) ) ) ) ).
    # So F0 -> apply M_msb -> apply M_... -> apply M_lsb.
    # So we process bits from MSB to LSB.
    res = [eval(str(x)) if type(x) == str else x for x in F0]
    for b in bits:
        if b == '0':
            res = mult(M0, res)
        else:
            res = mult(M1, res)
    return res

V = compute_F(1000)
# Basis element 1 starts as the identity sequence?
# Wait, F0[1] is BB(2^0 * 0 + 0) = BB(0).
# actually the index of BB(n) is the one with e=0, a=0.
# In our basis, e=-1, a=-1 is index 0. This is the 1s sequence.
# e=0, a=0 is index 1. This is BB(n).
print("Computed BB(1000) =", V[1])

print("Computed BB(10000) =", compute_F(10000)[1])
print("Computed BB(16384) =", compute_F(16384)[1])

# Now compute 10**18
ans = compute_F(10**18)[1]
print(f"Computed BB(10**18) = {ans}")
