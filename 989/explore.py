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

F = build_fib(100)
G = [0] + [get_G(n) for n in range(1, 101)]

for i in range(1, 20):
    print(f"n={i}, F_n={F[i]}, G_n={G[i]}, F_n G_n = {(F[i]*G[i])%M}")
    
# Let's check n up to 10^3
ans = 0
for i in range(1, 1001):
    f = F[i] if i < len(F) else 0
    if i >= len(F):
        # build more
        while len(F) <= i:
            F.append((F[-1] + F[-2]) % M)
        f = F[i]
    ans = (ans + f * get_G(i)) % M
print(f"Sum up to 10^3 = {ans}")
