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
    // Collect all distinct (dL, dR) transitions and also 
    // check if the width constraint is simply >= 2 for interior rows
    
    for (N = 4; N <= 5; N++) {
        int total = N * N;
        set<pair<int,int>> all_transitions;
        int valid_count = 0;
        
        // Also check: are all valid sets just described by row ranges
        // where adjacent rows have width >= 2?
        // And the minimum width overall is >= 2 for multi-row sets?
        
        // Also: check if all sets span contiguous rows
        // And check minimum row width
        int min_width_seen = 999;
        
        for (long long mask = 1; mask < (1LL << total); mask++) {
            if (__builtin_popcountll(mask) <= 1) continue;
            if (!check(mask)) continue;
            valid_count++;
            
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
            
            for (int r = rmin; r <= rmax; r++) {
                int w = R[r] - L[r] + 1;
                if (w < min_width_seen) min_width_seen = w;
            }
            
            for (int r = rmin; r < rmax; r++) {
                int dL = L[r+1] - L[r];
                int dR = R[r+1] - R[r];
                all_transitions.insert({dL, dR});
            }
        }
        
        printf("=== N=%d: %d valid non-singleton sets ===\n", N, valid_count);
        printf("Min width across all rows: %d\n", min_width_seen);
        printf("All (dL, dR) transitions:\n");
        for (auto& [a,b] : all_transitions) {
            printf("  (%d, %d)\n", a, b);
        }
        printf("\n");
    }
    
    return 0;
}
