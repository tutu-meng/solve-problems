#include <stdio.h>
#include <stdlib.h>

long long V[200000];
int V_len = 0;

int main() {
    FILE *f = fopen("bb_values.txt", "r");
    if (!f) return 1;
    long long n, v;
    while (fscanf(f, "%lld %lld", &n, &v) == 2) {
        V[V_len++] = v;
    }
    fclose(f);
    
    printf("Loaded %d values.\n", V_len);
    
    for (int p = 1; p <= 5000; p++) {
        for (int start = 0; start < V_len - 100 * p; start++) {
            int constant = 1;
            long long diff = V[start + p] - V[start];
            for (int i = start; i < V_len - p; i++) {
                if (V[i + p] - V[i] != diff) {
                    constant = 0;
                    break;
                }
            }
            if (constant) {
                printf("Found period P=%d, shift=%d, diff=%lld\n", p, start, diff);
                return 0;
            }
        }
    }
    printf("No period found up to P=5000\n");
    return 0;
}
