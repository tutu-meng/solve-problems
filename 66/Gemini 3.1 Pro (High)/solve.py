import math

def get_pell_solution(D):
    a0 = int(math.isqrt(D))
    if a0 * a0 == D:
        return 0 # no solution for perfect squares
        
    m = 0
    d = 1
    a = a0
    
    p1 = 1
    p2 = a0
    
    q1 = 0
    q2 = 1
    
    if p2*p2 - D*q2*q2 == 1:
        return p2
        
    m_n = m
    d_n = d
    a_n = a
    
    while True:
        m_n = d_n * a_n - m_n
        d_n = (D - m_n * m_n) // d_n
        a_n = (a0 + m_n) // d_n
        
        p_next = a_n * p2 + p1
        q_next = a_n * q2 + q1
        
        if p_next * p_next - D * q_next * q_next == 1:
            return p_next
            
        p1 = p2
        p2 = p_next
        q1 = q2
        q2 = q_next

max_x = 0
best_D = 0
for D in range(2, 1001):
    x = get_pell_solution(D)
    if x > max_x:
        max_x = x
        best_D = D

print(best_D)
