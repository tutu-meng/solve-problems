import sys

lines = open('bb_values.txt').read().splitlines()
bbs = {}
for line in lines:
    if line.strip():
        parts = line.split()
        if len(parts) >= 2:
            try:
                bbs[int(parts[0])] = int(parts[1])
            except:
                pass

N_vals = sorted(bbs.keys())
V = [bbs[n] for n in N_vals]

print(f"Loaded {len(V)} values.")

def find_period(seq, min_p, max_p):
    for p in range(min_p, max_p+1):
        # check if sequence ultimately becomes periodic with period p
        # differences seq[i+p] - seq[i] should be constant
        valid = False
        for start in range(len(seq) - 200*p):
            # Try to see if it becomes constant after `start`
            constant = True
            diff = seq[start+p] - seq[start]
            for i in range(start, len(seq) - p):
                if seq[i+p] - seq[i] != diff:
                    constant = False
                    break
            if constant:
                print(f"Found period P={p}, shift={start}, diff={diff}")
                return p, start, diff
    return None

find_period(V, 1, 1000)
