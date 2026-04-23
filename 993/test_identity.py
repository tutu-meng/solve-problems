import subprocess
P = 1000000007
proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
g = {}
exec(proc.stdout, g)
M0, F0 = g['M0'], g['F0']

def mult(M, V):
    return [(sum(M[i][j] * V[j] for j in range(len(V))) % P) for i in range(len(M))]

res = mult(M0, F0)
for i in range(len(F0)):
    if res[i] != F0[i]:
        print(f"Mismatch at basis {i}: res={res[i]}, F0={F0[i]}")

