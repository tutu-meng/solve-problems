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

// Check knight connectivity for a convex shape given by intervals
bool check_connectivity(int h, int* L, int* R) {
    // Build the knight graph and check connectivity
    // Total squares
    vector<pair<int,int>> squares;
    map<pair<int,int>, int> sq_id;
    
    for (int r = 0; r < h; r++) {
        for (int c = L[r]; c <= R[r]; c++) {
            sq_id[{r,c}] = squares.size();
            squares.push_back({r,c});
        }
    }
    
    int n = squares.size();
    if (n <= 1) return true;
    
    vector<vector<int>> adj(n);
    for (int i = 0; i < n; i++) {
        auto [r, c] = squares[i];
        for (int d = 0; d < 8; d++) {
            int nr = r + knight_dx[d], nc = c + knight_dy[d];
            auto it = sq_id.find({nr, nc});
            if (it != sq_id.end()) {
                adj[i].push_back(it->second);
            }
        }
    }
    
    vector<bool> visited(n, false);
    queue<int> q;
    q.push(0);
    visited[0] = true;
    int cnt = 1;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                cnt++;
                q.push(v);
            }
        }
    }
    return cnt == n;
}

bool check_1row(int L0, int R0, int L1, int R1) {
    // (r,c) <-> (r+1,c+2)
    {
        int lo = max(L0, L1-2), hi = min(R0, R1-2);
        if (lo <= hi) {
            if (R1 > R0+1) return false;
            if (L1 > L0+1) return false;
        }
    }
    // (r,c) <-> (r+1,c-2)
    {
        int lo = max(L0, L1+2), hi = min(R0, R1+2);
        if (lo <= hi) {
            if (L0 > L1+1) return false;
            if (R0 > R1+1) return false;
        }
    }
    return true;
}

bool check_2row(int L0, int R0, int L1, int R1, int L2, int R2) {
    {
        int lo = max(L0, L2-1), hi = min(R0, R2-1);
        if (lo <= hi) {
            if (lo < L1 || hi > R1-1) return false;
        }
    }
    {
        int lo = max(L0, L2+1), hi = min(R0, R2+1);
        if (lo <= hi) {
            if (lo < L1+1 || hi > R1) return false;
        }
    }
    return true;
}

int main() {
    // For small N, enumerate horse-disjoint convex shapes AND check connectivity.
    // Compare with brute force.
    
    for (N = 2; N <= 7; N++) {
        long long count_singletons = (long long)N * N;
        long long count_hd_connected = 0;
        
        // For each height h from 2 to N, enumerate all valid shapes.
        // Use DFS/recursion: build the shape row by row.
        // At each step, try all possible intervals for the new row.
        
        // To avoid O(N^6) per height, use DP.
        // But also need connectivity check at the end.
        
        // For small N, just enumerate all shapes and check connectivity.
        // Shape: rows 0..h-1 with intervals [L[r], R[r]] in [0, N-1].
        
        struct ShapeState {
            int h;
            int L[20], R[20];
        };
        
        // DFS
        function<void(int, int*, int*)> dfs = [&](int depth, int* L, int* R) {
            if (depth >= 2) {
                // This is a valid shape of height `depth`.
                // Check connectivity.
                if (check_connectivity(depth, L, R)) {
                    long long vert = N - depth + 1;
                    count_hd_connected += vert;
                }
            }
            
            if (depth >= N) return; // can't add more rows
            
            // Try adding a new row with interval [Ln, Rn]
            for (int Ln = 0; Ln < N; Ln++) {
                for (int Rn = Ln; Rn < N; Rn++) {
                    bool ok = true;
                    if (depth >= 1) {
                        if (!check_1row(L[depth-1], R[depth-1], Ln, Rn)) ok = false;
                    }
                    if (depth >= 2 && ok) {
                        if (!check_2row(L[depth-2], R[depth-2], L[depth-1], R[depth-1], Ln, Rn)) ok = false;
                    }
                    if (ok) {
                        L[depth] = Ln;
                        R[depth] = Rn;
                        dfs(depth + 1, L, R);
                    }
                }
            }
        };
        
        int L[20], R[20];
        // Start with each possible first row
        for (int L0 = 0; L0 < N; L0++) {
            for (int R0 = L0; R0 < N; R0++) {
                L[0] = L0;
                R[0] = R0;
                dfs(1, L, R);
            }
        }
        
        printf("f(%d) = %lld (HD+connected convex multi-row + singletons)\n", N, count_hd_connected + count_singletons);
    }
    
    return 0;
}
