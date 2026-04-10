#pragma GCC optimize("O3,unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

long long gcd(long long a, long long b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}

int state_map[13000000];
int OFFSET = 0;

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
        if (state_map[i] >= 2) { valid = false; }
        state_map[i] = 0;
    }
    return valid;
}

long long G(long long c, long long d) {
    long long low = 1;
    long long high = 1;
    OFFSET = 12000000;
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
    return ans;
}

int main() {
    for(int i=0; i<13000000; i++) state_map[i] = 0;
    
    vector<long long> G1(245, 0);
    vector<long long> Gc1(165, 0);
    
    cout << "Computing G(1, k)..." << endl;
    for (int k = 1; k <= 240; k++) {
        G1[k] = G(1, k);
    }
    
    cout << "Computing G(c, 1)..." << endl;
    for (int c = 1; c <= 160; c++) {
        Gc1[c] = G(c, 1);
    }
    
    long long dp_G[161][161] = {0};
    long long sum = 0;
    long long total_mismatch = 0;
    
    for (int c = 1; c <= 160; c++) {
        for (int d = 1; d <= 160; d++) {
            long long g = gcd(c, d);
            int cp = c / g;
            int dp = d / g;
            
            long long val = 0;
            if (dp >= 2) {
                val = G1[dp + (cp - 1) / 2];
            } else { // dp == 1
                val = Gc1[cp];
            }
            dp_G[cp][dp] = val;
            sum += val;
        }
    }
    cout << "FINAL SUM USING PATTERN: " << sum << endl;
    
    // VERIFICATION small grid
    for(int c=1; c<=15; c++) {
        for(int d=1; d<=15; d++) {
            if(gcd(c, d)==1 && d>=2) {
                long long actual = G(c, d);
                long long predicted = G1[d + (c - 1) / 2];
                if(actual != predicted) {
                    cout << "Mismatch c=" << c << " d=" << d << " actual=" << actual << " predicted=" << predicted << endl;
                    total_mismatch++;
                }
            }
        }
    }
    cout << "Verification mismatches (<=15 grid): " << total_mismatch << endl;
    
    return 0;
}
