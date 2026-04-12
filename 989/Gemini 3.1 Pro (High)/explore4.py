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

F = build_fib(200)

ans = 0
print("n \t F_n \t G_n \t Fn*Gn")
for i in range(1, 201):
    f_g = (F[i] * get_G(i)) % M
    if f_g != 0:
        print(f"{i} \t {F[i]} \t {get_G(i)} \t {f_g}")
