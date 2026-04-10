#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cstring>
using namespace std;

const int MAXK = 8;
int N, K;
int words_g[MAXK];

// Compact state: encode intervals as single integers
// For n<=10: each interval (l,r) encoded as l*11+r (max 10*11+10=120, fits in byte)
// State = turn + K intervals = 1 + K bytes

typedef uint64_t StateKey; // enough for k<=7 and n<=10

StateKey encode_state(uint8_t lr[][2], int turn) {
    StateKey key = turn;
    for (int i = 0; i < K; i++) {
        key = key * 121 + lr[i][0] * 11 + lr[i][1];
    }
    return key;
}

unordered_map<StateKey, int8_t> memo; // 0=unknown, 1=Left wins, -1=Right wins

// Returns 1 if Left wins, -1 if Right wins
int minimax(uint8_t lr[][2], int turn) {
    // Terminal check
    bool terminal = true;
    for (int i = 0; i < K; i++) {
        if (lr[i][0] != lr[i][1]) { terminal = false; break; }
    }
    if (terminal) {
        int ls = 0;
        for (int i = 0; i < K; i++) {
            int pos = lr[i][0];
            if (((words_g[i] >> (N - pos)) & 1) == 0) ls++;
        }
        return (ls > K - ls) ? 1 : -1;
    }
    
    StateKey key = encode_state(lr, turn);
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;
    
    // Generate moves using recursive enumeration
    int result;
    if (turn == 0) {
        result = -1; // assume Right wins unless Left finds winning move
    } else {
        result = 1; // assume Left wins unless Right finds winning move
    }
    
    // Enumerate all possible moves recursively
    uint8_t new_lr[MAXK][2];
    for (int i = 0; i < K; i++) {
        new_lr[i][0] = lr[i][0];
        new_lr[i][1] = lr[i][1];
    }
    
    // Use iterative nested loop approach for efficiency
    // For small k, expand loops
    
    // Generic recursive approach
    function<bool(int, bool)> enumerate = [&](int idx, bool any_changed) -> bool {
        if (idx == K) {
            if (!any_changed) return false;
            int val = minimax(new_lr, 1 - turn);
            if (turn == 0 && val == 1) return true; // Left found winning move
            if (turn == 1 && val == -1) return true; // Right found winning move
            return false;
        }
        
        int l = lr[idx][0], r = lr[idx][1];
        if (turn == 0) {
            // Left: advance l to new_l in [l, r]
            for (int nl = l; nl <= r; nl++) {
                new_lr[idx][0] = nl;
                new_lr[idx][1] = r;
                if (enumerate(idx + 1, any_changed || (nl != l))) {
                    new_lr[idx][0] = l; // restore
                    return true;
                }
            }
            new_lr[idx][0] = l; // restore
        } else {
            // Right: retreat r to new_r in [l, r]
            for (int nr = l; nr <= r; nr++) {
                new_lr[idx][0] = l;
                new_lr[idx][1] = nr;
                if (enumerate(idx + 1, any_changed || (nr != r))) {
                    new_lr[idx][1] = r; // restore
                    return true;
                }
            }
            new_lr[idx][1] = r; // restore
        }
        return false;
    };
    
    bool found = enumerate(0, false);
    if (turn == 0) {
        result = found ? 1 : -1;
    } else {
        result = found ? -1 : 1;
    }
    
    memo[key] = result;
    return result;
}

bool solve_game(int w[], int n, int k) {
    N = n; K = k;
    for (int i = 0; i < k; i++) words_g[i] = w[i];
    memo.clear();
    
    uint8_t lr[MAXK][2];
    for (int i = 0; i < k; i++) {
        lr[i][0] = 1;
        lr[i][1] = n;
    }
    return minimax(lr, 0) == -1; // true = Right wins
}

long long factorial(int n) {
    long long r = 1;
    for (int i = 2; i <= n; i++) r *= i;
    return r;
}

long long G_compute(int n, int k, int reps[], int sizes[], int num_types) {
    long long total = 0;
    // Iterate over multisets of types (combinations with replacement)
    vector<int> combo(k, 0);
    
    function<void(int, int)> gen = [&](int idx, int start) {
        if (idx == k) {
            int ws[MAXK];
            for (int i = 0; i < k; i++) ws[i] = reps[combo[i]];
            bool rw = solve_game(ws, n, k);
            if (rw) {
                int cnt[256] = {};
                for (int i = 0; i < k; i++) cnt[combo[i]]++;
                long long ord = factorial(k);
                for (int i = 0; i < num_types; i++) {
                    ord /= factorial(cnt[i]);
                }
                long long sf = 1;
                for (int i = 0; i < k; i++) sf *= sizes[combo[i]];
                total += ord * sf;
            }
            return;
        }
        for (int t = start; t < num_types; t++) {
            combo[idx] = t;
            gen(idx + 1, t);
        }
    };
    
    gen(0, 0);
    return total;
}

int main() {
    // Verify known values
    {
        // n=2, 3 types: sizes [2, 1, 1], reps [0(LL), 1(LR), 3(RR)]
        int reps[] = {0, 1, 3};
        int sizes[] = {2, 1, 1};
        cout << "G(2,3) = " << G_compute(2, 3, reps, sizes, 3) << " (exp 14)" << endl;
        cout << "G(2,5) = " << G_compute(2, 5, reps, sizes, 3) << " (exp 182)" << endl;
    }
    {
        // n=4, 8 types
        int reps[] = {0, 5, 1, 3, 7, 9, 11, 15};
        int sizes[] = {8, 2, 1, 1, 1, 1, 1, 1};
        cout << "G(4,3) = " << G_compute(4, 3, reps, sizes, 8) << " (exp 496)" << endl;
        cout << "G(4,5) = " << G_compute(4, 5, reps, sizes, 8) << " (exp 79274)" << endl;
    }
    {
        // n=6, 18 types
        // Parse words from strings
        auto pw = [](const char* s, int n) {
            int w = 0;
            for (int i = 0; i < n; i++) w = (w << 1) | (s[i] == 'R' ? 1 : 0);
            return w;
        };
        int n = 6;
        int reps[] = {
            pw("LLLLLL",n), pw("LLRRLR",n), pw("LLRLLR",n), pw("LRRLRR",n),
            pw("LLLRRR",n), pw("LRLLLR",n), pw("LLLLLR",n), pw("LLLLRR",n),
            pw("LLLRLR",n), pw("LLRRRR",n), pw("LRLRRR",n), pw("LRRRRR",n),
            pw("RLLLLR",n), pw("RLLRLR",n), pw("RLRLRR",n), pw("RLRRRR",n),
            pw("RRLRRR",n), pw("RRRRRR",n)
        };
        int sizes[] = {32, 8, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
        cout << "G(6,3) = " << G_compute(6, 3, reps, sizes, 18) << " (exp 20490)" << endl;
        cout << "Computing G(6,5)..." << flush;
        cout << " G(6,5) = " << G_compute(6, 5, reps, sizes, 18) << endl;
    }
    
    return 0;
}
