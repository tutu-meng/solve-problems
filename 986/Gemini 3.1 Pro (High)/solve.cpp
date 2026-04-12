#pragma GCC optimize("O3,unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
#include <iostream>

using namespace std;

long long gcd(long long a, long long b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}

int state_map[12000000];
int OFFSET = 0;
int global_min_p_seen = 0;

bool check_T(long long c, long long d, long long T, int cutoff) {
    state_map[OFFSET] = T;
    
    int p = OFFSET;
    int min_p_seen = OFFSET;
    
    while (p >= min_p_seen) {
        long long val = state_map[p];
        if (val >= 2) {
            long long num = val / 2;
            state_map[p] = val % 2;
            
            int p1 = p - d;
            int p2 = p - c - d;
            
            state_map[p1] += num;
            state_map[p2] += num;
            
            if (p2 < min_p_seen) {
                min_p_seen = p2;
                if (min_p_seen < cutoff) {
                    for (int i = min_p_seen; i <= OFFSET; i++) state_map[i] = 0;
                    return false;
                }
            }
        }
        p--;
    }
    
    bool valid = true;
    for (int i = min_p_seen; i <= OFFSET; i++) {
        if (state_map[i] >= 2) { valid = false; break; }
    }
    for (int i = min_p_seen; i <= OFFSET; i++) {
        state_map[i] = 0;
    }
    global_min_p_seen = min_p_seen;
    return valid;
}

long long G(long long c, long long d) {
    long long low = 1;
    long long high = 1;
    OFFSET = 11000000;
    int cutoff = 1000;
    
    while (check_T(c, d, high, cutoff)) {
        high *= 2;
    }
    long long ans = 1;
    while (low <= high) {
        long long mid = low + (high - low) / 2;
        if (check_T(c, d, mid, cutoff)) {
            ans = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    check_T(c, d, ans, cutoff);
    return ans;
}

int main() {
    for(int i=0; i<12000000; i++) state_map[i] = 0;
    cout << "G(1, 160) = " << G(1, 160) << " min_p_seen=" << OFFSET - global_min_p_seen << endl;
    cout << "G(160, 160) = " << G(160, 160) << " min_p_seen=" << OFFSET - global_min_p_seen << endl;
    
    long long sum = 0;
    for (int c = 1; c <= 160; c++) {
        for (int d = 1; d <= 160; d++) {
            if (gcd(c, d) == 1) sum += G(c, d);
        }
    }
    cout << "FINAL: " << sum << endl;
    return 0;
}
