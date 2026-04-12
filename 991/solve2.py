def solve2(limit):
    s_sum = 0
    # To cover S <= 10^7 in the first interval, y ~ 0.25d, S = 5y-d ~ 0.25d.
    # So d <= 4 * 10^7.
    import math
    for d in range(1, 40000): # test small range
        # interval 1
        y_min1 = math.ceil((5*d - math.sqrt(21*d*d - 4*d)) / 2)
        y_max1 = math.floor((4*d - math.sqrt(12*d*d + 4*d)) / 2)
        
        # interval 2
        y_min2 = math.ceil((4*d + math.sqrt(12*d*d + 4*d)) / 2)
        y_max2 = math.floor((5*d + math.sqrt(21*d*d - 4*d)) / 2)
        
        for y in range(max(1, y_min1), y_max1 + 1):
            if (y * y) % d == 0:
                s = 5 * y - d
                if s <= limit:
                    s_sum += s
        
        for y in range(y_min2, y_max2 + 1):
            if (y * y) % d == 0:
                s = 5 * y - d
                if s <= limit:
                    s_sum += s
                    
    return s_sum

print(solve2(1000))
