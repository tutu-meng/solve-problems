#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

using namespace std;

typedef long long ll;

const int N_MAX = 100000000;
const int K_MAX = 2 * N_MAX;

int R[K_MAX + 1];
int min_prime[K_MAX + 1];
vector<int> primes;

void linear_sieve(int max_val) {
    R[1] = 1;
    for (int i = 2; i <= max_val; ++i) {
        if (min_prime[i] == 0) {
            min_prime[i] = i;
            primes.push_back(i);
            R[i] = i; // p^1 -> R(p) = p^(ceil(1/2)) = p
        }
        for (int p : primes) {
            if (p * i > max_val) break;
            min_prime[p * i] = p;
            
            // Calculate R for p * i
            if (i % p == 0) {
                // p divides i, so we are extending a prime power.
                // We need to count the exact power of p in i.
                int temp = i;
                int count = 1; // already includes the p we multiply by
                while (temp % p == 0) {
                    count++;
                    temp /= p;
                }
                
                // R(p^count * temp) = p^(ceil(count/2)) * R(temp)
                int p_power_r = 1;
                for (int j = 0; j < (count + 1) / 2; ++j) {
                    p_power_r *= p;
                }
                R[p * i] = p_power_r * R[temp];
                break;
            } else {
                // p does not divide i, so gcd(p, i) = 1.
                // R is multiplicative, so R(p * i) = R(p) * R(i)
                R[p * i] = p * R[i];
            }
        }
    }
}

ll compute_f(ll n) {
    ll total_pairs = 0;
    for (ll k = 2; k <= 2 * n; ++k) {
        ll r_k = R[k];
        
        // Number of x such that x <= k/2 and x is a multiple of r_k
        ll max_valid_x_count = (k / 2) / r_k;
        
        // Number of x such that x < k - n and x is a multiple of r_k
        ll min_x_bound = max(0LL, k - n - 1);
        ll invalid_x_count = min_x_bound / r_k;
        
        total_pairs += (max_valid_x_count - invalid_x_count);
    }
    return total_pairs;
}

int main() {
    auto start_time = chrono::high_resolution_clock::now();
    
    // Test base cases to ensure correctness
    int test_n = 5;
    linear_sieve(2 * test_n);
    cout << "f(" << test_n << ") = " << compute_f(test_n) << " (expected 2)" << endl;
    
    test_n = 10;
    linear_sieve(2 * test_n);
    cout << "f(" << test_n << ") = " << compute_f(test_n) << " (expected 6)" << endl;
    
    test_n = 100;
    linear_sieve(2 * test_n);
    cout << "f(" << test_n << ") = " << compute_f(test_n) << " (expected 110)" << endl;
    
    test_n = 1000;
    linear_sieve(2 * test_n);
    cout << "f(" << test_n << ") = " << compute_f(test_n) << " (expected 1569)" << endl;

    cout << "\nPreparing to calculate for N = 10^8..." << endl;
    ll huge_n = 100000000LL; // 10^8
    
    // We clear primes and reset arrays (or normally start clean, since sizing allows it)
    primes.clear();
    for (int i = 0; i <= 2 * test_n; i++) min_prime[i] = 0; // Quick reset
    
    auto sieve_start = chrono::high_resolution_clock::now();
    linear_sieve(2 * huge_n);
    auto sieve_end = chrono::high_resolution_clock::now();
    
    auto calc_start = chrono::high_resolution_clock::now();
    ll result = compute_f(huge_n);
    auto calc_end = chrono::high_resolution_clock::now();
    
    auto end_time = chrono::high_resolution_clock::now();
    
    cout << "f(10^8) = " << result << endl;
    
    cout << "\nTiming info:" << endl;
    cout << "Sieve time: " << chrono::duration_cast<chrono::milliseconds>(sieve_end - sieve_start).count() << " ms" << endl;
    cout << "Calculation time: " << chrono::duration_cast<chrono::milliseconds>(calc_end - calc_start).count() << " ms" << endl;
    cout << "Total time: " << chrono::duration_cast<chrono::milliseconds>(end_time - start_time).count() << " ms" << endl;

    return 0;
}
