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

void print_grid(long long mask) {
    for (int r = 0; r < N; r++) {
        printf("  ");
        for (int c = 0; c < N; c++) {
            int i = r * N + c;
            printf("%c ", (mask & (1LL << i)) ? '#' : '.');
        }
        printf("\n");
    }
}

int main() {
    // Visualize valid sets for N=4
    N = 4;
    {
        int total = N * N;
        int count = 0;
        printf("=== N=%d: All non-singleton valid sets (grid view) ===\n\n", N);
        for (long long mask = 1; mask < (1LL << total); mask++) {
            if (__builtin_popcountll(mask) <= 1) continue;
            if (check(mask)) {
                printf("Set #%d (size=%d):\n", ++count, __builtin_popcountll(mask));
                print_grid(mask);
                printf("\n");
            }
        }
    }
    
    // For N=5, just look at the row-ranges of each valid set
    // for each valid set, find min_col[r], max_col[r] for each row r
    N = 5;
    {
        int total = N * N;
        printf("\n=== N=%d: Non-singleton valid sets (grid view, first 20) ===\n\n", N);
        int count = 0;
        // Also count how many are "convex" (each row is a contiguous range)
        int convex_count = 0;
        int total_nonsingleton = 0;
        
        for (long long mask = 1; mask < (1LL << total); mask++) {
            if (__builtin_popcountll(mask) <= 1) continue;
            if (!check(mask)) continue;
            total_nonsingleton++;
            
            // Check if each row is a contiguous range
            bool convex = true;
            for (int r = 0; r < N && convex; r++) {
                int first = -1, last = -1;
                for (int c = 0; c < N; c++) {
                    if (mask & (1LL << (r*N+c))) {
                        if (first == -1) first = c;
                        last = c;
                    }
                }
                if (first == -1) continue;
                for (int c = first; c <= last; c++) {
                    if (!(mask & (1LL << (r*N+c)))) {
                        convex = false;
                        break;
                    }
                }
            }
            if (convex) convex_count++;
            
            if (count < 20) {
                printf("Set #%d (size=%d, convex=%s):\n", count+1, __builtin_popcountll(mask), convex ? "yes" : "no");
                print_grid(mask);
                printf("\n");
            }
            count++;
        }
        printf("Total non-singleton: %d, convex: %d\n", total_nonsingleton, convex_count);
    }
    
    return 0;
}
