#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <queue>
#include <utility>
#include <vector>
#include <map>
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
    // Check horse-disjoint
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
    
    // Check knight-connected
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
    // Enumerate valid sets for small N to understand structure
    for (N = 4; N <= 5; N++) {
        int total = N * N;
        map<int, long long> by_size; // count by set size
        vector<long long> valid_sets;
        
        for (long long mask = 1; mask < (1LL << total); mask++) {
            if (check(mask)) {
                int sz = __builtin_popcountll(mask);
                by_size[sz]++;
                valid_sets.push_back(mask);
            }
        }
        
        printf("=== f(%d) = %d ===\n", N, (int)valid_sets.size());
        printf("By set size:\n");
        for (auto& [sz, cnt] : by_size) {
            printf("  size %d: %lld\n", sz, cnt);
        }
        
        // Print some valid sets with size > 1
        if (N <= 5) {
            printf("Non-singleton sets:\n");
            int printed = 0;
            for (long long mask : valid_sets) {
                int sz = __builtin_popcountll(mask);
                if (sz <= 1) continue;
                if (printed >= 50) { printf("  ... (more)\n"); break; }
                printf("  {");
                bool first = true;
                for (int i = 0; i < total; i++) {
                    if (mask & (1LL << i)) {
                        if (!first) printf(",");
                        printf("(%d,%d)", i/N, i%N);
                        first = false;
                    }
                }
                printf("}\n");
                printed++;
            }
        }
        printf("\n");
    }
    return 0;
}
