import importlib.util
import math

class FastFraction:
    def __init__(self, num, den=1):
        self.num = num
        self.den = den

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

spec = importlib.util.spec_from_file_location("exact_eval", "exact_eval.py")
eval_mod = importlib.util.module_from_spec(spec)
eval_mod.Fraction = FastFraction
# Override F
def F(n, d=1):
    return FastFraction(n, d)
eval_mod.F = F
spec.loader.exec_module(eval_mod)

def convert_matrix(M_ff):
    # Find common denominator
    den = 1
    for row in M_ff:
        for x in row:
            if isinstance(x, FastFraction):
                den = lcm(den, x.den)
    
    # Convert to integers
    M_int = []
    for row in M_ff:
        M_int.append([(x.num * (den // x.den)) if isinstance(x, FastFraction) else x * den for x in row])
    return M_int, den

M0_int, D0 = convert_matrix(eval_mod.M0)
M1_int, D1 = convert_matrix(eval_mod.M1)

F0 = []
for x in eval_mod.F0:
    if isinstance(x, str): F0.append(int(x))
    elif isinstance(x, FastFraction): F0.append(x.num // x.den)
    else: F0.append(x)

def mult(M_int, D, V):
    res = [0] * len(V)
    for i in range(len(M_int)):
        for j in range(len(V)):
            res[i] += M_int[i][j] * V[j]
        assert res[i] % D == 0
        res[i] //= D
    return res

def compute_F(N):
    if N == 0:
        return list(F0)
    
    bits = bin(N)[2:]
    res = list(F0)
    for b in bits:
        if b == '0':
            res = mult(M0_int, D0, res)
        else:
            res = mult(M1_int, D1, res)
    return res

print(f"BB(1000) = {compute_F(1000)[1]}")
print(f"BB(10000) = {compute_F(10000)[1]}")
print(f"BB(50000) = {compute_F(50000)[1]}")
ans = compute_F(10**18)[1]
print(f"BB(10**18) = {ans}")
