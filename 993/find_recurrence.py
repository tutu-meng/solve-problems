def solve():
    lines = open('bb_values.txt').read().splitlines()
    V = [int(l.split()[1]) for l in lines if l.strip()][:10000]

    for m in range(2, 5):
        for k in range(m):
            # Try to find a, b, c such that V[m*n + k] = a * V[n] + b * n + c
            # We can pick n=10, 11, 12 to solve for a, b, c.
            # Then check if it holds for all n.
            n1, n2, n3 = 100, 101, 102
            # but wait, maybe b is a fraction? Let's just try integer a
            for a in range(-5, 6):
                # V[m*n+k] - a*V[n] = b*n + c
                # So difference should be constant b
                diffs = [V[m*n+k] - a*V[n] for n in range(10, 1000)]
                # check if diffs[i+1] - diffs[i] is constant
                b_set = set(diffs[i+1] - diffs[i] for i in range(len(diffs)-1))
                if len(b_set) == 1:
                    b = b_set.pop()
                    c = diffs[0] - b * 10
                    print(f"Found: BB({m}N + {k}) = {a} BB(N) + {b} N + {c}")

            # Also check if V[m*n+k] relates to V[n] through some other simple m multiplier
            # Maybe V[2N] vs V[N]
solve()
