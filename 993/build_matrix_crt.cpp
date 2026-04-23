#include <iostream>
#include <vector>
#include <fstream>
#include <cassert>
#include <string>

using namespace std;

long long P;

long long power(long long base, long long exp) {
    long long res = 1; base %= P; if(base<0) base += P;
    while(exp>0) { if(exp%2) res=(res*base)%P; base=(base*base)%P; exp/=2; }
    return res;
}
long long modInverse(long long n) { n%=P; if(n<0) n+=P; return power(n, P-2); }

int main(int argc, char** argv) {
    if(argc < 2) return 1;
    P = stoll(argv[1]);
    
    ifstream fin("bb_values.txt");
    vector<long long> V; long long x, y;
    while(fin >> x >> y) V.push_back(y);
    
    int L = 400; int max_e = 7;
    vector<vector<long long>> seqs;
    vector<pair<int, int>> seq_info;
    vector<long long> ones(L, 1); seqs.push_back(ones); seq_info.push_back({-1, -1});
    
    for(int e=0; e<=max_e; e++) {
        for(int a=0; a<(1<<e); a++) {
            vector<long long> sub(L);
            for(int n=0; n<L; n++) sub[n] = (V[(1<<e)*n+a]%P+P)%P;
            seqs.push_back(sub);
            seq_info.push_back({e, a});
        }
    }
    
    int num_seqs = seqs.size();
    vector<int> basis; 
    vector<vector<long long>> row_reduced;
    vector<vector<long long>> relations(num_seqs); // expresses seq_i in basis
    vector<vector<long long>> R_basis_expr; // expresses R_j in basis
    
    for(int i=0; i<num_seqs; i++) {
        vector<long long> cur = seqs[i]; 
        vector<long long> factors(basis.size(), 0);
        
        bool indep = false;
        
        for(int j=0; j<(int)basis.size(); j++) {
            int pivot=-1; for(int c=0; c<L; c++) if(row_reduced[j][c]!=0) {pivot=c; break;}
            if(pivot!=-1 && cur[pivot]!=0) {
                long long factor = (cur[pivot] * modInverse(row_reduced[j][pivot]))%P;
                factors[j] = factor;
                for(int c=pivot; c<L; c++) { cur[c]=(cur[c]-factor*row_reduced[j][c])%P; if(cur[c]<0) cur[c]+=P; }
            }
        }
        for(int c=0; c<L; c++) if(cur[c]!=0) {indep=true; break;}
        
        if(indep) { 
            basis.push_back(i); 
            row_reduced.push_back(cur); 
            
            // seq_i is exactly 1 * basis[-1]
            vector<long long> sr(basis.size(), 0); sr.back()=1; 
            relations[i] = sr; 
            
            // pad older relations and R_basis_expr
            for(int r=0; r<i; r++) if(relations[r].size()>0) relations[r].push_back(0);
            for(int j=0; j<(int)R_basis_expr.size(); j++) R_basis_expr[j].push_back(0);
            
            // R_new = seq_i - sum factors[j] R_j
            // so R_new_expr = 1*basis[-1] - sum factors[j] R_basis_expr[j]
            vector<long long> R_expr(basis.size(), 0);
            R_expr.back() = 1;
            for(int j=0; j<(int)basis.size()-1; j++) {
                if(factors[j] != 0) {
                    for(int k=0; k<(int)basis.size(); k++) {
                        R_expr[k] = (R_expr[k] - factors[j] * R_basis_expr[j][k]) % P;
                        if(R_expr[k] < 0) R_expr[k] += P;
                    }
                }
            }
            R_basis_expr.push_back(R_expr);
        } else { 
            // seq = sum factors[j] R_j
            // express seq in terms of basis:
            vector<long long> expr(basis.size(), 0);
            for(int j=0; j<(int)basis.size(); j++) {
                if(factors[j] != 0) {
                    for(int k=0; k<(int)basis.size(); k++) {
                        expr[k] = (expr[k] + factors[j] * R_basis_expr[j][k]) % P;
                    }
                }
            }
            relations[i] = expr; 
        }
    }
    
    int d = basis.size();
    vector<vector<long long>> M0(d, vector<long long>(d, 0));
    vector<vector<long long>> M1(d, vector<long long>(d, 0));
    for(int i=0; i<d; i++) {
        int idx = basis[i];
        int e = seq_info[idx].first; int a = seq_info[idx].second;
        if(e==-1) { M0[i][0]=1; M1[i][0]=1; continue; }
        int idx0=-1, idx1=-1;
        for(int j=0; j<num_seqs; j++) {
            if(seq_info[j].first==e+1 && seq_info[j].second==a) idx0=j;
            if(seq_info[j].first==e+1 && seq_info[j].second==a+(1<<e)) idx1=j;
        }
        M0[i] = relations[idx0]; M1[i] = relations[idx1];
    }
    
    cout << "M0 = [\n"; for(int i=0; i<d; ++i) { cout << "["; for(int j=0; j<d; ++j) cout << M0[i][j] << ","; cout << "],\n"; } cout << "]\n";
    cout << "M1 = [\n"; for(int i=0; i<d; ++i) { cout << "["; for(int j=0; j<d; ++j) cout << M1[i][j] << ","; cout << "],\n"; } cout << "]\n";
    cout << "F0 = ["; for(int i=0; i<d; ++i) { int idx=basis[i]; if(seq_info[idx].first==-1) cout<<1<<","; else cout<<(V[seq_info[idx].second]%P+P)%P<<","; } cout << "]\n";
    return 0;
}
