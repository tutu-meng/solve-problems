def solve():
    MOD = 10**9 + 7

    def poly_mul(A, B, P):
        d = len(P) - 1
        res = [0] * (2 * d)
        for i in range(len(A)):
            for j in range(len(B)):
                res[i + j] = (res[i + j] + A[i] * B[j]) % MOD
                
        for i in range(2 * d - 1, d - 1, -1):
            if res[i] == 0:
                continue
            coeff = res[i]
            for j in range(d):
                res[i - d + j] = (res[i - d + j] - coeff * P[j]) % MOD
        return res[:d]

    def poly_pow(A, p, P):
        d = len(P) - 1
        res = [1] + [0] * (d - 1)
        base = A[:]
        while p > 0:
            if p % 2 == 1:
                res = poly_mul(res, base, P)
            base = poly_mul(base, base, P)
            p //= 2
        return res

    # The recurrence coefficients (C) and the base cases (f)
    # The degree is 11.
    C = [1, 1000000000, 19, 999999986, 1000000001, 42, 999999965, 6, 21, 999999988, 7, 1000000006]
    base_cases = [92, 903, 4411, 14959, 41083, 98200, 212418, 425756, 803074, 1441065, 2479669]
    d = len(C) - 1

    P = [0] * (d + 1)
    for j in range(d + 1):
        P[d - j] = C[j]

    def get_f(N_target):
        base_idx = 4
        k = N_target - base_idx
        A = [0, 1] + [0] * (d - 2) if d > 1 else [0]
        res_poly = poly_pow(A, k, P)
        
        ans = 0
        for i in range(d):
            ans = (ans + res_poly[i] * base_cases[i]) % MOD
        return ans

    return get_f(10**18)

if __name__ == "__main__":
    print(solve())
