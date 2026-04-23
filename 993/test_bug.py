import subprocess
P = 1000000007
proc = subprocess.run(['./build_matrix_crt', str(P)], capture_output=True, text=True)
g = {}
exec(proc.stdout, g)
M0, F0 = g['M0'], g['F0']

print("M0[64] =", M0[64])
print("F0[64] =", F0[64])
