import collections

def bitmask_pruned(N):
    total = 0
    def check_valid(m0, m1, m2):
        for j in range(N):
            if (m0 >> j) & 1:
                for dj in [2, -2]:
                    tj = j + dj
                    if 0 <= tj < N and (m0 >> tj) & 1:
                        if not ((m0 >> (j + dj//2)) & 1): return False
                for dj in [2, -2]:
                    tj = j + dj
                    if 0 <= tj < N and (m1 >> tj) & 1:
                        ej0 = j + (1 if dj > 0 else -1)
                        if not ((m0 >> ej0) & 1): return False
                        ej1 = tj - (1 if dj > 0 else -1)
                        if not ((m1 >> ej1) & 1): return False
                for dj in [1, -1]:
                    tj = j + dj
                    if 0 <= tj < N and (m2 >> tj) & 1:
                        if not ((m1 >> j) & 1): return False
                        if not ((m1 >> tj) & 1): return False
        return True

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

    def dfs(r, m1, m2, current_mask):
        nonlocal total
        if r == N:
            if current_mask == 0: return
            if is_knight_connected(current_mask, N):
                total += 1
            return
        
        for m0 in range(1 << N):
            if check_valid(m0, m1, m2):
                dfs(r + 1, m0, m1, current_mask | (m0 << (r * N)))

    dfs(0, 0, 0, 0)
    return total

if __name__ == "__main__":
    import time
    for n in [7]:
        start = time.time()
        res = bitmask_pruned(n)
        print(f"f({n}) = {res} ({time.time() - start:.2f}s)")
