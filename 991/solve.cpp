#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

using namespace std;

typedef long long ll;

const ll LIMIT = 10000000;
// S = 5y - d. In interval 1, y >= 0.25d. S = 1.25d - d = 0.25d <= LIMIT => d <= 4*LIMIT
// Since S must be > 0 and <= LIMIT, to be safe, search up to 4*LIMIT + 100
const ll MAX_D = 4 * LIMIT + 100;

int R[MAX_D + 1];
int min_prime[MAX_D + 1];
vector<int> primes;

void linear_sieve(int max_val) {
    R[1] = 1;
    for (int i = 2; i <= max_val; ++i) {
        if (min_prime[i] == 0) {
            min_prime[i] = i;
            primes.push_back(i);
            R[i] = i;
        }
        for (int p : primes) {
            if (p * i > max_val) break;
            min_prime[p * i] = p;
            
            if (i % p == 0) {
                int temp = i;
                int count = 1;
                while (temp % p == 0) {
                    count++;
                    temp /= p;
                }
                int p_power_r = 1;
                for (int j = 0; j < (count + 1) / 2; ++j) {
                    p_power_r *= p;
                }
                R[p * i] = p_power_r * R[temp];
                break;
            } else {
                R[p * i] = p * R[i];
            }
        }
    }
}

int main() {
    auto start_time = chrono::high_resolution_clock::now();
    
    linear_sieve(MAX_D);
    
    ll s_sum = 0;
    
    for (ll d = 1; d <= MAX_D; ++d) {
        if (d % 1000000 == 0) {
            cerr << "Processing d = " << d << "\r" << flush;
        }
        
        long double d_ld = d;
        ll S1_sqrt = sqrtl(21.0L * d_ld * d_ld - 4.0L * d_ld);
        ll S2_sqrt = sqrtl(12.0L * d_ld * d_ld + 4.0L * d_ld);
        
        ll limit_y = (LIMIT + d) / 5;
        ll r = R[d];
        
        // Interval 1
        ll y1_min = max((d + 3) / 4, (5 * d - S1_sqrt) / 2 - 2);
        ll y1_max = min(limit_y, (4 * d - S2_sqrt) / 2 + 2);
        
        ll k1_min = (y1_min + r - 1) / r;
        ll k1_max = y1_max / r;
        
        for (ll k = k1_min; k <= k1_max; ++k) {
            ll y = k * r;
            if (y * y - 5LL * d * y + d * (d + 1LL) <= 0 &&
                y * y - 4LL * d * y + d * (d - 1LL) >= 0 &&
                4LL * y >= d + 1LL) {
                ll s = 5LL * y - d;
                if (s <= LIMIT) {
                    s_sum += s;
                }
            }
        }
        
        // Interval 2
        ll y2_min = (4 * d + S2_sqrt) / 2 - 2;
        ll y2_max = min(limit_y, (5 * d + S1_sqrt) / 2 + 2);
        
        ll k2_min = (y2_min + r - 1) / r;
        ll k2_max = y2_max / r;
        
        for (ll k = k2_min; k <= k2_max; ++k) {
            ll y = k * r;
            if (y * y - 5LL * d * y + d * (d + 1LL) <= 0 &&
                y * y - 4LL * d * y + d * (d - 1LL) >= 0 &&
                4LL * y >= d + 1LL) {
                ll s = 5LL * y - d;
                if (s <= LIMIT) {
                    s_sum += s;
                }
            }
        }
    }
    cerr << endl;
    
    cout << "Sum = " << s_sum << endl;
    
    auto end_time = chrono::high_resolution_clock::now();
    cout << "Time: " << chrono::duration_cast<chrono::milliseconds>(end_time - start_time).count() << " ms" << endl;
    
    return 0;
}
