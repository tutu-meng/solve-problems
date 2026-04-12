import sys

def solve_dp(N):
    # State: (mask_prev, mask_curr, partition)
    # Since knight moves reach row i-2, we need mask_{i-1} and mask_{i-2} when adding mask_i.
    # No, to check edges (i, j) <-> (i-2, j'), we need i-1 for elbows.
    # To check edges (i, j) <-> (i-1, j'), we need i for elbows.
    # So when we add row i, we check:
    # 1. Internal to i: (i, j) <-> (i, j+-2) elbows in i.
    # 2. i <-> i-1: (i, j) <-> (i-1, j+-2) elbows in i-1 or i. (Wait, let's see).
    #    (i, j) -> (i-1, j+2) elbow is (i, j+1). (In row i). Correct.
    #    (i-1, j+2) -> (i, j) elbow is (i-1, j+1). (In row i-1). Correct.
    # 3. i <-> i-2: (i, j) <-> (i-2, j+-1) elbow in i-1.
    #    (i, j) -> (i-2, j+1) elbow is (i-1, j). (In row i-1). Correct.
    #    (i-2, j+1) -> (i, j) elbow is (i-1, j+1). (In row i-1). Correct.
    
    # So we need rows i, i-1, i-2 to check horse-disjointness and connectivity.
    
    # dp[mask_prev2][mask_prev1][partition] = count
    
    memo = {(0, 0, ()): 1}
    
    for r in range(N):
        new_memo = {}
        for (m2, m1, part), count in memo.items():
            for m0 in range(1 << N):
                # Check horse-disjoint for row r (m0)
                # 1. Internal to m0
                valid = True
                for j in range(N):
                    if (m0 >> j) & 1:
                        # Moves (0, +-2)
                        for dj in [2, -2]:
                            tj = j + dj
                            if 0 <= tj < N and (m0 >> tj) & 1:
                                ej = j + (dj // 2)
                                if not ((m0 >> ej) & 1):
                                    valid = False; break
                    if not valid: break
                if not valid: continue
                
                # 2. m0 <-> m1
                for j in range(N):
                    if (m0 >> j) & 1:
                        # Moves (-1, +-2)
                        for dj in [2, -2]:
                            tj = j + dj
                            if 0 <= tj < N and (m1 >> tj) & 1:
                                # Elbow from m0 to m1 (1, 2 move): elbow is same column?
                                # (r, j) -> (r-1, j+2) displacement (-1, 2).
                                # Step 1 (orth): (0, 1). Square (r, j+1). Row m0.
                                ej = j + (dj // 2) if dj > 0 else j - 1
                                # Wait. (r, j) to (r-1, j+2) uses (r, j+1).
                                # (r-1, j+2) to (r, j) displacement (1, -2).
                                # Step 1 (orth): (0, -1). Square (r-1, j+1). Row m1.
                                ej_curr = j + (1 if dj > 0 else -1)
                                if not ((m0 >> ej_curr) & 1):
                                    valid = False; break
                                ej_prev = tj - (1 if dj > 0 else -1)
                                if not ((m1 >> ej_prev) & 1):
                                    valid = False; break
                    if not valid: break
                if not valid: continue
                
                # 3. m0 <-> m2
                for j in range(N):
                    if (m0 >> j) & 1:
                        # Moves (-2, +-1)
                        for dj in [1, -1]:
                            tj = j + dj
                            if 0 <= tj < N and (m2 >> tj) & 1:
                                # (r, j) -> (r-2, j+1) displacement (-2, 1).
                                # Step 1: (-1, 0). Square (r-1, j). Row m1.
                                if not ((m1 >> j) & 1):
                                    valid = False; break
                                # (r-2, j+1) -> (r, j) displacement (2, -1).
                                # Step 1: (1, 0). Square (r-1, j+1). Row m1.
                                if not ((m1 >> tj) & 1):
                                    valid = False; break
                    if not valid: break
                if not valid: continue
                
                # Connectivity check? Not here.
                # Just collect valid patterns first?
                # No, we must track connectivity.
                
                # This is too slow for N=10^18 but okay for N=6,7.
                # Wait, I'll just use the bitmask script for N=6,7 but with PRUNING.
                pass
    return 0
