def J_brute(n, k):
    req_v = [k + i for i in range(n)]
    
    # max visits for any node could be big, but n is unrestricted.
    # what is the total number of visits? sum(v_i) for i<n.
    # we don't know v_n. But jumps to n only happen from n-1. 
    # jumps out of n only go to n-1. 
    # so v_n can be at most R_{n-1} + (1 if ends on n else 0).
    # actually, every visit to n goes to n-1, except possibly the last.
    
    ans = 0
    def dfs(u, visits):
        # visits is a tuple
        nonlocal ans
        
        # terminal check
        # if we visited any i < n too many times, invalid
        for i in range(n):
            if visits[i] > req_v[i]:
                return
                
        # if all i < n exactly match requirements, it's a valid path!
        # wait, after meeting requirements, we can't jump anymore unless we go to n?
        # but we can't visit n-1 anymore if we already met its requirement.
        # so jump to n and stay there? no, "frog finishes on ANY stone"
        # but if we end exactly when all i<n meet reqs, that's a valid journey.
        # However, are we forced to stop? The problem says "it makes exactly k+i visits".
        # Yes, any path that exactly matches all counts for i < n is one valid journey.
        
        is_valid = True
        for i in range(n):
            if visits[i] != req_v[i]:
                is_valid = False
                break
        if is_valid:
            ans += 1
            # we can't continue jumping to anything < n because that would increase its visit count.
            # can we jump to n and stop?
            # From u, if u == n-1, we can jump to n. 
            # if we jump to n, does it increase any i < n? No.
            # wait! If we are at u=n-1, and we jump to n and stop, does it count as another journey?
            # The journey must EXACTLY match counts for i < n.
            # If we jump to n, visits[n] increases. Is n bounded? No.
            # But the journey would be a DIFFERENT sequence of jumps. 
            # Wait, if we are at n-1, jump to n, we can stop. That's a valid way.
            # Can we jump n -> n ? No, "only adjacents".
            # So from n, we MUST jump to n-1, which increases visits[n-1], invalidating the req!
        
        # so if it is valid, we can ONLY jump to n (if u == n-1), and then we MUST stop.
        # because the only jump from n is to n-1.
        
        if u > 0:
            v2 = list(visits)
            v2[u-1] += 1
            dfs(u-1, tuple(v2))
        
        if u < n:
            v2 = list(visits)
            v2[u+1] += 1
            dfs(u+1, tuple(v2))
            
    # start at 0
    v = [0]*(n+1)
    v[0] = 1
    dfs(0, tuple(v))
    return ans

print("J(2, 1) =", J_brute(2, 1))
print("J(3, 2) =", J_brute(3, 2))
