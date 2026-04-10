x, y = 2, 1
total_perimeter = 0
limit = 1000000000

while True:
    nx = 2 * x + 3 * y
    ny = x + 2 * y
    x, y = nx, ny
    
    handled = False
    if (x + 2) % 3 == 0:
        c = (x + 2) // 3
        if c > 0:
            a = 2 * c - 1
            if a > 0 and 2 * a > 2 * c:
                p = 6 * c - 2
                if p <= limit:
                    total_perimeter += p
                    handled = True
                else:
                    break

    if not handled and (x - 2) % 3 == 0:
        c = (x - 2) // 3
        if c > 0:
            a = 2 * c + 1
            if a > 0 and 2 * a > 2 * c:
                p = 6 * c + 2
                if p <= limit:
                    total_perimeter += p
                else:
                    break

print(total_perimeter)
