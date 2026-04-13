#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <queue>
#include <utility>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
using namespace std;

// DP approach: enumerate valid non-singleton sets as convex shapes
// (each row is a contiguous interval [L[r], R[r]])
// Process row by row from top to bottom.
// 
// Need to track: last 2 rows' intervals for the 2-row knight move constraint.
// State: (L_prev, R_prev, L_curr, R_curr)
// But also need to track knight-connectivity.
//
// For now, let's just check horse-disjoint and see if we match.
// We'll handle connectivity separately.
//
// Actually, the intervals are on [0, N-1]. The state is O(N^4) * N rows = O(N^5).
// For N up to about 20 this is feasible.
//
// But wait - let's use translation invariance.
// Instead of absolute L, R, use the width w = R - L + 1 and the left shift dL = L_curr - L_prev.
// Then the state could be (w_prev_prev, w_prev, dL_prev, dL_curr).
// Actually this gets complicated with the 3-row constraint.
//
// Let me just do the direct DP for small N first, up to maybe N=15.

const int MOD = 1000000007;
int N;

// For each row, state is (L, R) with 0 <= L <= R <= N-1
// We represent it as index: L * N + R (when L <= R)
// For the DP, we need to track last 2 rows.
// State: (L_prev, R_prev, L_curr, R_curr) + connectivity info
// 
// Connectivity: In a convex region, knight-connectivity requires
// that the set is "reachable" via knight moves. For wide enough shapes
// (width >= 3 in all but edge rows), this is automatic. For narrow shapes,
// we need to verify.
//
// For now, let me just count horse-disjoint convex sets and check
// against the brute force to see if connectivity is always satisfied.

// Check if adding a row with interval [L2, R2] after rows [L0, R0] and [L1, R1]
// satisfies the horse-disjoint condition for 2-row knight moves.
// 
// Recall: (r,c) <-> (r+2,c+1):
// Both in set: c in [L0, R0] and c+1 in [L2, R2], so c in [max(L0,L2-1), min(R0,R2-1)].
// Need c in [L1, R1-1]. (c and c+1 both in [L1, R1])
// So overlap = [max(L0,L2-1), min(R0,R2-1)] must be subset of [L1, R1-1].
//
// (r,c) <-> (r+2,c-1):
// Both in set: c in [L0, R0] and c-1 in [L2, R2], so c in [max(L0,L2+1), min(R0,R2+1)].
// Need c in [L1+1, R1]. (c and c-1 both in [L1, R1])
// So overlap = [max(L0,L2+1), min(R0,R2+1)] must be subset of [L1+1, R1].

bool check_2row(int L0, int R0, int L1, int R1, int L2, int R2) {
    // Check (r,c) <-> (r+2,c+1) constraint
    {
        int lo = max(L0, L2-1), hi = min(R0, R2-1);
        if (lo <= hi) {
            // Need [lo, hi] ⊆ [L1, R1-1]
            if (lo < L1 || hi > R1-1) return false;
        }
    }
    // Check (r,c) <-> (r+2,c-1) constraint
    {
        int lo = max(L0, L2+1), hi = min(R0, R2+1);
        if (lo <= hi) {
            // Need [lo, hi] ⊆ [L1+1, R1]
            if (lo < L1+1 || hi > R1) return false;
        }
    }
    return true;
}

// Check 1-row horse-disjoint constraint between rows r and r+1
// with intervals [L0, R0] and [L1, R1].
// Knight moves: (r,c) <-> (r+1,c+2) and (r,c) <-> (r+1,c-2)
//
// (r,c) -> (r+1,c+2): block at (r, c+1) -> c+1 in [L0, R0]
//                       block at (r+1, c+1) -> c+1 in [L1, R1]
// This pair exists iff c in [L0, R0] and c+2 in [L1, R1], i.e., c in [L1-2, R1-2]
// So c in [max(L0, L1-2), min(R0, R1-2)].
// Need c+1 in [L0, R0] => c <= R0-1 => min(R0, R1-2) <= R0-1 => R1-2 <= R0-1 => R1 <= R0+1
// Need c+1 in [L1, R1] => c >= L1-1. Since c >= max(L0, L1-2) >= L1-2. 
//   If L0 >= L1-1 then c >= L0 >= L1-1, OK.
//   If L0 < L1-1 then c >= L1-2, so c could be L1-2. Then c+1 = L1-1 < L1. Fail.
//   So need L0 >= L1-1 => L1 <= L0+1.
// OR overlap is empty.

