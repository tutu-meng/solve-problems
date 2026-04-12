def find_solutions(limit):
    total = 0
    # S = x + z
    # Since z is on the order of 4d, and x is on the order of 4z-d ~ 15d
    # We can iterate over d first. But limit is S <= 10^7.
    # z could be up to 10^7.
    # Better to iterate over z?
    # d | z^2. Since we need z/d in certain ratios, let's iterate z.
    for z in range(1, limit):
        # We need d | z^2 such that d < z/3.732 approx, and d > z/4.791
        # or d > z/0.2679 approx and d < z/0.2087
        pass
    
    return total

def brute(limit):
    s_sum = 0
    for z in range(2, limit):
        for d in range(1, int(z / 0.2) + 1):
            if z * z % d == 0:
                y_num = z*z - 4*z*d + d*d
                b_num = -z*z + 5*z*d - d*d
                if y_num >= d and b_num >= d:
                    x = 4*z - d
                    y = y_num // d
                    b = b_num // d
                    s = x + z
                    if s <= limit:
                        #print(f"z={z}, d={d}, x={x}, b={b}, y={y}, S={s}")
                        s_sum += s
    return s_sum

print(brute(1000))
