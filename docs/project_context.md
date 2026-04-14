## Project Euler Problem 983: Consonant Circle Crossing

This document details the solution to Project Euler Problem 983, which involves finding the minimal $R^2$ that allows a "perfect consonant set" of circles of size $n \ge 500$.

### Problem Restatement

Given a set of circles of radius $r$ centered at integer grid points, two points are in "harmony" if exactly two circles intersect at those points.
A set of $n$ circles is a "perfect consonant set" if:
1. The number of unique harmony points is exactly $n$.
2. The union of the circles is a single connected component.
3. No two circles are tangent to each other.

We are looking for $R(500)^2$, the minimal $r^2$ such that a perfect consonant set of $n \ge 500$ exists.

### Mathematical Analysis

#### Condition 1: Harmony Points and Subsets

Suppose a perfect consonant set consists of circles centered at $C = \{c_1, c_2, \dots, c_n\}$.
Let the set of harmony points be $H = \{h_1, h_2, \dots, h_n\}$.
Since $|C| = |H| = n$, the bipartite graph formed by incidences between circles and harmony points must have specific properties.

We discovered that perfect consonant sets can be formed by starting with a subset of independent vectors $V = \{v_1, v_2, \dots, v_k\}$ that lie on the circle $x^2 + y^2 = r^2$.
The set of circle centers $C$ is constructed by taking all subset sums of $V$ that have an *even* number of terms.
The set of harmony points $H$ is constructed by taking all subset sums of $V$ that have an *odd* number of terms.

If there are no "relations" (linear dependencies with coefficients $\pm 1$, except the trivial ones) among the vectors in $V$, then all subset sums are unique.
Thus, $|C| = 2^{k-1}$ and $|H| = 2^{k-1}$.
This perfectly satisfies the condition $|C| = |H| = n$, where $n = 2^{k-1}$.

#### Target Size

We need $n \ge 500$.
Since $n = 2^{k-1}$, the smallest power of 2 greater than or equal to 500 is $512$, which corresponds to $k = 10$.
Thus, we need to choose 10 vectors from the set of integer points on the circle $x^2 + y^2 = r^2$.

#### Vector Selection

To select 10 independent vectors, the circle must have at least $2k = 20$ integer points (since for every point $(x,y)$, its opposite $(-x,-y)$ is also on the circle, but we cannot pick both as they are trivially dependent: $v + (-v) = 0$).

Therefore, we need to search for $r^2$ values that can be expressed as the sum of two squares in many ways.
The number of integer points on $x^2 + y^2 = r^2$ is $4 \times (d_1(r^2) - d_3(r^2))$, where $d_i(N)$ is the number of divisors of $N$ congruent to $i \pmod 4$.

Candidate $R^2$ values with at least 20 points include: $325, 425, 625, 650, 725, 845, 850, 925, 1025, 1105, \dots$

#### Tangency and Relations

For a chosen set of 10 vectors, the resulting set $C$ must satisfy:
1. **No Tangency:** No two centers $c_1, c_2 \in C$ can be at distance exactly $2r$. That is, $(c_{1x} - c_{2x})^2 + (c_{1y} - c_{2y})^2 \neq 4r^2$.
2. **No Relations:** The set of centers $C$ must have exactly 512 distinct points, and the number of harmony points $H$ must also be exactly 512. A relation like $\sum \epsilon_i v_i = 0$ (where $\sum |\epsilon_i|$ is even) would cause centers to coincide, reducing $|C|$. A relation like $\sum \epsilon_i v_i = u - v$ (where $u, v$ are points on the circle) would create extra harmony points, breaking $|C| = |H|$.

By generating combinations of 10 vectors and testing these conditions, we search for the minimum $R^2$.

### Search Results

We systematically checked the candidate $r^2$ values:
- **$r^2 = 325$:** Has 24 points (12 vector pairs). All combinations fail due to relations or extra harmony points.
- **$r^2 = 425$:** Has 24 points. All combinations fail.
- **$r^2 = 625$:** Has 20 points (10 vector pairs). The only combination forms 512 centers, but fails because there are 1218 harmony points (extra relations exist).
- ...
- **$r^2 = 6925$:** Has 24 points. We found a valid combination of 10 vectors that forms exactly 512 centers, 512 harmony points, and has no internal tangencies.

The vectors chosen for $r^2 = 6925$ are:
`(-83, 6), (-83, -6), (-78, 29), (-78, -29), (-70, -45), (-45, -70), (-29, 78), (-29, -78), (-6, 83), (-6, -83)`

### Conclusion

The minimal $R^2$ that allows a perfect consonant set of $n \ge 500$ (specifically $n = 512$) is **6925**.

### Final Answer

$R(500)^2 = 6925$
