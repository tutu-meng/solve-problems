def build_linear_representation(V):
    # Determine the basis from subsequences V[2^e n + a]
    L = 500
    p = 1000000007 # We can use modulo arithmetic to find the basis index
    
    # We will compute things exactly later, but first find basis indices using mod p
    # Store subsequences
    seqs = []
    # seq_info = (e, a)
    seq_info = []
    
    # To handle V[N]+2N type affine stuff, include 1 and n. 
    # But since BB(N) is k-regular we can just use 1 and V itself.
    # Wait, the definition of 2-regular includes affine terms if we include them. 
    # Let's just use pure subsequences V[2^e n + a], it's enough because it spanned rank 119.
    
    # Actually, we should include the sequence [1, 1, 1...] to handle constants if it helps.
    # Wait, V[2^e n + a] itself is a subspace.
    
    # We need to find exactly rank=119 vectors.
    max_e = 7
    rank = 0
    basis_indices = []
    
    matrix = []
    
    # helper for rref to check if vector is independent
    current_basis_rows = []
    
    def is_independent(vec):
        # check if vec is independent of current_basis_rows mod p
        # just copy current_basis_rows, append vec, and do row reduction
        mat = [row[:] for row in current_basis_rows]
        mat.append(vec[:])
        
        rows = len(mat)
        cols = len(mat[0])
        r = 0
        for c in range(cols):
            pivot = r
            while pivot < rows and mat[pivot][c] % p == 0:
                pivot += 1
            if pivot == rows:
                continue
            mat[r], mat[pivot] = mat[pivot], mat[r]
            inv = pow(mat[r][c], p - 2, p)
            for j in range(c, cols):
                mat[r][j] = (mat[r][j] * inv) % p
            for i in range(rows):
                if i != r and mat[i][c] % p != 0:
                    factor = mat[i][c]
                    for j in range(c, cols):
                        mat[i][j] = (mat[i][j] - factor * mat[r][j]) % p
            r += 1
        return r > len(current_basis_rows)

    idx_to_info = {}
    cnt = 0
    
    for e in range(0, max_e + 1):
        for a in range(2**e):
            sub = [V[2**e * n + a] for n in range(L)]
            
            if is_independent(sub):
                current_basis_rows.append(sub)
                basis_indices.append(cnt)
            
            seqs.append(sub)
            seq_info.append((e, a))
            cnt += 1

    print(f"Found rank {len(basis_indices)}")
    
    # Now we need to express the "target" vectors in terms of the basis EXACTLY.
    # The targets are F_i(2n) and F_i(2n+1).
    # F_i(2n) = V[2^{e_i+1} n + a_i] -> which is exactly a vector in our set with e=e_i+1, a=a_i
    # F_i(2n+1) = V[2^{e_i+1} n + a_i + 2^{e_i}] -> an exact vector in our set with e=e_i+1, a=a_i + 2^{e_i}
    
    # We can express them by solving the linear system USING RATIONALS OR INTEGERS.
    # Luckily, all entries in our vectors are integers, and we just need exact integer or rational coefficients.
    return len(basis_indices)

lines = open('bb_values.txt').read().splitlines()
V = [int(l.split()[1]) for l in lines if l.strip()]
build_linear_representation(V)
