def jacobi(a, n):
    assert(n > 0 and n % 2 == 1)
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    else:
        return 0

def h(n):
    # n = 5^k * m
    k = 0
    m = n
    while m % 5 == 0:
        k += 1
        m //= 5
    if k == 1 or k > 2:
        return 0
    
    # check if m is square-free
    import math
    is_sq_free = True
    for i in range(2, int(math.sqrt(m)) + 2):
        if m % (i*i) == 0:
            return 0
            
    val = jacobi(m, 5) if m % 2 != 0 else (1 if m % 5 in (1,4) else -1)
    # wait jacobi is usually for odd n, but modulo 5 it's just (m|5) which is legendary symbol.
    val = 1 if m % 5 in (1, 4) else (-1 if m % 5 in (2, 3) else 0)
    
    # wait if m has multiple prime factors, (m|5) = product of (p|5).
    # Since legendre symbol is multiplicative, (m|5) = prod (p_i | 5). Yes!
    # So val = Legendre(m, 5).
    
    v = 1 if m % 5 in (1, 4) else (-1 if m%5 in (2, 3) else 0)
    if m == 1: v = 1
    
    if k == 2:
        return -v
    else:
        return v

def get_G_formula(n):
    res = 0
    for d in range(1, n+1):
        if n % d == 0:
            res += h(d)
    return res

def get_G(n):
    c = 0
    for x in range(n):
        if (x*x - x - 1) % n == 0:
            c += 1
    return c

good = True
for i in range(1, 1000):
    if get_G_formula(i) != get_G(i):
        print(f"Failed for {i}: formula={get_G_formula(i)}, actual={get_G(i)}")
        good = False
if good:
    print("Formula is PERFECT!")
