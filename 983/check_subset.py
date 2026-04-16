import itertools
import random

def check_subsets(k):
    centers = []
    points = []
    for i in range(1 << k):
        bits = bin(i).count('1')
        if bits % 2 == 0:
            centers.append(i)
        else:
            points.append(i)
            
    adj = {c: [] for c in centers}
    for c in centers:
        for i in range(k):
            adj[c].append(c ^ (1 << i))
            
    found_sizes = set()
    for size in range(2, len(centers) + 1):
        # try 10000 random subsets of this size
        for _ in range(5000):
            curr = random.choice(centers)
            subset = {curr}
            q = [curr]
            while len(subset) < size:
                node = random.choice(list(subset))
                n1 = random.choice(adj[node])
                n2 = random.choice([c for c in centers if n1 in adj[c]])
                subset.add(n2)
            
            hp_counts = {}
            for c in subset:
                for p in adj[c]:
                    hp_counts[p] = hp_counts.get(p, 0) + 1
            
            H = [p for p, cnt in hp_counts.items() if cnt >= 2]
            if len(H) == size:
                found_sizes.add(size)
    print(f"k={k}, perfect subset sizes found: {sorted(list(found_sizes))}")

for k in range(3, 6):
    check_subsets(k)
