// CAP-005E: independent C++17 exact pair-removal certificate for the known 236 cap.
// No randomization, solver, or floating-point arithmetic. CPU only.
#include <bits/stdc++.h>
using namespace std;
using Point=array<uint8_t,7>;
int key(const Point&p){int x=0;for(int i=0;i<7;i++)x=3*x+p[i];return x;}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: paircheck cap236.txt\n";return 2;}
 ifstream in(argv[1]);vector<Point> P;string s;
 while(in>>s){if(s=="n:"){in>>s;continue;}if(s.size()!=7)continue;Point p{};for(int i=0;i<7;i++)p[i]=s[i]-'0';P.push_back(p);}
 if(P.size()!=236){cerr<<"wrong fixture size "<<P.size()<<"\n";return 3;}
 array<int,2187> orig;orig.fill(-1);
 for(int i=0;i<236;i++){int k=key(P[i]);if(orig[k]!=-1)return 4;orig[k]=i;}
 vector<Point> X;vector<vector<pair<int,int>>> sec;
 array<int,2187> ext;ext.fill(-1);
 for(int k=0;k<2187;k++)if(orig[k]<0){int t=k;Point p{};for(int j=6;j>=0;j--){p[j]=t%3;t/=3;}ext[k]=X.size();X.push_back(p);sec.emplace_back();}
 for(int i=0;i<236;i++)for(int j=i+1;j<236;j++){
  Point x{};for(int z=0;z<7;z++)x[z]=(6-P[i][z]-P[j][z])%3;
  int k=key(x);if(orig[k]>=0){cerr<<"not a cap\n";return 5;}sec[ext[k]].emplace_back(i,j);
 }
 if(X.size()!=1951)return 6;
 long long pairs=0,at16=0;int best=237;int exampleA=-1,exampleB=-1;
 int parent[236],sz[236];bool active[236];
 auto root=[&](int x){while(parent[x]!=x){parent[x]=parent[parent[x]];x=parent[x];}return x;};
 for(int a=0;a<(int)X.size();a++)for(int b=a+1;b<(int)X.size();b++){
  int z=0;for(int j=0;j<7;j++)z=3*z+(6-X[a][j]-X[b][j])%3;
  int forced=orig[z];
  for(int i=0;i<236;i++){parent[i]=i;sz[i]=1;active[i]=false;}
  for(int t=0;t<2;t++){
   for(auto [u,v]:sec[t?b:a]){
    if(u==forced||v==forced)continue;
    active[u]=active[v]=true;
    int ru=root(u),rv=root(v);
    if(ru!=rv){if(sz[ru]<sz[rv])swap(ru,rv);parent[rv]=ru;sz[ru]+=sz[rv];}
   }
  }
  int del=forced>=0;
  for(int i=0;i<236;i++)if(active[i]&&parent[i]==i)del+=sz[i]/2;
  if(del<best){best=del;exampleA=a;exampleB=b;}
  if(del==16)at16++;
  pairs++;
 }
 cout<<"{\"outsiders\":"<<X.size()<<",\"pairs\":"<<pairs<<",\"minimum_deletions\":"<<best<<",\"pairs_with_exactly_16_deletions\":"<<at16<<",\"example_outsider_indices\":["<<exampleA<<","<<exampleB<<"]}"<<endl;
 return !(pairs==1902225 && best==16 && at16==888);
}
