#include <iostream>
#include <vector>
#include <set>
#include <cmath>

using namespace std;

struct Point {
    long long x, y;
    bool operator<(const Point& o) const {
        if (x != o.x) return x < o.x;
        return y < o.y;
    }
};

int main(int argc, char** argv) {
    long long r2 = 5525;
    if (argc > 1) r2 = std::stoll(argv[1]);
    
    vector<Point> pts;
    long long limit = std::sqrt(r2);
    for (long long dx = -limit; dx <= limit; ++dx) {
        long long dy2 = r2 - dx * dx;
        if (dy2 < 0) continue;
        long long dy = std::sqrt(dy2);
        if (dy * dy == dy2) {
            pts.push_back({dx, dy});
            if (dy != 0) pts.push_back({dx, -dy});
        }
    }
    
    vector<Point> vectors;
    set<Point> seen;
    for (auto p : pts) {
        if (!seen.count(p) && !seen.count({-p.x, -p.y})) {
            vectors.push_back(p);
            seen.insert(p);
        }
    }
    
    set<Point> D;
    for (auto u : pts) {
        for (auto v : pts) {
            D.insert({u.x - v.x, u.y - v.y});
        }
    }
    
    int n = vectors.size();
    vector<int> comb(10);
    for (int i = 0; i < 10; ++i) comb[i] = i;
    
    long long count = 0;
    while (true) {
        // test comb
        bool valid = true;
        auto dfs = [&](auto& self, int idx, long long cx, long long cy, int nnz) -> bool {
            if (idx == 10) {
                if (nnz >= 4 && nnz % 2 == 0) {
                    if (D.count({cx, cy})) return false;
                }
                return true;
            }
            if (!self(self, idx+1, cx, cy, nnz)) return false;
            if (!self(self, idx+1, cx+vectors[comb[idx]].x, cy+vectors[comb[idx]].y, nnz+1)) return false;
            if (!self(self, idx+1, cx-vectors[comb[idx]].x, cy-vectors[comb[idx]].y, nnz+1)) return false;
            return true;
        };
        
        if (dfs(dfs, 0, 0, 0, 0)) {
            cout << "FOUND! R^2=" << r2 << "\n";
            return 0;
        }
        
        count++;
        if (count % 100000 == 0) {
            cout << "Checked " << count << " combinations\n";
        }
        
        // next combination
        int i = 9;
        while (i >= 0 && comb[i] == n - 10 + i) i--;
        if (i < 0) break;
        comb[i]++;
        for (int j = i + 1; j < 10; ++j) comb[j] = comb[j-1] + 1;
    }
    
    cout << "NOT FOUND for R^2=" << r2 << "\n";
    return 0;
}
