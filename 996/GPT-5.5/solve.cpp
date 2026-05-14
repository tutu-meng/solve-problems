#include <cstdint>
#include <iostream>
#include <vector>

using namespace std;

using i64 = long long;
using u64 = unsigned long long;

static constexpr i64 MOD = 1234567891LL;

static i64 norm(i64 x) {
    x %= MOD;
    if (x < 0) x += MOD;
    return x;
}

static i64 mod_pow(i64 base, i64 exp) {
    i64 result = 1;
    while (exp > 0) {
        if (exp & 1) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

static vector<vector<i64>> build_combinations_mod(int limit) {
    vector<vector<i64>> comb(limit + 1, vector<i64>(limit + 1, 0));
    for (int i = 0; i <= limit; ++i) {
        comb[i][0] = comb[i][i] = 1;
        for (int j = 1; j < i; ++j) {
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j];
            if (comb[i][j] >= MOD) comb[i][j] -= MOD;
        }
    }
    return comb;
}

static vector<vector<i64>> build_run_counts_mod(int max_len, int max_edges) {
    vector<vector<i64>> comb = build_combinations_mod(2 * max_edges);
    vector<vector<i64>> run(max_len + 1, vector<i64>(max_edges + 1, 0));

    for (int len = 1; len <= max_len; ++len) {
        for (int edges = 1; edges <= max_edges; ++edges) {
            i64 ways = 0;
            if (2 * edges - 1 >= len - 1) {
                ways += comb[2 * edges - 1][len - 1];
            }
            if (edges - 1 >= len - 1) {
                ways -= static_cast<i64>(len) * comb[edges - 1][len - 1] % MOD;
            }
            run[len][edges] = norm(ways);
        }
    }

    return run;
}

static vector<i64> cumulative_values_mod(int n, int max_edges) {
    vector<vector<i64>> run = build_run_counts_mod(n, max_edges);
    vector<vector<i64>> zero(n + 1, vector<i64>(max_edges + 1, 0));
    vector<vector<i64>> positive(n + 1, vector<i64>(max_edges + 1, 0));
    zero[0][0] = 1;

    for (int pos = 0; pos <= n; ++pos) {
        if (pos < n) {
            for (int used = 0; used <= max_edges; ++used) {
                i64 ways = zero[pos][used] + positive[pos][used];
                if (ways >= MOD) ways -= MOD;
                if (ways == 0) continue;
                zero[pos + 1][used] += ways;
                if (zero[pos + 1][used] >= MOD) zero[pos + 1][used] -= MOD;
            }
        }

        for (int used = 0; used <= max_edges; ++used) {
            i64 base = zero[pos][used];
            if (base == 0) continue;
            for (int len = 1; pos + len <= n; ++len) {
                for (int add = 1; used + add <= max_edges; ++add) {
                    i64 choices = run[len][add];
                    if (choices == 0) continue;
                    i64& target = positive[pos + len][used + add];
                    target = (target + base * choices) % MOD;
                }
            }
        }
    }

    vector<i64> values(max_edges + 1, 0);
    i64 total = 0;
    for (int edges = 0; edges <= max_edges; ++edges) {
        total += zero[n][edges] + positive[n][edges];
        total %= MOD;
        values[edges] = total;
    }
    return values;
}

static i64 interpolate_at(const vector<i64>& values, i64 x) {
    int degree = static_cast<int>(values.size()) - 1;
    if (x <= degree) return values[static_cast<size_t>(x)];

    i64 xm = x % MOD;
    vector<i64> prefix(degree + 2, 1), suffix(degree + 2, 1);
    for (int i = 0; i <= degree; ++i) {
        prefix[i + 1] = prefix[i] * norm(xm - i) % MOD;
    }
    for (int i = degree; i >= 0; --i) {
        suffix[i] = suffix[i + 1] * norm(xm - i) % MOD;
    }

    vector<i64> fact(degree + 1, 1), inv_fact(degree + 1, 1);
    for (int i = 1; i <= degree; ++i) {
        fact[i] = fact[i - 1] * i % MOD;
    }
    inv_fact[degree] = mod_pow(fact[degree], MOD - 2);
    for (int i = degree; i >= 1; --i) {
        inv_fact[i - 1] = inv_fact[i] * i % MOD;
    }

    i64 answer = 0;
    for (int i = 0; i <= degree; ++i) {
        i64 numerator = prefix[i] * suffix[i + 1] % MOD;
        i64 inv_denominator = inv_fact[i] * inv_fact[degree - i] % MOD;
        if ((degree - i) & 1) inv_denominator = MOD - inv_denominator;
        answer = (answer + values[i] * numerator % MOD * inv_denominator) % MOD;
    }
    return answer;
}

static i64 solve_mod(int n, i64 k) {
    i64 edge_limit = k / 2;
    vector<i64> values = cumulative_values_mod(n, n);
    return interpolate_at(values, edge_limit);
}

static vector<vector<u64>> build_combinations_exact(int limit) {
    vector<vector<u64>> comb(limit + 1, vector<u64>(limit + 1, 0));
    for (int i = 0; i <= limit; ++i) {
        comb[i][0] = comb[i][i] = 1;
        for (int j = 1; j < i; ++j) {
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j];
        }
    }
    return comb;
}

static u64 direct_exact(int n, int edge_limit) {
    vector<vector<u64>> comb = build_combinations_exact(2 * edge_limit);
    vector<vector<u64>> run(n + 1, vector<u64>(edge_limit + 1, 0));
    for (int len = 1; len <= n; ++len) {
        for (int edges = 1; edges <= edge_limit; ++edges) {
            u64 ways = 0;
            if (2 * edges - 1 >= len - 1) {
                ways += comb[2 * edges - 1][len - 1];
            }
            if (edges - 1 >= len - 1) {
                ways -= static_cast<u64>(len) * comb[edges - 1][len - 1];
            }
            run[len][edges] = ways;
        }
    }

    vector<vector<u64>> zero(n + 1, vector<u64>(edge_limit + 1, 0));
    vector<vector<u64>> positive(n + 1, vector<u64>(edge_limit + 1, 0));
    zero[0][0] = 1;
    for (int pos = 0; pos <= n; ++pos) {
        if (pos < n) {
            for (int used = 0; used <= edge_limit; ++used) {
                zero[pos + 1][used] += zero[pos][used] + positive[pos][used];
            }
        }
        for (int used = 0; used <= edge_limit; ++used) {
            u64 base = zero[pos][used];
            if (base == 0) continue;
            for (int len = 1; pos + len <= n; ++len) {
                for (int add = 1; used + add <= edge_limit; ++add) {
                    positive[pos + len][used + add] += base * run[len][add];
                }
            }
        }
    }

    u64 total = 0;
    for (int edges = 0; edges <= edge_limit; ++edges) {
        total += zero[n][edges] + positive[n][edges];
    }
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "F(3, 4) = " << direct_exact(3, 2) << " (expected 8)\n";
    cout << "F(12, 34) = " << direct_exact(12, 17) << " (expected 2457178250)\n";
    cout << "F(12, 34) mod " << MOD << " = " << solve_mod(12, 34)
         << " (expected 1222610359)\n";
    cout << solve_mod(123, 4567891) << '\n';

    return 0;
}
