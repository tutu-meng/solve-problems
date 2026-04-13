#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <queue>
#include <utility>
#include <vector>
#include <map>
#include <set>
using namespace std;

int N;
int knight_dx[] = {-2,-2,-1,-1,1,1,2,2};
int knight_dy[] = {-1,1,-2,2,-2,2,-1,1};

pair<int,int> get_block(int r, int c, int d) {
    int dx = knight_dx[d], dy = knight_dy[d];
    if (abs(dx) == 2) {
        return {r + (dx > 0 ? 1 : -1), c};
    } else {
        return {r, c + (dy > 0 ? 1 : -1)};
    }
}

bool check(long long mask) {
    for (int i = 0; i < N*N; i++) {
        if (!(mask & (1LL << i))) continue;
        int r = i / N, c = i % N;
        for (int d = 0; d < 8; d++) {
            int nr = r + knight_dx[d], nc = c + knight_dy[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= N) continue;
            int j = nr * N + nc;
            if (!(mask & (1LL << j))) continue;
            auto [br, bc] = get_block(r, c, d);
            int bk = br * N + bc;
            if (!(mask & (1LL << bk))) return false;
        }
    }
    
    int start = __builtin_ctzll(mask);
    int set_size = __builtin_popcountll(mask);
    long long visited = 1LL << start;
    int visited_count = 1;
    queue<int> q;
    q.push(start);
    while (!q.empty()) {
        int cur = q.front(); q.pop();
        int r = cur / N, c = cur % N;
        for (int d = 0; d < 8; d++) {
            int nr = r + knight_dx[d], nc = c + knight_dy[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= N) continue;
            int j = nr * N + nc;
            if ((mask & (1LL << j)) && !(visited & (1LL << j))) {
                visited |= (1LL << j);
                visited_count++;
                q.push(j);
            }
        }
    }
    return visited_count == set_size;
}

int main() {
    // For valid non-singleton sets: 
    // 1. Check: is every row width >= 2?
    // 2. Check the exact constraints on (L[r-1],R[r-1]) -> (L[r],R[r]) -> (L[r+1],R[r+1])
    //    for the horse-disjoint condition involving 2-row knight moves.
    
    for (N = 4; N <= 5; N++) {
        int total = N * N;
        printf("=== N=%d ===\n", N);
        
        // Check if any valid set has a row width of 1
        int count_width_1 = 0;
        int count_total = 0;
        
        // Check the constraint pattern more carefully
        // For each triple of consecutive rows (r-1, r, r+1),
        // what constraints exist?
        
        for (long long mask = 1; mask < (1LL << total); mask++) {
            if (__builtin_popcountll(mask) <= 1) continue;
            if (!check(mask)) continue;
            count_total++;
            
            int rmin = -1, rmax = -1;
            int L[10], R[10];
            memset(L, -1, sizeof(L));
            memset(R, -1, sizeof(R));
            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N; c++) {
                    if (mask & (1LL << (r*N+c))) {
                        if (L[r] == -1) L[r] = c;
                        R[r] = c;
                        if (rmin == -1) rmin = r;
                        rmax = r;
                    }
                }
            }
            
            bool has_width_1 = false;
            for (int r = rmin; r <= rmax; r++) {
                if (R[r] - L[r] + 1 == 1) has_width_1 = true;
            }
            if (has_width_1) {
                count_width_1++;
                printf("Width-1 set: ");
                for (int r = rmin; r <= rmax; r++) {
                    printf("[%d,%d] ", L[r], R[r]);
                }
                printf("\n");
            }
        }
        
        printf("Total valid: %d, with width-1 row: %d\n\n", count_total, count_width_1);
    }
    
    return 0;
}
