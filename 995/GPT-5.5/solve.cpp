#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using namespace std;

static constexpr int TARGET_M = 20000;
static constexpr int PRIME_SEARCH_LIMIT = 5000000;
static constexpr int KEY_BASE = 20001;

static vector<int> primes;
static vector<int> small_primes;

static long long pow_mod(long long base, int exp, int mod) {
    long long result = 1;
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

static vector<int> sieve_primes(int limit) {
    vector<bool> is_prime(limit + 1, true);
    is_prime[0] = false;
    is_prime[1] = false;
    for (int i = 2; 1LL * i * i <= limit; ++i) {
        if (!is_prime[i]) continue;
        for (long long j = 1LL * i * i; j <= limit; j += i) {
            is_prime[static_cast<size_t>(j)] = false;
        }
    }

    vector<int> out;
    for (int i = 2; i <= limit; ++i) {
        if (is_prime[i]) out.push_back(i);
    }
    return out;
}

static vector<pair<int, int>> factorize(int n) {
    vector<pair<int, int>> factors;
    for (int q : small_primes) {
        if (1LL * q * q > n) break;
        if (n % q != 0) continue;
        int exp = 0;
        while (n % q == 0) {
            n /= q;
            ++exp;
        }
        factors.push_back({q, exp});
    }
    if (n > 1) factors.push_back({n, 1});
    return factors;
}

static vector<int> make_divisors(const vector<pair<int, int>>& factors) {
    vector<int> divisors{1};
    for (auto [prime, exp] : factors) {
        vector<int> next;
        int power = 1;
        for (int e = 0; e <= exp; ++e) {
            for (int d : divisors) {
                next.push_back(d * power);
            }
            power *= prime;
        }
        divisors.swap(next);
    }
    sort(divisors.begin(), divisors.end());
    return divisors;
}

static vector<vector<int>> divisor_lookup(int n, const vector<int>& divisors) {
    vector<vector<int>> lookup(n + 1);
    for (int value : divisors) {
        for (int d : divisors) {
            if (value % d == 0) lookup[value].push_back(d);
        }
    }
    return lookup;
}

static int primitive_root(int p) {
    vector<pair<int, int>> factors = factorize(p - 1);
    for (int g = 2; g < p; ++g) {
        bool ok = true;
        for (auto [q, exp] : factors) {
            (void)exp;
            if (static_cast<int>(pow_mod(g, (p - 1) / q, p)) == 1) {
                ok = false;
                break;
            }
        }
        if (ok) return g;
    }
    return 1;
}

static unsigned long long pow_int(int base, int exp) {
    unsigned long long result = 1;
    unsigned long long b = static_cast<unsigned long long>(base);
    while (exp > 0) {
        if (exp & 1) result *= b;
        b *= b;
        exp >>= 1;
    }
    return result;
}

struct SolverForPrime {
    int p;
    int n;
    vector<int> divisors;
    vector<vector<int>> divisors_of;
    unordered_map<int, int> condition_index;
    vector<int> best_prime;
    vector<long double> memo_log;
    vector<char> seen_log;
    vector<unsigned long long> memo_exact;
    vector<char> seen_exact;

    explicit SolverForPrime(int prime) : p(prime), n(prime - 1) {
        vector<pair<int, int>> factors = factorize(n);
        divisors = make_divisors(factors);
        divisors_of = divisor_lookup(n, divisors);
        build_best_primes();
        memo_log.assign(n + 1, 0.0L);
        seen_log.assign(n + 1, 0);
        memo_exact.assign(n + 1, 0);
        seen_exact.assign(n + 1, 0);
    }

    void build_best_primes() {
        vector<pair<int, int>> conditions;
        for (int d_processed : divisors) {
            int rem = n / d_processed;
            for (int length : divisors_of[rem]) {
                if (length <= 1) continue;
                int key = d_processed * KEY_BASE + length;
                condition_index[key] = static_cast<int>(conditions.size());
                conditions.push_back({d_processed, length});
            }
        }

        best_prime.assign(conditions.size(), 0);
        int remaining = static_cast<int>(conditions.size());

        int root = primitive_root(p);
        vector<int> discrete_log(p, 0);
        int residue = 1;
        for (int exp = 0; exp < n; ++exp) {
            discrete_log[residue] = exp;
            residue = static_cast<int>(1LL * residue * root % p);
        }

        for (int q : primes) {
            if (q == p) continue;
            int log_q = discrete_log[q % p];
            if (log_q == 0) continue;

            int gcd_log = std::gcd(log_q, n);
            for (int d_processed : divisors_of[gcd_log]) {
                int rem = n / d_processed;
                int reduced_log = log_q / d_processed;
                for (int length : divisors_of[rem]) {
                    if (length <= 1 || std::gcd(reduced_log, length) != 1) continue;
                    int key = d_processed * KEY_BASE + length;
                    auto it = condition_index.find(key);
                    if (it == condition_index.end()) continue;
                    int idx = it->second;
                    if (best_prime[idx] == 0) {
                        best_prime[idx] = q;
                        --remaining;
                        if (remaining == 0) return;
                    }
                }
            }
        }

        cerr << "Prime search limit too small for p=" << p << ", missing " << remaining << " conditions\n";
        exit(1);
    }

    int transition_prime(int d_processed, int length) const {
        int key = d_processed * KEY_BASE + length;
        auto it = condition_index.find(key);
        return best_prime[it->second];
    }

    long double min_log_from(int d_processed) {
        if (d_processed == n) return 0.0L;
        if (seen_log[d_processed]) return memo_log[d_processed];
        seen_log[d_processed] = 1;

        int rem = n / d_processed;
        long double best = numeric_limits<long double>::infinity();
        for (int length : divisors_of[rem]) {
            if (length <= 1) continue;
            int q = transition_prime(d_processed, length);
            long double candidate = (length - 1) * log10l(static_cast<long double>(q)) +
                                    min_log_from(d_processed * length);
            best = min(best, candidate);
        }
        memo_log[d_processed] = best;
        return best;
    }

    unsigned long long min_exact_from(int d_processed) {
        if (d_processed == n) return 1;
        if (seen_exact[d_processed]) return memo_exact[d_processed];
        seen_exact[d_processed] = 1;

        int rem = n / d_processed;
        long double best_log = numeric_limits<long double>::infinity();
        unsigned long long best_value = 0;
        for (int length : divisors_of[rem]) {
            if (length <= 1) continue;
            int q = transition_prime(d_processed, length);
            long double candidate_log = (length - 1) * log10l(static_cast<long double>(q)) +
                                        min_log_from(d_processed * length);
            unsigned long long candidate_value = pow_int(q, length - 1) * min_exact_from(d_processed * length);
            if (best_value == 0 || candidate_log < best_log - 1e-18L ||
                (fabsl(candidate_log - best_log) <= 1e-18L && candidate_value < best_value)) {
                best_log = candidate_log;
                best_value = candidate_value;
            }
        }

        memo_exact[d_processed] = best_value;
        return best_value;
    }
};

static long double log_s(int p) {
    if (p == 2) return 0.0L;
    SolverForPrime solver(p);
    return solver.min_log_from(1);
}

static unsigned long long exact_s(int p) {
    if (p == 2) return 1;
    SolverForPrime solver(p);
    return solver.min_exact_from(1);
}

static string scientific(long double log10_value) {
    long long exponent = static_cast<long long>(floorl(log10_value));
    long double mantissa = powl(10.0L, log10_value - exponent);
    long double rounded = floorl(mantissa * 100000.0L + 0.5L) / 100000.0L;
    if (rounded >= 10.0L) {
        rounded /= 10.0L;
        ++exponent;
    }

    ostringstream out;
    out << fixed << setprecision(5) << static_cast<double>(rounded) << 'e' << exponent;
    return out.str();
}

static unsigned long long exact_t(int m) {
    unsigned long long product = 1;
    for (int p : small_primes) {
        if (p >= m) break;
        product *= exact_s(p);
    }
    return product;
}

static long double log_t(int m) {
    long double total = 0.0L;
    for (int p : small_primes) {
        if (p >= m) break;
        total += log_s(p);
    }
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    primes = sieve_primes(PRIME_SEARCH_LIMIT);
    for (int p : primes) {
        if (p >= TARGET_M) break;
        small_primes.push_back(p);
    }

    cout << "T(20) = " << exact_t(20) << " (expected 1348422598656)\n";
    cout << "T(100) = " << scientific(log_t(100)) << " (expected about 1.37451e123)\n";
    cout << scientific(log_t(TARGET_M)) << '\n';

    return 0;
}
