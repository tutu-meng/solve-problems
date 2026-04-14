# Project Euler 984: Knights and Horses

## Description
This project repository provides the solution algorithm for computing $f(10^{18})$ modulo $10^9+7$, where $f(N)$ computes the count of knight-connected, horse-disjoint non-empty subsets of an $N \times N$ chessboard.

## Implementation Details
The problem was solved analytically and computationally by identifying that valid shapes fall strictly into finite structures spanning across rows. These configurations were modeled as a Finite State Machine (FSM), where transitions depend on relative left and right boundaries and component connectivity.

Running the DP FSM up to small heights revealed that the sequence follows a linear recurrence relation of degree 11 for all $N \ge 15$.
The problem asks for $N = 10^{18}$, which is computed using fast evaluation (Fiduccia's algorithm/matrix exponentiation).

## Usage
Simply execute the main python program:
```sh
python3 984/solve.py
```

## Structure
- `docs/`: Reference documentation and system context.
- `984/`: Contains the specific solver module.

## Diagrams
```mermaid
graph TD;
    A[Initial Rows 1..N] --> B[Generate Relative Row Intervals L, R];
    B --> C[Compute Knight Intersections];
    C --> D{Is Valid & Connected?};
    D -- Yes --> E[Next Row L+dL, R+dR];
    D -- No --> F[Prune Invalid State];
    E --> C;
    E --> G[Accumulate to Sequence DP];
    G --> H[Berlekamp-Massey Extractor];
    H --> I[Recurrence Characteristic Polynomial];
    I --> J[X^{10^18} Modulo Poly Exp];
    J --> K(Final Answer);
```
