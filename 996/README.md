# Project Euler 996: Tennis Leader Board

## Result

The required value is:

```text
137726405
```

## Key Observations

Non-overtake matches only consume days, so it is enough to count overtake sequences whose length is even and at most `k`. Let `E = floor(k / 2)`, where one edge represents two pair crossings that restore the pair's relative order.

For any two players, returning to the initial order means they cross equally in both directions. Their repeated crossings contribute equally to both players' overtake counts. The possible count vectors can therefore be described as degree sequences of multigraph components that occupy contiguous intervals of the initial ranking.

This gives a local condition on each maximal positive run of overtake counts:

- Its sum must be even, say `2e`.
- No entry in the run may exceed `e`.

For a positive run of length `l` and edge count `e`, the number of valid count assignments is the number of positive compositions of `2e` into `l` parts, with every part at most `e`:

$$
A(l,e)=\binom{2e-1}{l-1}-l\binom{e-1}{l-1}.
$$

The subtraction removes the cases where one part is greater than `e`; at most one part can violate the bound.

## Algorithm

1. Dynamic program over positions using two states:
   - `zero`: the current prefix ends at a zero or at the start.
   - `positive`: the current prefix ends with a positive run.
2. Start a positive run only from `zero`, using `A(l,e)`.
3. Append a zero from either state.
4. For fixed `n`, the cumulative count for edge limit `E` is a polynomial in `E` of degree `n`.
5. Compute the first `n + 1` values and use Lagrange interpolation modulo `1234567891`.

## Verification

The solver prints:

```text
F(3, 4) = 8 (expected 8)
F(12, 34) = 2457178250 (expected 2457178250)
F(12, 34) mod 1234567891 = 1222610359 (expected 1222610359)
```

The final printed line is:

```text
137726405
```

## Diagram

```mermaid
flowchart TD
    A[Ignore non-overtake days] --> B[Count even overtake length <= k]
    B --> C[Pair crossings return in opposite directions]
    C --> D[Counts are interval multigraph degree sequences]
    D --> E[Split tuple into maximal positive runs]
    E --> F{Run sum 2e and max <= e?}
    F -- yes --> G[Run contributes A(l,e)]
    F -- no --> H[Invalid count tuple]
    G --> I[DP over zero-separated runs]
    I --> J[Get first n+1 cumulative values]
    J --> K[Lagrange interpolate at floor(k/2)]
    K --> L[Answer modulo 1234567891]
```
