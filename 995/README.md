# Project Euler 995: Divisor Residues

## Problem
Compute:

$$
T(20000)=\prod_{p<20000}S(p)
$$

where $S(p)$ is the least positive integer $s$ such that:

$$
1+x+\cdots+x^{p-1}
$$

divides:

$$
1+\sum_{d\mid s}x^d.
$$

The answer must be printed in scientific notation rounded to five digits after the decimal point.

## Key Idea
Since $1+x+\cdots+x^{p-1}=\Phi_p(x)$, divisibility means the exponent counts in $g_s(x)$ are uniformly distributed modulo $p$.

For a valid minimal $s$, $p\nmid s$, so the divisors of $s$ must hit each nonzero residue exactly once:

$$
\tau(s)=p-1.
$$

Let $N=p-1$ and choose a primitive root $r$ modulo $p$. A rational prime $q$ contributes an additive step:

$$
b=\log_r(q)\pmod N.
$$

The divisors of:

$$
s=\prod q_i^{a_i}
$$

produce all sums:

$$
\sum_i e_i b_i \pmod N,\quad 0\le e_i\le a_i.
$$

So the problem becomes a minimum-cost mixed-radix tiling of the cyclic group $C_N$.

## Algorithm
At processed scale $D$, an interval length $d=a+1$ is valid when:

$$
D\mid b,\quad \gcd(b/D,d)=1.
$$

The solver:

1. Generates primes up to `PRIME_SEARCH_LIMIT`.
2. Finds a primitive root and discrete logs for each prime $p<20000$.
3. Records the least rational prime $q$ satisfying each transition `(D, d)`.
4. Runs DP over divisors of $p-1$ to minimize:

$$
\sum (d-1)\log_{10}(q).
$$

5. Sums $\log_{10}S(p)$ and formats the result.

## Verification
The solver checks:

```text
T(20) = 1348422598656
T(100) = 1.37451e123
```

## Usage
```sh
g++ -O2 -std=c++17 "995/GPT-5.5/solve.cpp" -o solve
./solve
```

Final answer:

```text
2.21322e536280
```

## Diagram
```mermaid
flowchart TD
    A[Phi_p divides g_s] --> B[Uniform exponent counts mod p]
    B --> C[p does not divide s]
    C --> D[Divisors cover nonzero residues once]
    D --> E[Choose primitive root r]
    E --> F[Map q to b = log_r q]
    F --> G[Build C_(p-1) by mixed radix intervals]
    G --> H{D divides b and gcd b/D,d = 1}
    H -- Valid --> I[Use least compatible prime q]
    I --> J[DP minimizes logarithmic cost]
    J --> K[Sum logs for p < 20000]
    K --> L[Format scientific answer]
```
