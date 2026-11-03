#include <bits/stdc++.h>
using namespace std;
#include "E061_base.h"
const int n=10,ROOTS=470;
int C7[n][n]={{0,-1,-1,-1,1,2,3,4,5,6},{6,4,2,-1,-1,5,1,3,-1,0},{4,-1,5,3,2,-1,6,0,1,-1},{5,1,-1,6,4,3,-1,-1,0,2},{3,2,-1,0,-1,1,5,6,-1,4},{1,0,3,-1,6,-1,2,5,4,-1},{2,-1,0,1,3,4,-1,-1,6,5},{-1,5,4,2,-1,6,0,1,3,-1},{-1,3,6,5,0,-1,4,-1,2,1},{-1,6,1,4,5,0,-1,2,-1,3}};
struct DLX {
 vector<int>L,R,U,D,C,S,ID; vector<array<int,3>> options;vector<int>sel;int tot=ROOTS+1;
 long long nodes=0,solutions=0,original=0,distinct=0;bool timeout=false;int maxdepth=0;
 chrono::steady_clock::time_point start;
 DLX(){for(auto*v:{&L,&R,&U,&D,&C,&S,&ID})v->resize(ROOTS+1);for(int i=0;i<=ROOTS;i++){L[i]=i-1;R[i]=i+1;U[i]=D[i]=i;C[i]=i;}L[0]=ROOTS;R[ROOTS]=0;}
 void add(int r,int c,int b){int id=options.size();options.push_back({r,c,b});vector<int>cols={r*10+c,100+r*10+b,200+c*10+b,300+Q[0][r][c]*10+b};if(C7[r][c]>=0)cols.push_back(400+C7[r][c]*10+b);int first=tot;
  for(int v:cols){int co=v+1,u=U[co];L.push_back(tot-1);R.push_back(tot+1);U.push_back(u);D.push_back(co);C.push_back(co);S.push_back(0);ID.push_back(id);U[co]=tot;D[u]=tot;S[co]++;tot++;}
  L[first]=tot-1;R[tot-1]=first;
 }
 void cover(int c){R[L[c]]=R[c];L[R[c]]=L[c];for(int i=D[c];i!=c;i=D[i])for(int j=R[i];j!=i;j=R[j]){U[D[j]]=U[j];D[U[j]]=D[j];S[C[j]]--;}}
 void uncover(int c){for(int i=U[c];i!=c;i=U[i])for(int j=L[i];j!=i;j=L[j]){S[C[j]]++;U[D[j]]=j;D[U[j]]=j;}R[L[c]]=c;L[R[c]]=c;}
 bool go(int depth){nodes++;maxdepth=max(maxdepth,depth);if(nodes%16384==0&&chrono::duration<double>(chrono::steady_clock::now()-start).count()>12){timeout=true;return false;}
 if(R[0]==0){solutions++;bool same=true;for(int id:sel){auto[r,c,b]=options[id];if(Q[1][r][c]!=b)same=false;}if(same)original++;else{distinct++;return true;}return false;}
 int best=-1,bsize=INT_MAX;for(int c=R[0];c!=0;c=R[c]){if(S[c]<bsize){best=c;bsize=S[c];if(bsize<=1)break;}}if(bsize==0)return false;
 cover(best);for(int v=D[best];v!=best;v=D[v]){sel.push_back(ID[v]);for(int j=R[v];j!=v;j=R[j])cover(C[j]);bool ok=go(depth+1);for(int j=L[v];j!=v;j=L[j])uncover(C[j]);sel.pop_back();if(ok||timeout){uncover(best);return ok;}}uncover(best);return false;}
};
int main(){DLX d;for(int r=0;r<10;r++)for(int c=0;c<10;c++)for(int b=0;b<10;b++){if(r==0&&b!=Q[1][0][c])continue;d.add(r,c,b);}int oldok=0;bool seen[470]={};for(int r=0;r<10;r++)for(int c=0;c<10;c++){int b=Q[1][r][c],a=Q[0][r][c];int cols[]={r*10+c,100+r*10+b,200+c*10+b,300+a*10+b};for(int cc:cols){if(seen[cc])abort();seen[cc]=true;oldok++;}if(C7[r][c]>=0){int cc=400+C7[r][c]*10+b;if(seen[cc])abort();seen[cc]=true;oldok++;}}
 for(bool v:seen)if(!v)abort();d.start=chrono::steady_clock::now();bool found=d.go(0);double seconds=chrono::duration<double>(chrono::steady_clock::now()-d.start).count();cout<<"{\"status\":\""<<(found?"SAT_NEW_B":d.timeout?"UNKNOWN_BUDGET":"EXHAUSTIVE_UNIQUE_B")<<"\",\"nodes\":"<<d.nodes<<",\"maxdepth\":"<<d.maxdepth<<",\"solutions\":"<<d.solutions<<",\"original\":"<<d.original<<",\"distinct\":"<<d.distinct<<",\"options\":"<<d.options.size()<<",\"seconds\":"<<seconds<<",\"fixed_scope\":true}"<<endl;
}