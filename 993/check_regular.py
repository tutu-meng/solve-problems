def rref_mod(matrix, p=1000000007):
    if not matrix: return 0
    rows = len(matrix)
    cols = len(matrix[0])
    r = 0
    for c in range(cols):
        pivot = r
        while pivot < rows and matrix[pivot][c] % p == 0:
            pivot += 1
        if pivot == rows:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        
        inv = pow(matrix[r][c], p - 2, p)
        for j in range(c, cols):
            matrix[r][j] = (matrix[r][j] * inv) % p
            
        for i in range(rows):
            if i != r and matrix[i][c] % p != 0:
                factor = matrix[i][c]
                for j in range(c, cols):
                    matrix[i][j] = (matrix[i][j] - factor * matrix[r][j]) % p
        r += 1
    return r

def check_k_regular(k, V, max_e, L):
    if len(V) < k**max_e * L:
        return
        
    subseqs = []
    subseqs.append([1] * L)
    subseqs.append([n for n in range(L)])
    
    for e in range(1, max_e+1):
        for a in range(k**e):
            sub = [V[k**e * n + a] for n in range(L)]
            subseqs.append(sub)
            
    rank = rref_mod([row[:] for row in subseqs])
    print(f"k={k}, max_e={max_e}, L={L}: rank={rank}, num_vectors={len(subseqs)}")

lines = open('bb_values.txt').read().splitlines()
V = [int(l.split()[1]) for l in lines if l.strip()]

for e in range(1, 8):
    check_k_regular(2, V, e, 500)
