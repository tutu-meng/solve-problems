#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

typedef long long ll;

struct Point {
    ll x, z, g;
};

bool comparePoints(const Point& a, const Point& b) {
    if (a.x != b.x) return a.x < b.x;
    return a.z < b.z;
}

ll F(ll a, ll b) {
    vector<Point> G;
    for (ll x = 1; x <= b - 1; ++x) {
        for (ll z = 1; z <= a - 1; ++z) {
            if (a * x > b * z) {
                ll g = x * a - z * b;
                G.push_back({x, z, g});
            }
        }
    }
    
    sort(G.begin(), G.end(), comparePoints);
    
    int n = G.size();
    vector<ll> dp_count(n, 0);
    vector<ll> dp_sum(n, 0);
    
    ll total_sum = 0;
    
    for (int i = 0; i < n; ++i) {
        ll count = 1; 
        ll sum = G[i].g;
        
        for (int j = 0; j < i; ++j) {
            if (G[j].x < G[i].x && G[j].z < G[i].z) {
                count += dp_count[j];
                sum += dp_sum[j] + G[i].g * dp_count[j];
            }
        }
        
        dp_count[i] = count;
        dp_sum[i] = sum;
        
        total_sum += sum;
    }
    
    return total_sum;
}

int main() {
    cout << "F(3, 5) = " << F(3, 5) << " (expected 23)" << endl;
    cout << "F(5, 13) = " << F(5, 13) << " (expected 16336)" << endl;
    cout << "F(19, 53) = " << F(19, 53) << endl;
    return 0;
}
