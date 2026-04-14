# Developer Guide: Project Euler 984 - Knights and Horses

## Overview
This project solves Project Euler problem 984 ("Knights and Horses").
The problem requires counting the number of non-empty "horse-disjoint" and "knight-connected" subsets of an $N \times N$ chessboard for $N=10^{18}$, modulo $10^9+7$.

## Mathematical Approach
The core of the solution is based on the following insights:
1. **Geometric Constraints**: Valid multi-row subsets must form contiguous, convex shapes along the horizontal axis. Their left and right boundaries shift by at most $\pm 1$ between adjacent rows.
2. **Graph Connectivity**: A valid shape must be entirely knight-connected. Isolated components must be pruned during generation.
3. **Finite State Machine (FSM)**: Because the width and shift variations are strictly bounded for a globally connected subset, the generation of shapes can be modeled as an FSM.
4. **Linear Recurrence**: By evaluating the sequence of counts $f(N)$ using Dynamic Programming on the FSM for $N \in [1, 200]$, it was discovered that the sequence satisfies a linear recurrence relation of degree 11 for $N \ge 15$.
5. **Fast Evaluation**: For $N=10^{18}$, matrix exponentiation (or polynomial multiplication modulo the characteristic polynomial) is used to evaluate the 11-degree recurrence in $O(d^2 \log N)$ time.

## Algorithms
- **Dynamic Programming (DP)**: A row-by-row DP tracks the relative position of the boundaries and the active components of the knight graph.
- **Berlekamp-Massey**: Used initially to find the shortest linear recurrence describing the sequence $f(N)$.
- **Fiduccia's Algorithm**: Used to compute $X^{10^{18}}$ modulo the characteristic polynomial of the recurrence relation.

## Code Structure
- `984/solve.py`: The final, optimized solver script containing the precomputed recurrence coefficients and the $O(\log N)$ polynomial multiplication.

## Adding/Modifying
When editing the recurrence or testing for smaller $N$, one should reconstruct the FSM in Python (as done in the development scripts) to re-evaluate the base cases.
