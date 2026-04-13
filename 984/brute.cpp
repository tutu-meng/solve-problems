#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <queue>
#include <utility>
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

int main() {
    for (N = 1; N <= 5; N++) {
        int total = N * N;
        long long count = 0;
        
        for (long long mask = 1; mask < (1LL << total); mask++) {
            bool ok = true;
            for (int i = 0; i < total && ok; i++) {
                if (!(mask & (1LL << i))) continue;
                int r = i / N, c = i % N;
                for (int d = 0; d < 8 && ok; d++) {
                    int nr = r + knight_dx[d], nc = c + knight_dy[d];
                    if (nr < 0 || nr >= N || nc < 0 || nc >= N) continue;
                    int j = nr * N + nc;
                    if (!(mask & (1LL << j))) continue;
                    auto [br, bc] = get_block(r, c, d);
                    int bk = br * N + bc;
                    if (!(mask & (1LL << bk))) {
                        ok = false;
                    }
                }
            }
            if (!ok) continue;
            
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
            
            if (visited_count == set_size) {
                count++;
            }
        }
        
        printf("f(%d) = %lld\n", N, count);
    }
    return 0;
}
