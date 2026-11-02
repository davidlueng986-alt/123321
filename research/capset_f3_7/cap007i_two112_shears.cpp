// CAP-007I: deterministic CPU-only exact F3 additive-hole audit for 112+112+Z.
// No global theorem: selected elementary shear combinations only, not all GL(6,3).
#include <array>
#include <vector>
#include <string>
#include <unordered_set>
#include <map>
#include <random>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <cassert>
using namespace std;
using V=array<uint8_t,6>;
using M=array<array<uint8_t,6>,6>;
int enc(const V& v){int a=0;for(auto c:v)a=3*a+c;return a;}
V dec(int a){V v{};for(int i=5;i>=0;i--){v[i]=a%3;a/=3;}return v;}
M eye(){M r{};for(int i=0;i<6;i++)r[i][i]=1;return r;}
M mul(const M&A,const M&B){M C{};for(int i=0;i<6;i++)for(int j=0;j<6;j++)
    for(int k=0;k<6;k++)C[i][j]=(C[i][j]+A[i][k]*B[k][j])%3;return C;}
V act(const M&A,const V&p){V q{};for(int i=0;i<6;i++)for(int j=0;j<6;j++)
    q[i]=(q[i]+A[i][j]*p[j])%3;return q;}
string sig(const M&m){string s;for(auto&r:m)for(auto x:r)s.push_back('0'+x);return s;}

int main(int argc,char**argv){
 if(argc!=2)return 2;
 vector<V>X,Y;
 ifstream in(argv[1]);string line;getline(in,line);assert(line=="n: 7");
 while(getline(in,line))if(line.size()==7){
  V p{};for(int i=0;i<6;i++)p[i]=line[i+1]-'0';
  if(line[0]=='0')X.push_back(p);
  if(line[0]=='1')Y.push_back(p);
 }
 assert(X.size()==112 && Y.size()==112);
 static int T[729][729];
 for(int a=0;a<729;a++)for(int b=0;b<729;b++){
  auto x=dec(a),y=dec(b);V z{};
  for(int i=0;i<6;i++)z[i]=(6-x[i]-y[i])%3;
  T[a][b]=enc(z);
 }
 vector<int>xi;for(auto&p:X)xi.push_back(enc(p));
 vector<M>E;
 for(int i=0;i<6;i++)for(int j=0;j<6;j++)if(i!=j)for(int k=1;k<=2;k++){
  M z=eye();z[i][j]=k;E.push_back(z);
 }
 assert(E.size()==60);
 unordered_set<string>seen;map<int,int>hist;
 int best=-1;string bestmat;vector<int>holesbest;int record13=0;
 auto score=[&](const M&m){
  string key=sig(m);
  if(!seen.insert(key).second)return;
  vector<int>yi;yi.reserve(Y.size());
  for(auto&p:Y)yi.push_back(enc(act(m,p)));
  array<uint8_t,729>forbidden{};
  for(int x:xi)for(int y:yi)forbidden[T[x][y]]=1;
  vector<int>holes;
  for(int i=0;i<729;i++)if(!forbidden[i])holes.push_back(i);
  int h=holes.size();hist[h]++;
  if(h>best){best=h;bestmat=key;holesbest=holes;}
  if(h>=13){record13++;cerr<<"POTENTIAL_13_OR_MORE_HOLES count="<<h<<" mat="<<key<<"\n";}
 };
 score(eye());for(auto&a:E)score(a);
 for(auto&a:E)for(auto&b:E)score(mul(a,b));
 mt19937 rng(20261102);
 for(int z=0;z<4000;z++){
  M m=eye();int k=(z%2?3:4);
  for(int r=0;r<k;r++)m=mul(E[rng()%E.size()],m);
  score(m);
 }
 cout<<"{\"tested_unique_linear_maps\":"<<seen.size()
     <<",\"max_holes\":"<<best
     <<",\"maps_with_at_least_13_holes\":"<<record13
     <<",\"best_transform_matrix_digits\":\""<<bestmat
     <<"\",\"holes_histogram\":{";
 int c=0;
 for(auto [h,n]:hist){if(c++)cout<<",";cout<<"\""<<h<<"\":"<<n;}
 cout<<"},\"best_holes\":[";
 for(size_t i=0;i<holesbest.size();i++){if(i)cout<<",";cout<<holesbest[i];}
 cout<<"]}"<<endl;
}
