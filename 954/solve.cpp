#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <cmath>

using namespace std;

typedef long long ll;

struct Summary {
    int rem;
    int mask;
    int mask_nz;
    bool operator<(const Summary& o) const {
        if (rem != o.rem) return rem < o.rem;
        if (mask != o.mask) return mask < o.mask;
        return mask_nz < o.mask_nz;
    }
};

map<Summary, ll> get_summaries(int n_w, int w) {
    map<Summary, ll> res;
    int limit = 1;
    for (int i = 0; i < n_w; i++) limit *= 10;
    for (int i = 0; i < limit; i++) {
        int temp = i;
        int sum_rem = 0;
        int mask = 0;
        int mask_nz = 0;
        for (int j = 0; j < n_w; j++) {
            int d = temp % 10;
            temp /= 10;
            sum_rem = (sum_rem + d * w) % 7;
            mask |= (1 << (d % 7));
            if (d != 0) mask_nz |= (1 << (d % 7));
        }
        res[{sum_rem, mask, mask_nz}]++;
    }
    return res;
}

struct FullState {
    int rem;
    uint8_t masks[6];
    uint8_t nz_masks[6];
    
    bool operator<(const FullState& o) const {
        if (rem != o.rem) return rem < o.rem;
        for (int i = 0; i < 6; i++) if (masks[i] != o.masks[i]) return masks[i] < o.masks[i];
        for (int i = 0; i < 6; i++) if (nz_masks[i] != o.nz_masks[i]) return nz_masks[i] < o.nz_masks[i];
        return false;
    }
};

ll solve_length(int L) {
    if (L == 0) return 0;
    if (L == 1) {
        // heptaphobic 1..9: all except 7
        return 8;
    }

    int v1 = 1; // 10^(L-1) % 7
    for (int i = 0; i < L - 1; i++) v1 = (v1 * 10) % 7;

    int n_w[7] = {0};
    for (int j = 2; j <= L; j++) {
        int w = 1;
        for (int k = 0; k < L - j; k++) w = (w * 10) % 7;
        n_w[w]++;
    }

    vector<map<Summary, ll>> weight_summaries(7);
    for (int w = 1; w <= 6; w++) {
        weight_summaries[w] = get_summaries(n_w[w], w);
    }

    // Merge 6 weights
    map<vector<pair<int, int>>, map<int, ll>> dp; // {masks} -> {rem -> count}
    
    // Initial: no weights processed
    vector<pair<int, int>> initial_masks(6, {0, 0});
    dp[initial_masks][0] = 1;

    for (int w = 1; w <= 6; w++) {
        map<vector<pair<int, int>>, map<int, ll>> next_dp;
        for (auto const& [masks, rem_map] : dp) {
            for (auto const& [summ, ways] : weight_summaries[w]) {
                vector<pair<int, int>> next_masks = masks;
                next_masks[w-1] = {summ.mask, summ.mask_nz};
                for (auto const& [r, count] : rem_map) {
                    next_dp[next_masks][(r + summ.rem) % 7] += count * ways;
                }
            }
        }
        dp = next_dp;
    }

    ll heptaphobics = 0;
    for (auto const& [masks, rem_map] : dp) {
        // Precompute F_inner
        int f_inner = (1 << 0);
        for (int w1 = 1; w1 <= 6; w1++) {
            int m1 = masks[w1-1].first;
            if (m1 == 0) continue;
            // Case w1 == w2: (d - d')(0) = 0. Already in f_inner.
            // Wait, if |S_w1| > 1, then (d-d')*0 is 0. 
            // Correct.
            for (int w2 = 1; w2 <= 6; w2++) {
                int m2 = masks[w2-1].first;
                if (m2 == 0) continue;
                int dw = (w1 - w2 + 7) % 7;
                if (dw == 0) continue;
                for (int d1 = 0; d1 < 7; d1++) {
                    if (!(m1 & (1 << d1))) continue;
                    for (int d2 = 0; d2 < 7; d2++) {
                        if (!(m2 & (1 << d2))) continue;
                        int diff = (d1 - d2 + 7) % 7;
                        f_inner |= (1 << ((diff * dw) % 7));
                    }
                }
            }
        }

        for (auto const& [r, count] : rem_map) {
            for (int d1 = 1; d1 <= 9; d1++) {
                int X = (r + d1 * v1) % 7;
                if (X == 0) continue;
                if (f_inner & (1 << X)) continue;
                
                // F_outer
                bool in_f_outer = false;
                for (int w = 1; w <= 6; w++) {
                    int mnz = masks[w-1].second;
                    int dw = (v1 - w + 7) % 7;
                    if (dw == 0) continue;
                    for (int d2 = 0; d2 < 7; d2++) {
                        if (mnz & (1 << d2)) {
                            int diff = (d1 - d2 + 7) % 7;
                            if (X == (diff * dw) % 7) {
                                in_f_outer = true;
                                break;
                            }
                        }
                    }
                    if (in_f_outer) break;
                }
                if (!in_f_outer) {
                    heptaphobics += count;
                }
            }
        }
    }

    return heptaphobics;
}

int main() {
    cout << "C(100) = " << solve_length(1) + solve_length(2) << endl;
    cout << "C(1000) = " << solve_length(1) + solve_length(2) + solve_length(3) << endl;
    cout << "C(10000) = " << solve_length(1) + solve_length(2) + solve_length(3) + solve_length(4) << endl;
    
    ll total = 0;
    for (int L = 1; L <= 13; L++) {
        ll res = solve_length(L);
        cout << "Length " << L << ": " << res << endl;
        total += res;
    }
    cout << "C(10^13) = " << total << endl;
    return 0;
}