// (r,c) -> (r+1,c-2): block at (r, c-1) and (r+1, c-1).
// Pair exists iff c in [L0, R0] and c-2 in [L1, R1], i.e., c in [L1+2, R1+2].
// c in [max(L0, L1+2), min(R0, R1+2)].
// Need c-1 in [L0, R0] => c >= L0+1 => max(L0, L1+2) >= L0+1 => L1+2 >= L0+1 => L1 >= L0-1 => L0 <= L1+1.
// Need c-1 in [L1, R1] => c <= R1+1 => min(R0, R1+2) <= R1+1 => R0 <= R1+1 => R1 >= R0-1.
// OR overlap is empty.

bool check_1row(int L0, int R0, int L1, int R1) {
    // (r,c) <-> (r+1,c+2)
    {
        int lo = max(L0, L1-2), hi = min(R0, R1-2);
        if (lo <= hi) {
            if (R1 > R0+1) return false;
            if (L1 > L0+1) return false;
        }
    }
    // (r,c) <-> (r+1,c-2)
    {
        int lo = max(L0, L1+2), hi = min(R0, R1+2);
        if (lo <= hi) {
            if (L0 > L1+1) return false;
            if (R0 > R1+1) return false;
        }
    }
    return true;
}

int main() {
    // Count horse-disjoint convex sets (each row contiguous, rows contiguous)
    // without connectivity constraint, and compare with brute force + connectivity
    
    for (N = 1; N <= 8; N++) {
        long long count_singletons = (long long)N * N;
        
        // Count multi-row convex horse-disjoint sets by DP
        // We need to handle both the "number of rows" and the horse-disjoint constraints.
        // 
        // For a set spanning rows [r_start, r_end]:
        // - All rows r in [r_start, r_end] have non-empty interval [L[r], R[r]]
        // - 1-row constraint between consecutive rows
        // - 2-row constraint between rows 2 apart
        //
        // By vertical and horizontal translation:
        // The shape is determined by the widths w[r] and shifts s[r] = L[r] - L[r-1].
        // The number of placements = (N - height + 1) * (N - (max_R - min_L) + 1 ... 
        // actually not quite because of constraints on L[r], R[r].
        //
        // Actually let me just track absolute positions since N is small.
        
        // DP state: (row_index, L_prev, R_prev, L_curr, R_curr)
        // where _prev is the row before _curr.
        // For the first row, there's no _prev.
        
        // We'll enumerate "shapes" by fixing r_start and processing each successive row.
        // For convenience: row_idx = current row index (0-based).
        // After processing all rows of the shape, we count it.
        
        long long total_convex_hd = 0; // horse-disjoint convex sets
        
        // For each starting row r0 (the shape spans rows [r0, r0+h-1] for some h >= 2)
        // DP over columns using intervals
        
        // State: after processing rows 0..i of the shape:
        //   (L_{i-1}, R_{i-1}, L_i, R_i) if i >= 1
        //   (L_0, R_0) if i == 0
        
        // Let me just count by iterating:
        // For each height h from 2 to N:
        //   For each sequence of (L[0], R[0]), ..., (L[h-1], R[h-1]):
        //     Check all constraints.
        //     Number of placements = (N - h + 1) possible vertical positions.
        //     Horizontal placement: L_min = min(L[r]), R_max = max(R[r]).
        //     Need L_min >= 0 already (since we use L relative to something).
        //     
        // OK, let me use a simpler DP: process shapes from top to bottom.
        // State after deciding rows 0..k:
        //   (L[k-1], R[k-1], L[k], R[k])
        // When adding row k+1 with (L[k+1], R[k+1]):
        //   Check 1-row constraint between (L[k], R[k]) and (L[k+1], R[k+1]).
        //   Check 2-row constraint among (L[k-1], R[k-1]), (L[k], R[k]), (L[k+1], R[k+1]).
        
        // But we also need to count the number of vertical and horizontal placements.
        // By translation invariance:
        //   Vertical placements: (N - height + 1)
        //   Horizontal: the shape has some "bounding box" width W = max(R[r]) - min(L[r]) + 1.
        //     The shape can be shifted so that min(L[r]) ranges from 0 to N - W.
        //     But the L[r] values are relative to min(L[r]).
        //     So horizontal placements = max(0, N - W + 1).
        //     BUT we need to be careful: the constraint that 0 <= L[r] and R[r] <= N-1
        //     might add more constraints. Since we defined L relative to min_L = 0,
        //     and all L[r] >= 0, R[r] = L[r] + w[r] - 1, the rightmost R is max(R[r]) = W-1 + shift.
        //     So shift can range from 0 to N-1-(W-1) = N-W. Number of placements = N-W+1.
        
        // So the total count of multi-row sets = sum over shapes * (N - height + 1) * (N - W + 1)
        
        // Let me implement this with DP.
        // The shape is defined relative to min_L = 0.
        // State: (L[k-1], R[k-1], L[k], R[k], max_R_so_far)
        // where L values are relative (min_L of all rows so far = 0).
        // Actually, to track min_L and max_R, we need more info.
        // Let me just track (L_prev, R_prev, L_curr, R_curr) and also min_L, max_R.
        
        // For N <= 8, the intervals are small. Let me just enumerate.
        
        // map from state (L_{k-1}, R_{k-1}, L_k, R_k) to count of shapes seen so far
        // But also need to track min_L and max_R across all rows to compute W.
        
        // Hmm, this gets complicated. Let me just use absolute coordinates
        // (not relative) and iterate over all possible intervals.
        
        // Alternative: directly count via DP with absolute coords.
        // dp[L_prev, R_prev, L_curr, R_curr] = number of such shapes ending
        // at the current row, where _prev and _curr are the last 2 rows.
        // When we "complete" a shape (don't add more rows), we count it.
        // The starting row can be any of N possible rows (for vertical placement),
        // but the shape's height is determined. Actually, the vertical placement
        // count is (N - height + 1) which we track.
        
        // Simplification: since both dimensions are N, and we need N up to ~20 for
        // the recurrence search, let me just do it as:
        // For each height h = 1, 2, ..., N:
        //   Count the number of valid shapes of height h.
        //   Multiply by (N - h + 1) for vertical placement.
        //   For horizontal placement: each shape has a certain horizontal span W,
        //   multiply by (N - W + 1).
        
        // A "shape" is defined by the sequence of (L[0], ..., L[h-1]) where
        // L[0] = 0 (normalize), and widths (w[0], ..., w[h-1]) with w[r] >= 1.
        // The horizontal span W = max(L[r] + w[r] - 1) - min(L[r]) + 1
        //                        = max(R[r]) + 1  (since min(L[r]) = 0 by normalization)
        
        // So: shape count for horizontal = N - W + 1 = N - max(R[r]).
        
        // This is still O(N^{2h}) which is too slow for large h.
        // But with DP tracking (L_prev, R_prev, L_curr, R_curr, max_R),
        // it's more manageable.
        
        // Actually, max_R can go up to N-1, so the state space is:
        // (L_prev, R_prev, L_curr, R_curr, max_R_so_far) with each in [0, N-1].
        // That's N^5 states. For N=8, 32768 per row, not bad.
        
        // But we also need to track min_L. Since L[0] = 0, min_L starts at 0
        // but could become negative if L[r] decreases. Oh wait, if we use
        // ABSOLUTE coordinates, all L[r] in [0, N-1]. Let me just use absolute
        // coords and not normalize.
        
        // OK forget everything, let me just do a raw DP with absolute coordinates.
        // For N <= 10, this should work.
        
        // dp[i][Lp][Rp][Lc][Rc] = 1 if there's a valid shape ending at row i with
        // rows i-1 and i having intervals [Lp, Rp] and [Lc, Rc].
        // But I want to count all shapes, not just track existence.
        // Actually, since the shape is determined by the sequence of intervals,
        // and we're summing over all shapes, the DP value is:
        // dp[Lp][Rp][Lc][Rc] = number of valid shapes ending with these last two intervals.
        
        // Wait, but different shapes can have the same last two intervals.
        // And we need max_R across all rows to determine horizontal placement count.
        // So we can't merge shapes with different max_R.
        
        // For simplicity, let me just enumerate all valid multi-row shapes
        // and count placements. For N <= 10, the shapes are manageable.
        
        // Actually, I realize the problem is symmetric in rows and columns.
        // The board is N×N. Let me just process row by row with DP.
        
        // State: (L_pp, R_pp, L_p, R_p) where _pp is 2 rows ago, _p is 1 row ago.
        // For each new row with (L_c, R_c):
        //   Check 1-row constraint between (L_p, R_p) and (L_c, R_c).
        //   Check 2-row constraint among (L_pp, R_pp), (L_p, R_p), (L_c, R_c).
        //   (Skip 2-row if fewer than 3 rows so far.)
        
        // For counting valid sets on the N×N board, each valid set corresponds to
        // a contiguous range of rows [r_start, r_end] with intervals [L[r], R[r]].
        // All L, R in [0, N-1]. The number of such sets is the sum over all valid
        // sequences of intervals.
        
        // DP idea: process the board from row 0 to row N-1.
        // At each row, decide: does this row participate in the current shape?
        // If yes, add it with some interval. If no, the shape ends (or hasn't started).
        
        // State: (phase, L_{-2}, R_{-2}, L_{-1}, R_{-1})
        // phase: 0 = haven't started, 1 = just started (1 row so far), 2+ = 2+ rows.
        // When phase >= 1 and we decide to not continue, we "finish" the shape.
        
        // This would correctly count all valid shapes, but the state space is
        // O(N^4) per row and N rows => O(N^5). For N=8: 8^5 = 32768. Totally fine.
        // For N=20: 20^5 = 3.2M. Also fine.
        
        // Let me implement this.
        
        // But wait, I also need to check knight-CONNECTIVITY.
        // For convex shapes, when is knight-connectivity guaranteed?
        // 
        // In a rectangle of width w and height h:
        // - If w >= 3, a knight can reach any square from any other square 
        //   (the knight graph on a rectangle ≥ 3 wide is connected for h >= 2).
        // - If w == 2, the knight can only move ±(2,1) staying within width 2:
        //   from (r,0) can go to (r+1,2) which is out, or (r+2,1) which is in.
        //   So (r,0) <-> (r+2,1) and (r,1) <-> (r+2,0). This connects all squares.
        //   Actually, from (r,0): can move to (r+1,2) out, (r-1,2) out, 
        //   (r+2,1), (r-2,1), (r+2,-1) out, (r-2,-1) out.
        //   So from (r,0): (r+2,1) and (r-2,1).
        //   From (r,1): (r+2,0) and (r-2,0).
        //   For h >= 3: (0,0) -> (2,1), (2,1) -> (0,0) (back). But (2,1) -> (4,0) etc.
        //   So it forms a chain: connected if h >= 3 or h = 2 (then only 4 squares, 
        //   and (0,0)->(2,1) needs row 2, so for h=2, from (0,0) we can't reach (1,1)).
        //   Hmm, width=2, height=2: squares (0,0),(0,1),(1,0),(1,1).
        //   Knight moves from (0,0): (1,2) out, (2,1) out. No moves! Disconnect.
        //   So width=2, height=2 is disconnected.
        //   Width=2, height=3: from (0,0)->(2,1), from (2,1)->(0,0), from (0,1)->(2,0).
        //   Squares: 6 total. (0,0) connected to (2,1). (0,1) connected to (2,0).
        //   But (1,0) and (1,1) have no knight neighbors within the set.
        //   So width=2, height=3 is NOT knight-connected.
        
        // For the horse-disjoint convex shapes, the minimum width was ≥ 2 for interior
        // rows and could be 1 for edge rows. Knight-connectivity in such shapes 
        // depends on the specific shape. This makes the DP more complex.
        
        // For now, let me just count horse-disjoint convex shapes without connectivity
        // and compare with the brute-force values to see the difference.
        
        // Using absolute coordinates:
        long long total_hd_convex = 0;
        
        // Enumerate all valid shapes by DFS/iteration
        // For each starting row r0 (always take r0=0 for simplicity, multiply by N-h+1 later... 
        // no, that doesn't work because the intervals depend on absolute position)
        
        // Actually, intervals are always in [0, N-1], independent of vertical position.
        // And the horizontal positions are absolute. So a shape starting at row r0
        // is the same as one starting at row r0' if the intervals are the same.
        // So: count shapes by height, with (N-h+1) vertical placements.
        
        // For each height h = 1, ..., N:
        //   Count sequences (L[0],R[0]), ..., (L[h-1],R[h-1]) with:
        //     0 <= L[i] <= R[i] <= N-1
        //     1-row HD constraint for adjacent rows
        //     2-row HD constraint for rows 2 apart
        //   Multiply by (N-h+1).
        
        // For h=1: any interval [L,R], contributes (N-1+1) * C(N,2+N) ...
        // No wait. For h=1, every interval [L,R] is a valid set. The number of such
        // sets for a fixed vertical position is C(N,2) + N = N(N+1)/2 (choosing L <= R).
        // But these will include singletons.
        
        // Hmm, for h=1: valid set = any single-row interval [L,R] with L <= R.
        // For horse-disjoint: no knight moves within a single row (distance at least 2
        // in each direction for a knight move, but within one row, the row difference is 0).
        // Wait: two squares in the same row separated by 0 rows can still be knight-move
        // adjacent? No! A knight move has |dx|=2,|dy|=1 or |dx|=1,|dy|=2. For dx=0,
        // there's no knight move. So within a single row, no knight moves exist.
        // So any single-row interval is horse-disjoint.
        // But is it knight-connected? Only if it's a singleton (no knight edges within row).
        // For |interval| >= 2: no knight edges, so the set is NOT knight-connected.
        // So single-row valid sets are only singletons.
        
        // So the count is: singletons (N^2 of them) + multi-row connected shapes.
        
        // For multi-row shapes: the knight-connectivity is the tricky part.
        // Let me for now just count horse-disjoint convex multi-row shapes
        // (with height >= 2 and each row having width >= 1) and see how it
        // compares with the brute-force answer minus N^2.
        
        printf("N=%d:\n", N);
        
        // DP for multi-row shapes (height >= 2)
        // Process: enumerate shapes of height h for h=2,...,N.
        // For each h, DP over rows.
        
        long long total_hd = 0;
        
        for (int h = 2; h <= N; h++) {
            long long vert = N - h + 1; // vertical placements
            
            // DP: dp[Lpp][Rpp][Lp][Rp] = count of valid sequences of length k
            // For k=1 (first row of shape): dp_init[L0][R0] = 1 for all valid intervals.
            // We don't have Lpp, Rpp yet.
            // For k=2: check 1-row constraint only.
            // For k>=3: check both 1-row and 2-row constraints.
            
            // Phase 1: initialize with first 2 rows (k=2)
            // dp2[Lp][Rp][Lc][Rc] = 1 if valid
            vector<vector<vector<vector<long long>>>> dp(N, vector<vector<vector<long long>>>(N, vector<vector<long long>>(N, vector<long long>(N, 0))));
            
            for (int L0 = 0; L0 < N; L0++)
            for (int R0 = L0; R0 < N; R0++)
            for (int L1 = 0; L1 < N; L1++)
            for (int R1 = L1; R1 < N; R1++) {
                if (check_1row(L0, R0, L1, R1)) {
                    dp[L0][R0][L1][R1] = 1;
                }
            }
            
            if (h == 2) {
                long long shape_count = 0;
                for (int L0 = 0; L0 < N; L0++)
                for (int R0 = L0; R0 < N; R0++)
                for (int L1 = 0; L1 < N; L1++)
                for (int R1 = L1; R1 < N; R1++) {
                    shape_count += dp[L0][R0][L1][R1];
                }
                total_hd += shape_count * vert;
            } else {
                // Add more rows
                for (int row = 2; row < h; row++) {
                    vector<vector<vector<vector<long long>>>> ndp(N, vector<vector<vector<long long>>>(N, vector<vector<long long>>(N, vector<long long>(N, 0))));
                    
                    for (int Lp = 0; Lp < N; Lp++)
                    for (int Rp = Lp; Rp < N; Rp++)
                    for (int Lc = 0; Lc < N; Lc++)
                    for (int Rc = Lc; Rc < N; Rc++) {
                        if (dp[Lp][Rp][Lc][Rc] == 0) continue;
                        // Try adding new row with [Ln, Rn]
                        for (int Ln = 0; Ln < N; Ln++)
                        for (int Rn = Ln; Rn < N; Rn++) {
                            if (!check_1row(Lc, Rc, Ln, Rn)) continue;
                            if (!check_2row(Lp, Rp, Lc, Rc, Ln, Rn)) continue;
                            ndp[Lc][Rc][Ln][Rn] += dp[Lp][Rp][Lc][Rc];
                        }
                    }
                    
                    if (row == h - 1) {
                        long long shape_count = 0;
                        for (int L0 = 0; L0 < N; L0++)
                        for (int R0 = L0; R0 < N; R0++)
                        for (int L1 = 0; L1 < N; L1++)
                        for (int R1 = L1; R1 < N; R1++) {
                            shape_count += ndp[L0][R0][L1][R1];
                        }
                        total_hd += shape_count * vert;
                    }
                    
                    dp = ndp;
                }
            }
        }
        
        printf("  HD convex multi-row count: %lld\n", total_hd);
        printf("  Total (HD convex + singletons): %lld\n", total_hd + count_singletons);
    }
    
    return 0;
}
