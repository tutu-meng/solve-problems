import collections

class Solver:
    def __init__(self, N):
        self.N = N
        self.num_squares = N * N
        self.total = 0
        self.memo = {}

    def is_row_hd(self, m0, m1, m2):
        # Check horse-disjoint constraints involving m0
        # 1. Internal to m0
        for j in range(self.N):
            if (m0 >> j) & 1:
                for dj in [2, -2]:
                    tj = j + dj
                    if 0 <= tj < self.N and (m0 >> tj) & 1:
                        if not ((m0 >> (j + dj//2)) & 1): return False
        # 2. m0 <-> m1
        for j in range(self.N):
            if (m0 >> j) & 1:
                for dj in [2, -2]:
                    tj = j + dj
                    if 0 <= tj < self.N and (m1 >> tj) & 1:
                        if not ((m0 >> (j + (1 if dj > 0 else -1))) & 1): return False
                        if not ((m1 >> (tj - (1 if dj > 0 else -1))) & 1): return False
        # 3. m0 <-> m2
        for j in range(self.N):
            if (m0 >> j) & 1:
                for dj in [1, -1]:
                    tj = j + dj
                    if 0 <= tj < self.N and (m2 >> tj) & 1:
                        if not ((m1 >> j) & 1): return False
                        if not ((m1 >> tj) & 1): return False
        return True

    def get_next_partition(self, m0, m1, m2, part):
        # part is a tuple of component IDs for set bits in m1 and m2
        # We need to compute component IDs for set bits in m0 and m1
        pass

    def solve(self):
        # Using a simpler approach: 
        # Since we only need f(6) and f(7) and maybe f(8), let's just 
        # use the bitmask but with row-by-row pruning.
        # solve(row_idx, m_prev1, m_prev2) returns a list of valid (m0, m1, ..., m_row_idx)
        # but we need connectivity. 
        # Actually, let's just use BFS on the connected horse-disjoint sets.
        # But correctly.
        pass

def bitmask_pruned(N):
    total = 0
    # precompute row-to-row horse-disjoint compatibility
    # m0 is valid given m1, m2
    def check_valid(m0, m1, m2):
        for j in range(N):
            if (m0 >> j) & 1:
                # Int (0, +-2) -> (0, +-1)
                for dj in [2, -2]:
                    tj = j + dj
                    if 0 <= tj < N and (m0 >> tj) & 1:
                        if not ((m0 >> (j + dj//2)) & 1): return False
                # m0-m1 (1, +-2) -> (0, +-1) on both
                for dj in [2, -2]:
                    tj = j + dj
                    if 0 <= tj < N and (m1 >> tj) & 1:
                        ej0 = j + (1 if dj > 0 else -1)
                        if not ((m0 >> ej0) & 1): return False
                        ej1 = tj - (1 if dj > 0 else -1)
                        if not ((m1 >> ej1) & 1): return False
                # m0-m2 (2, +-1) -> (1, 0) and (1, +-1)
                for dj in [1, -1]:
                    tj = j + dj
                    if 0 <= tj < N and (m2 >> tj) & 1:
                        if not ((m1 >> j) & 1): return False
                        if not ((m1 >> tj) & 1): return False
        return True

    rows = []
    def dfs(r, m1, m2, current_mask):
        nonlocal total
        if r == N:
            if current_mask == 0: return
            # Check knight connectivity
            if is_knight_connected(current_mask, N):
                total += 1
            return
        
        for m0 in range(1 << N):
            if check_valid(m0, m1, m2):
                dfs(r + 1, m0, m1, current_mask | (m0 << (r * N)))

    def is_knight_connected(mask, N):
        start = -1
        cnt = 0
        for i in range(N*N):
            if (mask >> i) & 1:
                if start == -1: start = i
                cnt += 1
        if cnt == 1: return True
        visited = 1 << start
        queue = [start]
        qi = 0
        while qi < len(queue):
            u = queue[qi]; qi += 1
            r, c = u // N, u % N
            for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < N and 0 <= nc < N:
                    v = nr * N + nc
                    if (mask >> v) & 1 and not (visited >> v) & 1:
                        visited |= (1 << v)
                        queue.append(v)
        return visited == mask

    dfs(0, 0, 0, 0)
    return total

if __name__ == "__main__":
    for n in range(1, 7):
        import time
        start = time.time()
        res = bitmask_pruned(n)
        print(f"f({n}) = {res} ({time.time() - start:.2f}s)")
