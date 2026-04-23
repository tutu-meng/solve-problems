import subprocess
P = 1000000007
proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
g = {}
exec(proc.stdout, g)
M0, M1, F0 = g['M0'], g['M1'], g['F0']

def mult(M, V):
    return [(sum(M[i][j] * V[j] for j in range(len(V))) % P) for i in range(len(M))]

# F0 is V at n=0. Since V[m] = S_m, F0[1] = V[0] = S_0.
# My basis has e=0, a=0, which means F(n) = V[n].
# So F(n)[1] = V[n].
# To get BB(N), we need V[N-1] if V[n] = BB(n+1).
# Wait, did V contain BB(0)?
with open('bb_values.txt') as f:
    lines = f.readlines()[:10]
    for l in lines: print(l.strip())

