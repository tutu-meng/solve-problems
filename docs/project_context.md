# Project Context: Project Euler 984

## Purpose
This repository houses the solution logic, research, and analysis for Project Euler 984: Knights and Horses. The primary goal is to compute $f(10^{18}) \bmod 10^9+7$.

## Background
The puzzle blends combinatorics, finite state machines, and algebraic recurrence theory. A valid shape requires satisfying two opposing conditions:
1. **Horse-disjoint**: The shape must be convex with specific horizontal boundary conditions (preventing moves within the piece's immediate vicinity).
2. **Knight-connected**: The entire set of chosen squares must be reachable using standard knight moves.

The tension between these constraints means valid connected shapes cannot grow infinitely wide at a rapid pace, bounding the structure into a small finite state automaton of configurations over successive rows.

## Architecture
The system is constructed with one primary execution script (`984/solve.py`) containing the end-result of our research:
- A linear recurrence of degree 11 that governs the sequence.
- The initial 11 boundary cases of the sequence ($N=4$ to $14$).
- A fast exponentiation algorithm that resolves $X^{N-15}$ modulo the characteristic polynomial.

## Constraints
- Time Limit: Fast polynomial multiplication allows instantaneous calculation of $O(\log N)$ complexity.
- Modulo Arithmetic: All addition, subtraction, and multiplication must stay strictly within $10^9+7$.
