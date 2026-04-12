def solve_f_mask(N):
    total = 0
    num_squares = N * N
    
    # Pre-map moves to indices
    move_indices = []
    # moves = (dx, dy, ex, ey)
    raw_moves = [
        (2, 1, 1, 0), (2, -1, 1, 0),
        (-2, 1, -1, 0), (-2, -1, -1, 0),
        (1, 2, 0, 1), (-1, 2, 0, 1),
        (1, -2, 0, -1), (-1, -2, 0, -1)
    ]
    for i in range(num_squares):
        r, c = i // N, i % N
        node_moves = []
        for dx, dy, ex, ey in raw_moves:
            tx, ty = r + dx, c + dy
            if 0 <= tx < N and 0 <= ty < N:
                t_idx = tx * N + ty
                e_idx = (r+ex) * N + (c+ey)
                node_moves.append((t_idx, e_idx))
        move_indices.append(node_moves)
        
    knight_adj = []
    for i in range(num_squares):
        r, c = i // N, i % N
        adj = []
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < N and 0 <= nc < N:
                adj.append(nr * N + nc)
        knight_adj.append(adj)

    for mask in range(1, 1 << num_squares):
        valid_hd = True
        for i in range(num_squares):
            if (mask >> i) & 1:
                # Square i is in S
                for t_idx, e_idx in move_indices[i]:
                    if (mask >> t_idx) & 1:
                        # Target in S, check elbow
                        if not ((mask >> e_idx) & 1):
                            valid_hd = False
                            break
                if not valid_hd: break
        
        if not valid_hd: continue
        
        # Knight connected
        # find first bit
        start_node = -1
        count = 0
        for i in range(num_squares):
            if (mask >> i) & 1:
                if start_node == -1: start_node = i
                count += 1
        
        if count == 1:
            total += 1
            continue
            
        visited = 1 << start_node
        queue = [start_node]
        qi = 0
        while qi < len(queue):
            u = queue[qi]
            qi += 1
            for v in knight_adj[u]:
                if ((mask >> v) & 1) and not ((visited >> v) & 1):
                    visited |= (1 << v)
                    queue.append(v)
        
        if visited == mask:
            total += 1
            
    return total

if __name__ == "__main__":
    print(f"f(3) = {solve_f_mask(3)}")
    print(f"f(4) = {solve_f_mask(4)}")
    print(f"f(5) = {solve_f_mask(5)}")
