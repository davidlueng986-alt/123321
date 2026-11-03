#include <bits/stdc++.h>
using namespace std;
using Clock=chrono::steady_clock;
struct Candidate {int r,c,a,b,d;};
struct DLX {
 int n,roots,head,tot, selected=0,maxdepth=0;
 vector<int> L,R,U,D,C,S,ROW; vector<Candidate> cand; vector<array<int,6>> cs;
 vector<int> chosen,solution; long long nodes=0, prune=0, branches=0; bool timedout=false; Clock::time_point started; double limit=5.0; long long node_budget=1000000;
 DLX(int n_):n(n_),roots(6*n*n),head(0),tot(roots+1){
  L.resize(roots+1);R.resize(roots+1);U.resize(roots+1);D.resize(roots+1);C.resize(roots+1);S.resize(roots+1);ROW.resize(roots+1);
  for(int i=0;i<=roots;i++){L[i]=i-1;R[i]=i+1;U[i]=D[i]=i;C[i]=i;}
  L[0]=roots;R[roots]=0;
 }
 void add(int r,int c,int a,int b,int d){
   int id=cand.size();cand.push_back({r,c,a,b,0});
   array<int,6> cols={r*n+c,n*n+r*n+a,2*n*n+c*n+a,3*n*n+r*n+b,4*n*n+c*n+b,5*n*n+a*n+b};
   int first=tot;
   for(int k=0;k<6;k++){
    int col=cols[k]+1;int u=U[col];
    U.push_back(u);D.push_back(col);L.push_back(tot-1);R.push_back(tot+1);C.push_back(col);S.push_back(0);ROW.push_back(id);
    U[col]=tot;D[u]=tot;S[col]++;tot++;
   }
   L[first]=tot-1;R[tot-1]=first;
   cs.push_back(cols);
 }

 void cover(int c){R[L[c]]=R[c];L[R[c]]=L[c];for(int i=D[c];i!=c;i=D[i])for(int j=R[i];j!=i;j=R[j]){U[D[j]]=U[j];D[U[j]]=D[j];S[C[j]]--;}}
 void uncover(int c){for(int i=U[c];i!=c;i=U[i])for(int j=L[i];j!=i;j=L[j]){S[C[j]]++;U[D[j]]=j;D[U[j]]=j;}R[L[c]]=c;L[R[c]]=c;}
 bool go(int d){
  nodes++;if(d>maxdepth)maxdepth=d;
  if(nodes>=node_budget || ((nodes&16383)==0 && chrono::duration<double>(Clock::now()-started).count()>limit)) {timedout=true;return false;}
  if(R[head]==head){solution=chosen;return true;}
  int c=-1,best=INT_MAX;
  for(int i=R[head];i!=head;i=R[i]){if(S[i]<best){best=S[i];c=i;if(best<=1)break;}}
  if(best==0){prune++;return false;}
  cover(c);
  for(int r=D[c];r!=c;r=D[r]){
   chosen.push_back(ROW[r]); branches++;
   for(int j=R[r];j!=r;j=R[j])cover(C[j]);
   if(go(d+1))return true;
   for(int j=L[r];j!=r;j=L[j])uncover(C[j]);
   chosen.pop_back();
   if(timedout)break;
  }
  uncover(c);
  return false;
 }
 string solve(double secs,long long nbudget){limit=secs;node_budget=nbudget;started=Clock::now();bool sat=go(0);double elapsed=chrono::duration<double>(Clock::now()-started).count();
  string status=sat?"SAT":timedout?"UNKNOWN_BUDGET":"UNSAT_EXHAUSTIVE";
  cerr << "E061 order "<<n<<" candidates "<<cand.size()<<" nodes "<<nodes<<" branches "<<branches<<" prune "<<prune<<" maxdepth "<<maxdepth<<" sec "<<elapsed<<" status "<<status<<"\n";
  cout << "{\"n\":"<<n<<",\"status\":\""<<status<<"\",\"candidates\":"<<cand.size()<<",\"nodes\":"<<nodes<<",\"branches\":"<<branches<<",\"dead_ends\":"<<prune<<",\"maxdepth\":"<<maxdepth<<",\"seconds\":"<<setprecision(5)<<elapsed;
  if(sat){vector<vector<vector<int>>> mats(2,vector<vector<int>>(n,vector<int>(n,-1)));for(int id:solution){auto v=cand[id];mats[0][v.r][v.c]=v.a;mats[1][v.r][v.c]=v.b;}for(auto&m:mats)for(auto&row:m)for(int v:row)if(v<0)abort();cout<<",\"witness\":[";for(int s=0;s<2;s++){if(s)cout<<",";cout<<"[";for(int r=0;r<n;r++){if(r)cout<<",";cout<<"[";for(int c=0;c<n;c++){if(c)cout<<",";cout<<mats[s][r][c];}cout<<"]";}cout<<"]";}cout<<"]";}
  cout<<"}\n";
  return status;
 }
};
int main(int argc,char**argv){int n=argc>1?atoi(argv[1]):10;double sec=argc>2?atof(argv[2]):5;long long budget=argc>3?atoll(argv[3]):10000000;
 vector<int> f(n,-1);string cyc=argc>4?argv[4]:"";if(cyc.size()){
  vector<int> dims;istringstream ss(cyc);string tok;int next=0;
  while(getline(ss,tok,',')){int k=stoi(tok);if(k<2||next+k>n)abort();
   for(int j=0;j<k;j++)f[next+j]=next+(j+1)%k;next+=k;dims.push_back(k);}
  if(next!=n||f[0]!=1)abort();
 }
 DLX solver(n);
 unsigned seed=argc>5?unsigned(atoi(argv[5])):0;
 vector<Candidate> opts;for(int r=0;r<n;r++)for(int c=0;c<n;c++){
 if(r==0){opts.push_back({r,c,c,c,0});continue;}
 for(int a=0;a<n;a++){if(a==c||(c==0&&a!=r)||(r==1&&cyc.size()&&a!=f[c]))continue;
 for(int b=0;b<n;b++){if(b==c||b==a)continue;opts.push_back({r,c,a,b,0});}}
 }
 if(seed){mt19937 rng(seed);shuffle(opts.begin(),opts.end(),rng);}
 for(auto &v:opts)solver.add(v.r,v.c,v.a,v.b,0);
 solver.solve(sec,budget);
}