#include <bits/stdc++.h>
using namespace std;
using clock_t2=chrono::steady_clock;
struct T {int r,c,a;};
struct DLX {
 int n,columns,head=0; vector<int>L,R,U,D,C,S,X; vector<T>cand;vector<int>chosen,solution;long long nodes=0,budget; bool timedout=false;double secs;clock_t2::time_point start;
 DLX(int n):n(n),columns(4*n*n){int z=columns+1;L.resize(z);R.resize(z);U.resize(z);D.resize(z);C.resize(z);S.resize(z);X.resize(z);for(int i=0;i<z;i++){L[i]=i-1;R[i]=i+1;U[i]=D[i]=i;C[i]=i;}L[0]=columns;R[columns]=0;}
 void add(int r,int c,int a,int fixedc){int id=cand.size();cand.push_back({r,c,a});int cols[4]={r*n+c,n*n+r*n+a,2*n*n+c*n+a,3*n*n+fixedc*n+a};int first=L.size();for(int k=0;k<4;k++){int col=cols[k]+1;int node=L.size();int u=U[col];L.push_back(node-1);R.push_back(node+1);U.push_back(u);D.push_back(col);C.push_back(col);S.push_back(0);X.push_back(id);U[col]=node;D[u]=node;S[col]++;}L[first]=int(L.size())-1;R.back()=first;}
 void cover(int c){R[L[c]]=R[c];L[R[c]]=L[c];for(int x=D[c];x!=c;x=D[x])for(int y=R[x];y!=x;y=R[y]){U[D[y]]=U[y];D[U[y]]=D[y];S[C[y]]--;}}
 void uncover(int c){for(int x=U[c];x!=c;x=U[x])for(int y=L[x];y!=x;y=L[y]){S[C[y]]++;U[D[y]]=y;D[U[y]]=y;}R[L[c]]=c;L[R[c]]=c;}
 bool go(){nodes++;if(nodes>=budget||((nodes&8191)==0&&chrono::duration<double>(clock_t2::now()-start).count()>secs)){timedout=true;return false;}if(R[0]==0){solution=chosen;return true;}
 int best=INT_MAX,c=-1;for(int i=R[0];i;i=R[i])if(S[i]<best){best=S[i];c=i;if(best<=1)break;}if(best==0)return false;
 cover(c);for(int r=D[c];r!=c;r=D[r]){chosen.push_back(X[r]);for(int j=R[r];j!=r;j=R[j])cover(C[j]);if(go())return true;for(int j=L[r];j!=r;j=L[j])uncover(C[j]);chosen.pop_back();if(timedout)break;}uncover(c);return false;
 }
 string run(double sec,long long bn){secs=sec;budget=bn;start=clock_t2::now();bool yes=go();return yes?"SAT":timedout?"UNKNOWN_BUDGET":"UNSAT_EXHAUSTIVE";}
};
int main(int argc,char**argv){if(argc<4){cerr<<"args: c_index seconds budget\n";return 2;}int index=atoi(argv[1]);double secs=atof(argv[2]);long long budget=atoll(argv[3]);vector<vector<int>>Cmat(10,vector<int>(10));ifstream in(argc>4?argv[4]:"C7_all_complete.txt");if(!in)return 3;for(int i=0;i<=index;i++)for(int r=0;r<10;r++)for(int c=0;c<10;c++)if(!(in>>Cmat[r][c]))return 4;auto& Q=Cmat;DLX dx(10);for(int r=0;r<10;r++)for(int c=0;c<10;c++)for(int a=0;a<10;a++){
if(r==0){if(a!=c)continue;}else if(a==c||a==Q[r][c])continue;
dx.add(r,c,a,Q[r][c]);}
string status=dx.run(secs,budget);cout<<"{\"index\":"<<index<<",\"status\":\""<<status<<"\",\"nodes\":"<<dx.nodes<<",\"candidates\":"<<dx.cand.size();if(status=="SAT"){vector<vector<int>>A(10,vector<int>(10,-1));for(int i:dx.solution){auto z=dx.cand[i];A[z.r][z.c]=z.a;}for(auto&row:A)if(set<int>(row.begin(),row.end()).size()!=10)abort();for(int c=0;c<10;c++){set<int>v;for(int r=0;r<10;r++)v.insert(A[r][c]);if(v.size()!=10)abort();}set<pair<int,int>>v;for(int r=0;r<10;r++)for(int c=0;c<10;c++)v.insert({A[r][c],Q[r][c]});if(v.size()!=100)abort();cout<<",\"A\":[";for(int r=0;r<10;r++){if(r)cout<<",";cout<<"[";for(int c=0;c<10;c++){if(c)cout<<",";cout<<A[r][c];}cout<<"]";}cout<<"]";}
cout<<"}\n";
}