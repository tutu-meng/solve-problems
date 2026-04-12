#include <iostream>
#include <vector>
#include <cstring>
#include <chrono>

using namespace std;

typedef long long ll;

const ll MOD = 1000000007;

ll memo[55][30][30][55];
ll ways_delta[26][26][26][26][500];

vector<ll> multiply(const vector<ll>& a, const vector<ll>& b) {
    if (a.empty() || b.empty()) return {};
    vector<ll> res(a.size() + b.size() - 1, 0);
    for (size_t i = 0; i < a.size(); ++i) {
        if (!a[i]) continue;
        for (size_t j = 0; j < b.size(); ++j) {
            res[i + j] = (res[i + j] + a[i] * b[j]) % MOD;
        }
    }
    return res;
}

vector<ll> poly_pow(vector<ll> p, int exp) {
    vector<ll> res = {1};
    while (exp > 0) {
        if (exp % 2 == 1) res = multiply(res, p);
        p = multiply(p, p);
        exp /= 2;
    }
    return res;
}

ll Comb[30][30];
void precompute_combinations() {
    for (int i = 0; i <= 25; ++i) {
        Comb[i][0] = 1;
        for (int j = 1; j <= i; ++j) {
            Comb[i][j] = (Comb[i - 1][j - 1] + Comb[i - 1][j]) % MOD;
        }
    }
}

vector<ll> get_poly(int A, int Ac) {
    vector<ll> p1(10, 1); p1[0] = 0;
    vector<ll> p0(10, 1);
    vector<ll> res1 = poly_pow(p1, A - Ac);
    vector<ll> res0 = poly_pow(p0, Ac);
    vector<ll> res = multiply(res1, res0);
    for (auto& x : res) x = (x * Comb[A][Ac]) % MOD;
    return res;
}

void precompute_deltas() {
    precompute_combinations();
    
    vector<vector<vector<ll>>> P(26, vector<vector<ll>>(26));
    for (int A = 0; A <= 25; ++A) {
        for (int Ac = 0; Ac <= A; ++Ac) {
            P[A][Ac] = get_poly(A, Ac);
        }
    }
    
    for (int a = 0; a <= 25; ++a) {
        for (int ac = 0; ac <= a; ++ac) {
            for (int b = 0; b <= 25; ++b) {
                if (a + b > 50) continue;
                for (int bc = 0; bc <= b; ++bc) {
                    const auto& P_A = P[a][ac];
                    const auto& P_B = P[b][bc];
                    
                    for (int vl = 0; vl < P_A.size(); ++vl) {
                        if (!P_A[vl]) continue;
                        for (int vr = 0; vr < P_B.size(); ++vr) {
                            if (!P_B[vr]) continue;
                            int delta = vl - vr;
                            ll ways = (P_A[vl] * P_B[vr]) % MOD;
                            ways_delta[a][ac][b][bc][delta + 250] = 
                                (ways_delta[a][ac][b][bc][delta + 250] + ways) % MOD;
                        }
                    }
                }
            }
        }
    }
}

ll dfs(int L, int a, int b, int c) {
    if (a == 0 && b == 0) return (c == 0) ? 1 : 0;
    if (L < a + b) return 0;
    
    if (memo[L][a][b][c + 25] != -1) {
        return memo[L][a][b][c + 25];
    }
    
    ll ways = 0;
    for (int ac = 0; ac <= a; ++ac) {
        for (int bc = 0; bc <= b; ++bc) {
            if (a > 0 && b > 0 && ac == a && bc == b) {
                // terms will consume a+b length and recursively call. 
                // However, since a+b >= 2, L strictly decreases!
            }
            int delta_min = -(b * 9);
            int delta_max = a * 9;
            for (int delta = delta_min; delta <= delta_max; ++delta) {
                if ((delta + c) % 10 == 0) {
                    int c_next = (delta + c) / 10;
                    if (c_next >= -25 && c_next <= 25) {
                        ll wd = ways_delta[a][ac][b][bc][delta + 250];
                        if (wd > 0) {
                            ways = (ways + wd * dfs(L - a - b, ac, bc, c_next)) % MOD;
                        }
                    }
                }
            }
        }
    }
    return memo[L][a][b][c + 25] = ways;
}

ll solve(int N) {
    memset(memo, -1, sizeof(memo));
    ll ans = 0;
    
    // Evaluate sum for lengths exactly up to N.
    // Notice that base case dfs(0,0,0) returns 1 for ANY matching ending, so it captures exact string lengths perfectly.
    // If we want string length <= N, we can just iterate the initial choice of length L
    // But wait! If we pass `N - (K + M - 1)`, it calculates all possible ways that consume ANY length <= N - (K+M-1).
    // Because each valid sequence of consumed lengths corresponds to exactly one valid total length!
    // BUT we must avoid duplicate counting. Is the length inherently bounded by the DP?
    // YES, because DP drops L exactly by `a+b` each step.
    // If it hits `a=0, b=0` with some `L >= 0`, does it return 1?
    // Yes. And that means the total length consumed WAS exactly `N - L`.
    // So one sequence of (K, M, a', b', ...) uniquely determines the string shape and its EXACT length!
    // Since we evaluate for a fixed N and return 1 when `a=0, b=0` regardless of `L`, 
    // are we counting the SAME sequence multiple times for different initial L?
    // Wait. In my DP base case:
    // `if (a == 0 && b == 0) return (c == 0) ? 1 : 0;`
    // This evaluates a path and returns 1. The value returned DOES NOT depend on L!
    // So `dfs(L_start, a, b, c)` returns the number of valid sequences that consume AT MOST `L_start` length!
    // Because if it consumes > L_start, `L < a+b` will prune it and return 0.
    // So `dfs(L_start, K, M, 0)` is exactly the number of strings of length <= N.
    
    for (int K = 1; K <= 25; ++K) {
        for (int M = 1; M <= 25; ++M) {
            int signs = K + M - 1;
            int max_digits_len = N - signs;
            if (max_digits_len >= K + M) {
                ans = (ans + dfs(max_digits_len, K, M, 0)) % MOD;
            }
        }
    }
    return ans;
}

int main() {
    precompute_deltas();
    
    cout << "A(3) = " << solve(3) << " (expected 9)" << endl;
    cout << "A(5) = " << solve(5) << " (expected 171)" << endl;
    cout << "A(7) = " << solve(7) << " (expected 4878)" << endl;
    
    auto st = chrono::high_resolution_clock::now();
    cout << "A(50) = " << solve(50) << endl;
    auto ed = chrono::high_resolution_clock::now();
    
    cout << "Time: " << chrono::duration_cast<chrono::milliseconds>(ed - st).count() << " ms\n";
    return 0;
}
