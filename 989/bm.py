M = 10**9 + 9

def build_fib(lim):
    F = [0, 1, 1]
    for _ in range(3, lim+1):
        F.append((F[-1] + F[-2]) % M)
    return F

def get_G(n):
    c = 0
    for x in range(n):
        if (x*x - x - 1) % n == 0:
            c += 1
    return c

F = build_fib(500)

S = [0]
for i in range(1, 500):
    S.append((S[-1] + F[i] * get_G(i)) % M)

def berlekamp_massey(s):
    n = len(s)
    C = [1]
    B = [1]
    L = 0
    m = 1
    b = 1
    for i in range(n):
        d = 0
        for j in range(L + 1):
            d = (d + C[j] * s[i - j]) % M
        if d == 0:
            m += 1
        else:
            T = C[:]
            # c -= d/b * x^m * B
            c_factor = (d * pow(b, M-2, M)) % M
            while len(C) <= len(B) + m:
                C.append(0)
            for j in range(len(B)):
                C[j + m] = (C[j + m] - c_factor * B[j]) % M
            if 2 * L <= i:
                L = i + 1 - L
                B = T
                b = d
                m = 1
            else:
                m += 1
    return C

recurrence = berlekamp_massey(S[1:])
print(f"Recurrence length: {len(recurrence) - 1}")
