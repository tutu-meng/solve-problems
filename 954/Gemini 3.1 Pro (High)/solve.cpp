#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>

using namespace std;

typedef long long ll;

struct MaskPair {
    uint8_t m, mnz;
    bool operator==(const MaskPair& o) const { return m == o.m && mnz == o.mnz; }
};

struct Summary {
    int rem;
    uint8_t m, mnz;
};

struct WeightData {
    int rem;
    int id;
    ll count;
};

// Global state for ID mapping
vector<MaskPair> id_to_mask;
int mask_to_id[128][128];

void reset_ids() {
    id_to_mask.clear();
    for (int i = 0; i < 128; i++) for (int j = 0; j < 128; j++) mask_to_id[i][j] = -1;
}

int get_id(uint8_t m, uint8_t mnz) {
    if (mask_to_id[m][mnz] != -1) return mask_to_id[m][mnz];
    int id = id_to_mask.size();
    id_to_mask.push_back({m, mnz});
    mask_to_id[m][mnz] = id;
    return id;
}

typedef uint64_t StateKey;

inline StateKey encode(int rem, const vector<int>& ids) {
    StateKey key = rem;
    for (int i = 0; i < ids.size(); i++) {
        key |= (uint64_t(ids[i]) << (3 + i * 6));
    }
    return key;
}

inline void decode(StateKey key, int& rem, vector<int>& ids) {
    rem = key & 7;
    for (int i = 0; i < ids.size(); i++) {
        ids[i] = (key >> (3 + i * 6)) & 63;
    }
}

ll solve_length(int L) {
    if (L <= 0) return 0;
    if (L == 1) return 8;

    int v1 = 1;
    for (int i = 0; i < L - 1; i++) v1 = (v1 * 10) % 7;

    int n_w[7] = {0};
    for (int j = 2; j <= L; j++) {
        int w = 1;
        for (int k = 0; k < L - j; k++) w = (w * 10) % 7;
        n_w[w]++;
    }

    reset_ids();
    vector<vector<WeightData>> weight_summaries(7);
    for (int w = 1; w <= 6; w++) {
        int limit = 1;
        for (int i = 0; i < n_w[w]; i++) limit *= 10;
        unordered_map<int, unordered_map<int, unordered_map<int, ll>>> temp;
        for (int i = 0; i < limit; i++) {
            int cur_i = i, r = 0, m = 0, mnz = 0;
            for (int k = 0; k < n_w[w]; k++) {
                int d = cur_i % 10; cur_i /= 10;
                r = (r + d * w) % 7;
                m |= (1 << (d % 7));
                if (d != 0) mnz |= (1 << (d % 7));
            }
            temp[r][m][mnz]++;
        }
        for (auto const& [r, m_map] : temp) {
            for (auto const& [m, mnz_map] : m_map) {
                for (auto const& [mnz, count] : mnz_map) {
                    weight_summaries[w].push_back({r, get_id(m, mnz), count});
                }
            }
        }
    }

    unordered_map<StateKey, ll> dp;
    dp[encode(0, vector<int>(6, get_id(0, 0)))] = 1;

    for (int w = 1; w <= 6; w++) {
        unordered_map<StateKey, ll> next_dp;
        vector<int> ids(6);
        for (auto const& [key, count] : dp) {
            int rem;
            decode(key, rem, ids);
            for (auto const& wd : weight_summaries[w]) {
                ids[w - 1] = wd.id;
                next_dp[encode((rem + wd.rem) % 7, ids)] += count * wd.count;
            }
        }
        dp = next_dp;
    }

    ll heptaphobics = 0;
    vector<int> ids(6);
    for (auto const& [key, count] : dp) {
        int r;
        decode(key, r, ids);
        
        int f_inner = (1 << 0);
        for (int w1 = 1; w1 <= 6; w1++) {
            int m1 = id_to_mask[ids[w1-1]].m;
            if (!m1) continue;
            for (int w2 = 1; w2 <= 6; w2++) {
                int m2 = id_to_mask[ids[w2-1]].m;
                if (!m2) continue;
                int dw = (w1 - w2 + 7) % 7;
                if (dw == 0) continue;
                for (int d1 = 0; d1 < 7; d1++) {
                    if (!(m1 & (1 << d1))) continue;
                    for (int d2 = 0; d2 < 7; d2++) {
                        if (m2 & (1 << d2)) {
                            f_inner |= (1 << ((d1 - d2 + 7) * dw % 7));
                        }
                    }
                }
            }
        }

        for (int d1 = 1; d1 <= 9; d1++) {
            int X = (r + d1 * v1) % 7;
            if (X == 0 || (f_inner & (1 << X))) continue;
            
            bool in_f_outer = false;
            for (int w = 1; w <= 6; w++) {
                int mnz = id_to_mask[ids[w-1]].mnz;
                if (!mnz) continue;
                int dw = (v1 - w + 7) % 7;
                if (dw == 0) continue;
                for (int d2 = 0; d2 < 7; d2++) {
                    if ((mnz & (1 << d2)) && X == (d1 - d2 + 7) * dw % 7) {
                        in_f_outer = true; break;
                    }
                }
                if (in_f_outer) break;
            }
            if (!in_f_outer) heptaphobics += count;
        }
    }
    return heptaphobics;
}

int main() {
    ll total = 0;
    for (int L = 1; L <= 13; L++) {
        ll res = solve_length(L);
        cout << "Length " << L << ": " << res << endl;
        total += res;
    }
    cout << "C(100) = " << solve_length(1) + solve_length(2) << endl;
    cout << "C(10000) = " << solve_length(1) + solve_length(2) + solve_length(3) + solve_length(4) << endl;
    cout << "C(10^13) = " << total << endl;
    return 0;
}
