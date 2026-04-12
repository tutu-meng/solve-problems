#include <iostream>
#include <vector>

using namespace std;

typedef long long ll;
const ll MOD = 987898789;
const int MAX_FACT = 2000000;

ll fact[MAX_FACT];
ll invFact[MAX_FACT];

ll power(ll base, ll exp) {
    ll res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

ll modInverse(ll n) {
    return power(n, MOD - 2);
}

void precompute() {
    fact[0] = 1;
    invFact[0] = 1;
    for (int i = 1; i < MAX_FACT; i++) {
        fact[i] = (fact[i - 1] * i) % MOD;
    }
    invFact[MAX_FACT - 1] = modInverse(fact[MAX_FACT - 1]);
    for (int i = MAX_FACT - 2; i >= 1; i--) {
        invFact[i] = (invFact[i + 1] * (i + 1)) % MOD;
    }
}

ll nCr(ll n, ll r) {
    if (r < 0 || r > n) return 0;
    ll res = (fact[n] * invFact[r]) % MOD;
    res = (res * invFact[n - r]) % MOD;
    return res;
}

ll path_count(const vector<ll>& R_list, const vector<ll>& L_list, int E, int n, ll k) {
    ll ways = 1;
    for (int i = 1; i < n; i++) {
        ll R = R_list[i];
        ll L = L_list[i];
        ll total_exits = R + L;
        
        if (i < E) {
            ways = (ways * nCr(total_exits - 1, R - 1)) % MOD;
        } else if (i > E) {
            ways = (ways * nCr(total_exits - 1, R)) % MOD;
        } else {
            ways = (ways * nCr(total_exits, R)) % MOD;
        }
    }
    return ways;
}

ll J_math(int n, ll k) {
    ll total = 0;
    vector<ll> R(n + 1, 0);
    vector<ll> L(n + 1, 0);
    
    for (int E = 0; E <= n; E++) {
        bool possible = true;
        R[0] = (E == 0) ? (k - 1) : k;
        if (R[0] < 0) continue;
        
        for (int i = 1; i < n; i++) {
            L[i] = (i <= E) ? (R[i - 1] - 1) : R[i - 1];
            if (L[i] < 0) {
                possible = false;
                break;
            }
            
            ll req_R = (k + i) - L[i] - ((E == i) ? 1 : 0);
            if (req_R < 0) {
                possible = false;
                break;
            }
            R[i] = req_R;
        }
        
        if (!possible) continue;
        total = (total + path_count(R, L, E, n, k)) % MOD;
    }
    return total;
}

int main() {
    precompute();
    
    ll ans = 0;
    ll powers[5] = {1, 10, 100, 1000, 10000};
    for (int s = 0; s <= 4; s++) {
        ll k = powers[s];
        ll val = J_math(500, k);
        ans = (ans + val) % MOD;
        cout << "J(500, " << k << ") = " << val << endl;
    }
    cout << "Final answer modulo " << MOD << " : " << ans << endl;
    
    return 0;
}
