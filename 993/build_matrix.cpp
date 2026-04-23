#include <iostream>
#include <vector>
#include <fstream>
#include <cassert>

using namespace std;

const long long P = 1000000007;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= P;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % P;
        base = (base * base) % P;
        exp /= 2;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, P - 2);
}

int main() {
    ifstream fin("bb_values.txt");
    vector<long long> V;
    long long x, y;
    while (fin >> x >> y) {
        if (x != V.size()) {
            cout << "Error reading file!" << endl;
            return 1;
        }
        V.push_back(y);
    }
    fin.close();
    
    int L = 400; // to keep 2^8 * 400 < 100000
    int max_e = 7;
    
    vector<vector<long long>> seqs;
    vector<pair<int, int>> seq_info;
    
    // In Python we added affine terms. To be exactly equivalent and keep rank stable:
    // Actually, V[N] being exact 2-regular implies that affine terms aren't necessary if the rank
    // includes V, but let's safely add the constant 1 sequence manually just in case.
    vector<long long> ones(L, 1);
    seqs.push_back(ones);
    seq_info.push_back({-1, -1}); // dummy marker for 1 sequence
    
    for (int e = 0; e <= max_e; e++) {
        for (int a = 0; a < (1 << e); a++) {
            vector<long long> sub(L);
            for (int n = 0; n < L; n++) {
                sub[n] = (V[(1<<e)*n + a] % P + P) % P;
            }
            seqs.push_back(sub);
            seq_info.push_back({e, a});
        }
    }
    
    int num_seqs = seqs.size();
    vector<int> basis;
    vector<vector<long long>> row_reduced; // to keep triangular form
    vector<vector<long long>> basis_orig;
    
    vector<vector<long long>> relations(num_seqs);
    
    for (int i = 0; i < num_seqs; i++) {
        vector<long long> cur = seqs[i];
        vector<long long> coeffs(basis.size(), 0);
        
        bool is_indep = false;
        
        for (int j = 0; j < (int)basis.size(); j++) {
            int pivot = -1;
            for(int c=0; c<L; c++) if(row_reduced[j][c] != 0) { pivot = c; break; }
            
            if (pivot != -1 && cur[pivot] != 0) {
                long long factor = (cur[pivot] * modInverse(row_reduced[j][pivot])) % P;
                coeffs[j] = factor;
                for (int c = pivot; c < L; c++) {
                    cur[c] = (cur[c] - factor * row_reduced[j][c]) % P;
                    if (cur[c] < 0) cur[c] += P;
                }
            }
        }
        
        for (int c = 0; c < L; c++) {
            if (cur[c] != 0) {
                is_indep = true;
                break;
            }
        }
        
        if (is_indep) {
            basis.push_back(i);
            row_reduced.push_back(cur);
            basis_orig.push_back(seqs[i]);
            vector<long long> self_rel(basis.size(), 0);
            self_rel.back() = 1;
            relations[i] = self_rel;
        } else {
            relations[i] = coeffs;
        }
    }
    
    cout << "Rank: " << basis.size() << endl;
    
    int d = basis.size();
    vector<vector<long long>> M0(d, vector<long long>(d, 0));
    vector<vector<long long>> M1(d, vector<long long>(d, 0));
    
    bool ok = true;
    for (int i = 0; i < d; i++) {
        int idx = basis[i];
        int e = seq_info[idx].first;
        int a = seq_info[idx].second;
        
        if (e == -1) {
            // This is the sequence of 1s. F(2n) = 1, F(2n+1) = 1
            // So M0 and M1 for this row is just 1 for the 1s basis vector
            // Which idx corresponds to 1s? It's basis[0] (which is idx 0).
            M0[i][0] = 1;
            M1[i][0] = 1;
            continue;
        }
        
        int idx0 = -1, idx1 = -1;
        for (int j=0; j<num_seqs; j++) {
            if (seq_info[j].first == e+1 && seq_info[j].second == a) idx0 = j;
            if (seq_info[j].first == e+1 && seq_info[j].second == a + (1<<e)) idx1 = j;
        }
        
        if (idx0 == -1 || idx1 == -1) {
            cout << "ERROR: basis sequence e=" << e << ", a=" << a << " could not find e+1 derivatives." << endl;
            ok = false;
        } else {
            M0[i] = relations[idx0];
            M1[i] = relations[idx1];
        }
    }
    
    if (!ok) return 1;
    
    ofstream fout("eval.py");
    fout << "P = 1000000007\n";
    fout << "M0 = " << "[\n";
    for(int i=0; i<d; i++) {
        fout << "[";
        for(int j=0; j<d; j++) fout << M0[i][j] << ",";
        fout << "],\n";
    }
    fout << "]\n";
    
    fout << "M1 = " << "[\n";
    for(int i=0; i<d; i++) {
        fout << "[";
        for(int j=0; j<d; j++) fout << M1[i][j] << ",";
        fout << "],\n";
    }
    fout << "]\n";
    
    fout << "F0 = [";
    for(int i=0; i<d; i++) {
        int idx = basis[i];
        if (seq_info[idx].first == -1) fout << 1 << ",";
        else fout << V[seq_info[idx].second] << ",";
    }
    fout << "]\n";
    
    fout.close();
    cout << "Generated eval.py" << endl;
    return 0;
}
