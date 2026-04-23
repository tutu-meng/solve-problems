import subprocess
P = 1000000007
proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
g = {}
exec(proc.stdout, g)
M0, M1, F0 = g['M0'], g['M1'], g['F0']

def mult(M, V):
    res = [0] * len(V)
    for i in range(len(M)):
        res[i] = sum(M[i][j] * V[j] for j in range(len(V))) % P
    return res

print("F0[1] =", F0[1])

bits = bin(13)[2:]
res = list(F0)
for b in bits:
    res = mult(M1 if b == '1' else M0, res)

print("BB(13) calculated:", res[1])
print("BB(13) expected: 11")

bits = bin(1000)[2:]
res = list(F0)
for b in bits:
    res = mult(M1 if b == '1' else M0, res)

print("BB(1000) calculated:", res[1])
print("BB(1000) expected: 1499")

bits = bin(10000)[2:]
res = list(F0)
for b in bits:
    res = mult(M1 if b == '1' else M0, res)

print("BB(10000) calculated:", res[1])
