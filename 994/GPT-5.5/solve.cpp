#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

using i64 = long long;
using u64 = unsigned long long;

static constexpr i64 MOD = 1000000007LL;
static constexpr i64 INV2 = (MOD + 1) / 2;
static constexpr i64 INV4 = 250000002LL;
static constexpr i64 INV6 = 166666668LL;

// Keep this high enough that the Du Jiao recursion only handles a few
// thousand large quotient states for the target input.
static constexpr int SIEVE_LIMIT = 25000000;

struct Prefix {
    uint32_t f0;
    uint32_t f1;
    uint32_t f2;
};

static vector<Prefix> pref;
static unordered_map<u64, Prefix> memo;

static inline i64 norm(i64 x) {
    x %= MOD;
    if (x < 0) x += MOD;
    return x;
}

static inline i64 sum_power(int power, u64 n) {
    i64 a = static_cast<i64>(n % MOD);
    if (power == 0) {
        return a;
    }
    if (power == 1) {
        return a * ((a + 1) % MOD) % MOD * INV2 % MOD;
    }
    if (power == 2) {
        return a * ((a + 1) % MOD) % MOD * ((2 * a + 1) % MOD) % MOD * INV6 % MOD;
    }
    // power == 3
    i64 s = a * ((a + 1) % MOD) % MOD * INV2 % MOD;
    return s * s % MOD;
}

static void build_weighted_totient_prefix() {
    pref.assign(SIEVE_LIMIT + 1, Prefix{0, 0, 0});

    vector<int> phi(SIEVE_LIMIT + 1, 0);
    vector<int> primes;
    vector<uint8_t> composite(SIEVE_LIMIT + 1, 0);
    primes.reserve(SIEVE_LIMIT / 10);

    phi[1] = 1;
    for (int i = 1; i <= SIEVE_LIMIT; ++i) {
        if (i > 1 && !composite[i]) {
            primes.push_back(i);
            phi[i] = i - 1;
        }

        i64 x = i % MOD;
        i64 p0 = (pref[i - 1].f0 + static_cast<i64>(phi[i])) % MOD;
        i64 p1 = (pref[i - 1].f1 + static_cast<i64>(phi[i]) * x) % MOD;
        i64 p2 = (pref[i - 1].f2 + static_cast<i64>(phi[i]) * x % MOD * x) % MOD;
        pref[i] = Prefix{static_cast<uint32_t>(p0), static_cast<uint32_t>(p1), static_cast<uint32_t>(p2)};

        for (int p : primes) {
            i64 v = static_cast<i64>(i) * p;
            if (v > SIEVE_LIMIT) break;
            composite[static_cast<int>(v)] = 1;
            if (i % p == 0) {
                phi[static_cast<int>(v)] = phi[i] * p;
                break;
            }
            phi[static_cast<int>(v)] = phi[i] * (p - 1);
        }
    }
}

static inline Prefix subtract_prefix(const Prefix& a, const Prefix& b) {
    return Prefix{
        static_cast<uint32_t>(norm(static_cast<i64>(a.f0) - b.f0)),
        static_cast<uint32_t>(norm(static_cast<i64>(a.f1) - b.f1)),
        static_cast<uint32_t>(norm(static_cast<i64>(a.f2) - b.f2)),
    };
}

static Prefix weighted_totient_prefix(u64 n) {
    if (n <= static_cast<u64>(SIEVE_LIMIT)) {
        return pref[static_cast<size_t>(n)];
    }

    auto it = memo.find(n);
    if (it != memo.end()) {
        return it->second;
    }

    array<i64, 3> res = {
        sum_power(1, n),
        sum_power(2, n),
        sum_power(3, n),
    };

    for (u64 l = 2, r; l <= n; l = r + 1) {
        u64 q = n / l;
        r = n / q;

        Prefix sub = weighted_totient_prefix(q);
        array<i64, 3> weight = {
            norm(sum_power(0, r) - sum_power(0, l - 1)),
            norm(sum_power(1, r) - sum_power(1, l - 1)),
            norm(sum_power(2, r) - sum_power(2, l - 1)),
        };

        res[0] = norm(res[0] - weight[0] * sub.f0);
        res[1] = norm(res[1] - weight[1] * sub.f1);
        res[2] = norm(res[2] - weight[2] * sub.f2);
    }

    Prefix ans{
        static_cast<uint32_t>(res[0]),
        static_cast<uint32_t>(res[1]),
        static_cast<uint32_t>(res[2]),
    };
    memo.emplace(n, ans);
    return ans;
}

static inline i64 choose2(u64 n) {
    i64 a = static_cast<i64>(n % MOD);
    return a * ((a - 1 + MOD) % MOD) % MOD * INV2 % MOD;
}

static inline i64 choose3(u64 n) {
    i64 a = static_cast<i64>(n % MOD);
    return a * ((a - 1 + MOD) % MOD) % MOD * ((a - 2 + MOD) % MOD) % MOD * INV6 % MOD;
}

static i64 concurrent_triples(u64 m, u64 n) {
    u64 m_span = m - 1;
    u64 n_span = n - 1;
    u64 limit = min(m_span, n_span);
    i64 total = 0;

    for (u64 l = 2, r; l <= limit; l = r + 1) {
        u64 a = m_span / l;
        u64 b = n_span / l;
        r = min(m_span / a, n_span / b);

        Prefix right = weighted_totient_prefix(r);
        Prefix left = weighted_totient_prefix(l - 1);
        Prefix block = subtract_prefix(right, left);

        i64 am = static_cast<i64>(a % MOD) * static_cast<i64>(m % MOD) % MOD;
        i64 bn = static_cast<i64>(b % MOD) * static_cast<i64>(n % MOD) % MOD;
        i64 aa = static_cast<i64>(a % MOD) * ((a + 1) % MOD) % MOD * INV2 % MOD;
        i64 bb = static_cast<i64>(b % MOD) * ((b + 1) % MOD) % MOD * INV2 % MOD;

        i64 c0 = am * bn % MOD;
        i64 c1 = norm(-(am * bb % MOD + bn * aa % MOD));
        i64 c2 = aa * bb % MOD;

        i64 contribution = (c0 * block.f0 + c1 * block.f1 + c2 * block.f2) % MOD;
        total += contribution;
        if (total >= MOD) total -= MOD;
    }

    return total;
}

static i64 solve(u64 m, u64 n) {
    i64 cm2 = choose2(m);
    i64 cn2 = choose2(n);
    i64 cm3 = choose3(m);
    i64 cn3 = choose3(n);

    i64 all_triangle_triples = 0;
    all_triangle_triples = (all_triangle_triples + 2 * cm2 % MOD * cn2) % MOD;
    all_triangle_triples = (all_triangle_triples + 2 * cm2 % MOD * cn3) % MOD;
    all_triangle_triples = (all_triangle_triples + 2 * cm3 % MOD * cn2) % MOD;
    all_triangle_triples = (all_triangle_triples + cm3 * cn3) % MOD;

    return norm(all_triangle_triples - concurrent_triples(m, n));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    build_weighted_totient_prefix();
    memo.reserve(200000);

    cout << "T(2, 3) = " << solve(2, 3) << " (expected 8)\n";
    cout << "T(3, 5) = " << solve(3, 5) << " (expected 146)\n";
    cout << "T(12, 23) = " << solve(12, 23) << " (expected 756716)\n";

    constexpr u64 M = 1234ULL * 100000000ULL;
    constexpr u64 N = 2345ULL * 100000000ULL;
    cout << solve(M, N) << '\n';

    return 0;
}
