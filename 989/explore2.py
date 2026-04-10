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

F = build_fib(2000)

ans = 0
for i in range(1, 2001):
    ans = (ans + F[i] * get_G(i)) % M
    if i in [10, 100, 1000, 2000]:
        print(f"Sum up to {i} = {ans}")
