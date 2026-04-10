from itertools import combinations, permutations, product
from fractions import Fraction

def solve():
    ops = [
        lambda x, y: x + y,
        lambda x, y: x - y,
        lambda x, y: x * y,
        lambda x, y: x / y if y != 0 else None
    ]

    def get_results(abcd):
        results = set()
        for p in permutations(abcd):
            p = [Fraction(x) for x in p]
            for op1, op2, op3 in product(range(4), repeat=3):
                # Parents schemas
                # ((a op1 b) op2 c) op3 d
                try:
                    v = ops[op1](p[0], p[1])
                    if v is not None:
                        v = ops[op2](v, p[2])
                        if v is not None:
                            v = ops[op3](v, p[3])
                            if v is not None and v > 0 and v.denominator == 1:
                                results.add(int(v))
                except ZeroDivisionError:
                    pass

                # (a op1 (b op2 c)) op3 d
                try:
                    v_inner = ops[op2](p[1], p[2])
                    if v_inner is not None:
                        v = ops[op1](p[0], v_inner)
                        if v is not None:
                            v = ops[op3](v, p[3])
                            if v is not None and v > 0 and v.denominator == 1:
                                results.add(int(v))
                except ZeroDivisionError:
                    pass

                # a op1 ((b op2 c) op3 d)
                try:
                    v_inner = ops[op2](p[1], p[2])
                    if v_inner is not None:
                        v_outer = ops[op3](v_inner, p[3])
                        if v_outer is not None:
                            v = ops[op1](p[0], v_outer)
                            if v is not None and v > 0 and v.denominator == 1:
                                results.add(int(v))
                except ZeroDivisionError:
                    pass

                # a op1 (b op2 (c op3 d))
                try:
                    v_inner = ops[op3](p[2], p[3])
                    if v_inner is not None:
                        v_outer = ops[op2](p[1], v_inner)
                        if v_outer is not None:
                            v = ops[op1](p[0], v_outer)
                            if v is not None and v > 0 and v.denominator == 1:
                                results.add(int(v))
                except ZeroDivisionError:
                    pass

                # (a op1 b) op2 (c op3 d)
                try:
                    v1 = ops[op1](p[0], p[1])
                    v2 = ops[op3](p[2], p[3])
                    if v1 is not None and v2 is not None:
                        v = ops[op2](v1, v2)
                        if v is not None and v > 0 and v.denominator == 1:
                            results.add(int(v))
                except ZeroDivisionError:
                    pass
        return results

    best_n = 0
    best_set = ""

    for abcd in combinations(range(10), 4):
        target_results = get_results(abcd)
        n = 0
        while n + 1 in target_results:
            n += 1
        
        if n > best_n:
            best_n = n
            best_set = "".join(map(str, sorted(abcd)))
    
    return best_set

if __name__ == "__main__":
    print(solve())
