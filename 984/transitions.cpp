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
    // For each valid non-singleton set, extract the boundary profile
    // and look at the constraints on L[r], R[r] transitions
    
    for (N = 4; N <= 5; N++) {
        int total = N * N;
        printf("=== N=%d ===\n", N);
        
        // Collect all boundary transitions
        map<string, int> transition_counts;
        
        for (long long mask = 1; mask < (1LL << total); mask++) {
            if (__builtin_popcountll(mask) <= 1) continue;
            if (!check(mask)) continue;
            
            // Extract L[r], R[r]
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
            
            // Check the row-to-row transitions
            // For each pair of adjacent rows, compute:
            // dL = L[r+1] - L[r], dR = R[r+1] - R[r]
            // Also check width of each row
            int nrows = rmax - rmin + 1;
            
            printf("Set: rows [%d,%d], widths: ", rmin, rmax);
            for (int r = rmin; r <= rmax; r++) {
                printf("%d", R[r]-L[r]+1);
                if (r < rmax) printf(",");
            }
            printf("  L: ");
            for (int r = rmin; r <= rmax; r++) {
                printf("%d", L[r]);
                if (r < rmax) printf(",");
            }
            printf("  R: ");
            for (int r = rmin; r <= rmax; r++) {
                printf("%d", R[r]);
                if (r < rmax) printf(",");
            }
            
            // Also check: is the row span contiguous (no empty rows in between)?
            bool contiguous_rows = true;
            for (int r = rmin; r <= rmax; r++) {
                if (L[r] == -1) { contiguous_rows = false; break; }
            }
            
            if (nrows >= 2) {
                printf("  dL,dR: ");
                for (int r = rmin; r < rmax; r++) {
                    printf("(%d,%d)", L[r+1]-L[r], R[r+1]-R[r]);
                }
            }
            
            printf("\n");
        }
        printf("\n");
    }
    
    return 0;
}
