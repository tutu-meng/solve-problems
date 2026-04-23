#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Use a hash map for banana positions
// Since positions tend to be in a range, use an offset array
#define MAX_POS 200000
#define OFFSET 50000

char bananas[MAX_POS]; // bananas[pos + OFFSET] = 1 if banana at pos

long long simulate(long long N) {
    memset(bananas, 0, sizeof(bananas));
    long long pos = 0;
    long long carry = N;
    
    while (1) {
        long long x = pos;
        int idx = (int)(x + OFFSET);
        int idx1 = (int)(x + 1 + OFFSET);
        
        int has_x = (idx >= 0 && idx < MAX_POS) ? bananas[idx] : 0;
        int has_x1 = (idx1 >= 0 && idx1 < MAX_POS) ? bananas[idx1] : 0;
        
        if (has_x && has_x1) {
            bananas[idx1] = 0;
            carry++;
            pos = x - 1;
        } else if (has_x && !has_x1) {
            bananas[idx] = 0;
            carry++;
            pos = x + 2;
        } else if (!has_x && has_x1) {
            bananas[idx1] = 0;
            bananas[idx] = 1;
            pos = x + 2;
        } else {
            if (carry >= 3) {
                int idx_m1 = (int)(x - 1 + OFFSET);
                bananas[idx_m1] = 1;
                bananas[idx] = 1;
                bananas[idx1] = 1;
                carry -= 3;
                pos = x - 2;
            } else {
                return pos;
            }
        }
    }
}

int main() {
    // Verify
    printf("BB(1000) = %lld\n", simulate(1000));
    
    // Compute for many values
    FILE* f = fopen("bb_values.txt", "w");
    for (long long n = 0; n <= 100000; n++) {
        long long bb = simulate(n);
        fprintf(f, "%lld %lld\n", n, bb);
        if (n % 10000 == 0) {
            printf("BB(%lld) = %lld, ratio=%.6f\n", n, bb, n > 0 ? (double)bb/n : 0.0);
        }
    }
    fclose(f);
    
    return 0;
}
