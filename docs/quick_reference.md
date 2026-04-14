# Quick Reference: Project Euler 984

## Sequence Definition
$f(N)$ defines the number of knight-connected, horse-disjoint non-empty subsets on an $N \times N$ chessboard.

- $f(1) = 1$
- $f(2) = 4$
- $f(3) = 9$
- $f(4) = 92$
- $f(5) = 903$
- $f(6) = 4411$
- $f(7) = 14959$
- $f(100) = 8658918531876 \equiv 348421318 \pmod{10^9+7}$

## Key Files
- **`984/solve.py`**: Executes the mathematical recurrence solver for $N=10^{18}$.

## Linear Recurrence
The sequence $f(N)$ obeys a degree 11 characteristic equation for $N \ge 15$:
$f_N = \sum_{j=1}^{11} (-C_j) f_{N-j} \pmod{10^9+7}$

Coefficients $C_1 \dots C_{11}$:
$[-7, 19, -21, -6, 42, -42, 6, 21, -19, 7, -1]$

## Execution
Run `python3 984/solve.py` to print the final answer to stdout.
