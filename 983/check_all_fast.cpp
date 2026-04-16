#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <algorithm>

using namespace std;

struct Point {
    long long x, y;
    bool operator<(const Point& o) const {
        if (x != o.x) return x < o.x;
        return y < o.y;
    }
};

bool check_r2(long long r2) {
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
    
    if (pts.size() < 20) return false;
    
    vector<Point> vectors;
    set<Point> seen;
    for (auto p : pts) {
        if (!seen.count(p) && !seen.count({-p.x, -p.y})) {
            vectors.push_back(p);
            seen.insert(p);
        }
    }
    
    if (vectors.size() < 10) return false;
    
    set<Point> D;
    for (auto u : pts) {
        for (auto v : pts) {
            D.insert({u.x - v.x, u.y - v.y});
        }
    }
    
    cout << "Checking R^2=" << r2 << " points=" << pts.size() << " vectors=" << vectors.size() << endl;
    
    int n = vectors.size();
    vector<int> comb(10);
    for (int i = 0; i < 10; ++i) comb[i] = i;
    
    while (true) {
        // Build array of chosen vectors
        vector<Point> chosen(10);
        for(int i=0; i<10; ++i) chosen[i] = vectors[comb[i]];
        
        bool valid = true;
        auto dfs = [&](auto& self, int idx, long long cx, long long cy, int nnz) -> bool {
            if (idx == 10) {
                if (nnz >= 4 && nnz % 2 == 0) {
                    if (D.count({cx, cy})) return false;
                }
                return true;
            }
            if (!self(self, idx+1, cx, cy, nnz)) return false;
            if (!self(self, idx+1, cx+chosen[idx].x, cy+chosen[idx].y, nnz+1)) return false;
            if (!self(self, idx+1, cx-chosen[idx].x, cy-chosen[idx].y, nnz+1)) return false;
            return true;
        };
        
        if (dfs(dfs, 0, 0, 0, 0)) {
            cout << "FOUND PERFECT SET! R^2=" << r2 << endl;
            return true;
        }
        
        int i = 9;
        while (i >= 0 && comb[i] == n - 10 + i) i--;
        if (i < 0) break;
        comb[i]++;
        for (int j = i + 1; j < 10; ++j) comb[j] = comb[j-1] + 1;
    }
    return false;
}

int main() {
    for (long long r2 = 5000; r2 <= 15000; ++r2) {
        long long limit = std::sqrt(r2);
        long long cnt = 0;
        for (long long dx = -limit; dx <= limit; ++dx) {
            long long dy2 = r2 - dx * dx;
            if (dy2 < 0) continue;
            long long dy = std::sqrt(dy2);
            if (dy * dy == dy2) {
                cnt++;
                if (dy != 0) cnt++;
            }
        }
        if (cnt >= 20) {
            if (check_r2(r2)) {
                cout << "MINIMUM IS " << r2 << endl;
                return 0;
            }
        }
    }
    return 0;
}
