## Project Euler 983: Consonant Circle Crossing

**Problem:** Find $R(500)^2$, the minimal $r^2$ allowing a "perfect consonant set" of size $n \ge 500$.

**Key Concepts:**
- **Harmony Points:** Points where exactly 2 circles intersect.
- **Perfect Consonant Set:** A connected set of circles with $|C| = |H| = n$ and no two circles are tangent.
- **Subset Sums:** We build centers using $k$ chosen independent vectors on the circle $x^2+y^2=r^2$.
- Centers are *even* subset sums, harmony points are *odd* subset sums.
- For $n \ge 500$, we need $k=10$ vectors, forming a set of size $2^{10-1} = 512$.
- $r^2$ must have at least 20 integer points to pick 10 independent vectors.

**Algorithm:**
1. Generate candidate $r^2$ values with $\ge 20$ points on the circumference.
2. For each $r^2$, generate the set of points. Choose combinations of 10 independent vectors.
3. Check that the even subset sums do not create extra relations or internal tangencies.
4. Specifically, no even subset sum of length $\ge 4$ can equal a difference $u-v$ between two points on the circle.
5. The smallest valid $r^2$ is our answer.

**Results:**
- Answer: **6925**
- The vectors for 6925: `(-83, 6), (-83, -6), (-78, 29), (-78, -29), (-70, -45), (-45, -70), (-29, 78), (-29, -78), (-6, 83), (-6, -83)`

---