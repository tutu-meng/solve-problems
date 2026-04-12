import collections

def get_closure(S_mask, N):
    # Squares indices 0..N*N-1
    # Returns the smallest horse-disjoint set containing S_mask
    mask = S_mask
    while True:
        new_bits = 0
        for i in range(N*N):
            if (mask >> i) & 1:
                r, c = i // N, i % N
                # Horse moves from (r, c)
                for dr, dc, er, ec in [(2,1,1,0), (2,-1,1,0), (-2,1,-1,0), (-2,-1,-1,0), (1,2,0,1), (-1,2,0,1), (1,-2,0,-1), (-1,-2,0,-1)]:
                    tr, tc = r + dr, c + dc
                    if 0 <= tr < N and 0 <= tc < N:
                        if (mask >> (tr * N + tc)) & 1:
                            # Must have elbow
                            e_idx = (r + er) * N + (c + ec)
                            if not ((mask >> e_idx) & 1):
                                new_bits |= (1 << e_idx)
        if new_bits == 0:
            break
        mask |= new_bits
    return mask

def is_connected(mask, N):
    if mask == 0: return False
    start_node = -1
    count = 0
    for i in range(N*N):
        if (mask >> i) & 1:
            if start_node == -1: start_node = i
            count += 1
    if count == 1: return True
    
    visited = 1 << start_node
    queue = collections.deque([start_node])
    while queue:
        u = queue.popleft()
        r, c = u // N, u % N
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < N and 0 <= nc < N:
                v = nr * N + nc
                if ((mask >> v) & 1) and not ((visited >> v) & 1):
                    visited |= (1 << v)
                    queue.append(v)
    return visited == mask

def solve_f(N):
    found = set()
    # BFS on closures
    # Each state is a bitmask
    # Optimization: since N is small, bitmasks are fine.
    
    # Start with all singletons
    queue = collections.deque()
    for i in range(N*N):
        m = 1 << i
        found.add(m)
        queue.append(m)
        
    while queue:
        curr = queue.popleft()
        # Try adding a knight-neighbor of any square in curr
        for i in range(N*N):
            if (curr >> i) & 1:
                r, c = i // N, i % N
                for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < N and 0 <= nc < N:
                        idx = nr * N + nc
                        if not ((curr >> idx) & 1):
                            # Possible expansion
                            new_m = get_closure(curr | (1 << idx), N)
                            if new_m not in found:
                                # We MUST check if it's connected.
                                # Wait, get_closure might add squares that bridge components
                                # but is it guaranteed to be connected if curr was connected?
                                # Yes, adding a neighbor of curr and then closures keeps it connected.
                                if is_connected(new_m, N):
                                    found.add(new_m)
                                    queue.append(new_m)
    return len(found)

if __name__ == "__main__":
    for n in range(1, 6):
        print(f"f({n}) = {solve_f(n)}")
