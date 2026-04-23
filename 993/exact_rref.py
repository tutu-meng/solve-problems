import sys
from fractions import Fraction

def compute_exact():
    lines = open('bb_values.txt').read().splitlines()
    V = [int(l.split()[1]) for l in lines if l.strip()]

    L = 300 # reduced L to speed up fractions
    max_e = 7
    k = 2
    
    seqs = []
    seq_info = []
    
    seqs.append([Fraction(1)] * L)
    seq_info.append((-1, -1))
    
    for e in range(0, max_e + 1):
        for a in range(2**e):
            sub = [Fraction(V[(1<<e)*n + a]) for n in range(L)]
            seqs.append(sub)
            seq_info.append((e, a))
            
    num_seqs = len(seqs)
    basis = []
    row_reduced = []
    basis_orig = []
    relations = [None] * num_seqs
    
    print("Starting exact RREF...")
    
    for i in range(num_seqs):
        cur = seqs[i][:]
        coeffs = [Fraction(0)] * len(basis)
        
        is_indep = False
        
        for j in range(len(basis)):
            pivot = -1
            for c in range(L):
                if row_reduced[j][c] != 0:
                    pivot = c
                    break
            
            if pivot != -1 and cur[pivot] != 0:
                factor = cur[pivot] / row_reduced[j][pivot]
                coeffs[j] = factor
                for c in range(pivot, L):
                    cur[c] -= factor * row_reduced[j][c]
                    
        for c in range(L):
            if cur[c] != 0:
                is_indep = True
                break
                
        if is_indep:
            basis.append(i)
            row_reduced.append(cur)
            basis_orig.append(seqs[i])
            self_rel = [Fraction(0)] * len(basis)
            self_rel[-1] = Fraction(1)
            relations[i] = self_rel
            
            # optionally, pad old relations to new basis size
            for r in range(i):
                if relations[r] is not None:
                    relations[r].append(Fraction(0))
        else:
            relations[i] = coeffs
            
        if (i+1) % 50 == 0:
            print(f"Processed {i+1}/{num_seqs}, rank {len(basis)}")

    d = len(basis)
    print(f"Rank: {d}")
    
    M0 = [[Fraction(0)]*d for _ in range(d)]
    M1 = [[Fraction(0)]*d for _ in range(d)]
    
    for i in range(d):
        idx = basis[i]
        e, a = seq_info[idx]
        
        if e == -1:
            M0[i][0] = Fraction(1)
            M1[i][0] = Fraction(1)
            continue
            
        idx0, idx1 = -1, -1
        for j in range(num_seqs):
            if seq_info[j] == (e+1, a): idx0 = j
            if seq_info[j] == (e+1, a + 2**e): idx1 = j
            
        M0[i] = relations[idx0]
        M1[i] = relations[idx1]
        
    # Write to a file
    with open('exact_eval.py', 'w') as f:
        f.write("from fractions import Fraction\n")
        f.write("def F(n, d):\n    return Fraction(n, d)\n\n")
        f.write("M0 = [\n")
        for row in M0:
            f.write("  [" + ", ".join(f"F({x.numerator}, {x.denominator})" for x in row) + "],\n")
        f.write("]\n")
        
        f.write("M1 = [\n")
        for row in M1:
            f.write("  [" + ", ".join(f"F({x.numerator}, {x.denominator})" for x in row) + "],\n")
        f.write("]\n")
        
        F0 = []
        for i in range(d):
            idx = basis[i]
            if seq_info[idx][0] == -1: F0.append("1")
            else: F0.append(str(V[seq_info[idx][1]]))
        f.write("F0 = [" + ", ".join(F0) + "]\n")

if __name__ == '__main__':
    compute_exact()
