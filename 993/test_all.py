import subprocess
P = 1000000007
proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
g = {}
exec(proc.stdout, g)
M0, M1, F0 = g['M0'], g['M1'], g['F0']

def mult(M, V):
    return [(sum(M[i][j] * V[j] for j in range(len(V))) % P) for i in range(len(M))]

lines = open('bb_values.txt').read().splitlines()
V = [int(l.split()[1]) for l in lines if l.strip()]

fail = -1
for N in range(0, 10000):
    if N == 0:
        ans = F0[1]
    else:
        bits = bin(N)[2:]
        res = list(F0)
        for b in bits:
            res = mult(M1 if b == '1' else M0, res)
        ans = res[1]
    if (ans % P) != (V[N] % P):
        print(f"Failed at N={N}, calculated={ans}, expected={V[N]}")
        fail = N
        break
if fail == -1: 
    print("All match up to 10000!!!")
