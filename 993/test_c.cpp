#include <iostream>
#include <vector>
#include <fstream>
#include <cassert>
#include <string>

using namespace std;

long long P = 1000000007;

long long power(long long base, long long exp) {
    long long res = 1; base %= P; if(base<0) base += P;
    while(exp>0) { if(exp%2) res=(res*base)%P; base=(base*base)%P; exp/=2; }
    return res;
}
long long modInverse(long long n) { n%=P; if(n<0) n+=P; return power(n, P-2); }

int main() {
    ifstream fin("bb_values.txt");
    vector<long long> V; long long x, y;
    while(fin >> x >> y) V.push_back(y);
    int L = 400; int max_e = 7;
    vector<vector<long long>> seqs;
    vector<long long> ones(L, 1); seqs.push_back(ones);
    for(int e=0; e<=max_e; e++) {
        for(int a=0; a<(1<<e); a++) {
            vector<long long> sub(L);
            for(int n=0; n<L; n++) sub[n] = (V[(1<<e)*n+a]%P+P)%P;
            seqs.push_back(sub);
        }
    }
    vector<int> basis; vector<vector<long long>> row_reduced;
    vector<vector<long long>> relations(seqs.size());
    for(int i=0; i<seqs.size(); i++) {
        vector<long long> cur = seqs[i]; vector<long long> coeffs(basis.size(), 0);
        bool indep = false;
        for(int j=0; j<(int)basis.size(); j++) {
            int pivot=-1; for(int c=0; c<L; c++) if(row_reduced[j][c]!=0) {pivot=c; break;}
            if(pivot!=-1 && cur[pivot]!=0) {
                long long factor = (cur[pivot] * modInverse(row_reduced[j][pivot]))%P;
                coeffs[j] = factor;
                for(int c=pivot; c<L; c++) { cur[c]=(cur[c]-factor*row_reduced[j][c])%P; if(cur[c]<0) cur[c]+=P; }
            }
        }
        for(int c=0; c<L; c++) if(cur[c]!=0) {indep=true; break;}
        if(indep) { basis.push_back(i); row_reduced.push_back(cur); vector<long long> sr(basis.size(),0); sr.back()=1; relations[i]=sr; for(int r=0; r<i; r++) if(relations[r].size()>0) relations[r].push_back(0); }
        else { relations[i] = coeffs; }
    }
    int idx0 = -1;
    for(int i=0; i<seqs.size(); i++) if(i == 1+127+1) { idx0=i; break; } // e=7, a=0 is index 129
    cout << "relations size: " << relations[129].size() << endl;
    long long sum = 0;
    for(int j=0; j<basis.size(); j++) {
        long long f0 = (basis[j]==0) ? 1 : seqs[basis[j]][0];
        sum = (sum + relations[129][j] * f0) % P;
    }
    cout << "In C++, relation * F0 = " << sum << ", target seq[0] = " << seqs[129][0] << endl;
    return 0;
}
