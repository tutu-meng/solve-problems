import subprocess

primes = [1000000007, 1000000009, 1000000021]
rems = []

def mult(M, V, P):
    res = [0] * len(V)
    for i in range(len(M)):
        val = 0
        for j in range(len(V)):
            val = (val + M[i][j] * V[j]) % P
        res[i] = val
    return res

# Function to compute modular inverse
def modInverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

# Chinese Remainder Theorem
def findMinX(num, rem, k):
    prod = 1
    for i in range(0, k):
        prod = prod * num[i]
    result = 0
    for i in range(0, k):
        pp = prod // num[i]
        result = result + rem[i] * modInverse(pp, num[i]) * pp
    return result % prod, prod

for P in primes:
    proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
    out = proc.stdout
    g = {}
    exec(out, g)
    M0 = g['M0']
    M1 = g['M1']
    F0 = g['F0']
    
    # Check 10**18
    N = 10**18
    bits = bin(N)[2:]
    
    res = list(F0)
    for b in bits:
        if b == '0':
            res = mult(M0, res, P)
        else:
            res = mult(M1, res, P)
            
    rems.append(res[1])

print("Remainders:", rems)
ans, limit = findMinX(primes, rems, 3)

if ans > limit // 2:
    ans -= limit
    
print(f"BB(10**18) = {ans}")

# Let's also verify 1000 and 10000 to be absolutely sure
for test_N in [1000, 10000]:
    test_rems = []
    for P in primes:
        proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
        g = {}
        exec(proc.stdout, g)
        M0 = g['M0']
        M1 = g['M1']
        F0 = g['F0']
        res = list(F0)
        for b in bin(test_N)[2:]:
            if b == '0': res = mult(M0, res, P)
            else: res = mult(M1, res, P)
        test_rems.append(res[1])
    test_ans, _ = findMinX(primes, test_rems, 3)
    if test_ans > limit // 2: test_ans -= limit
    print(f"BB({test_N}) = {test_ans}")

