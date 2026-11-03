#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <set>
#include <string>
#include <vector>
#include <cassert>
static constexpr int N=2187,K=237;
uint16_t third[N][N];
int pw3[7]={729,243,81,27,9,3,1};
int id(std::array<int,7> a){int x=0;for(int i=0;i<7;i++)x+=pw3[i]*a[i];return x;}
std::array<int,7> dec(int x){std::array<int,7>a{};for(int i=6;i>=0;i--){a[i]=x%3;x/=3;}return a;}
struct State {
 std::array<uint8_t,N> in{};
 std::array<int,N> g{};
 std::array<int,K> s{};
 int score=0;
 void init(const std::vector<int>&base,int extra) {
  in.fill(0);g.fill(0);for(int i=0;i<K-1;i++){s[i]=base[i];in[s[i]]=1;}
  s[K-1]=extra;in[extra]=1;
  for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)g[third[s[i]][s[j]]]++;
  score=0;for(int i=0;i<K;i++)score+=g[s[i]];
  assert(score%3==0);score/=3;
 }
 void move(int slot,int v,int delta){
  int u=s[slot]; assert(in[u]&&!in[v]);
  for(int w:s){if(w==u)continue;g[third[u][w]]--;g[third[v][w]]++;}
  in[u]=0;in[v]=1;s[slot]=v;score+=delta;
 }
 int delta(int slot,int v)const{
  int u=s[slot],w=third[u][v];
  return -g[u]+g[v]-(in[w] && w!=u);
 }
 int direct_score()const{
  int c=0;
  for(int i=0;i<K;i++)for(int j=i+1;j<K;j++){
   int t=third[s[i]][s[j]]; if(in[t])c++;
  }
  assert(c%3==0);return c/3;
 }
};
int main(int argc,char**argv){
 int iters=5000000;uint64_t seed=2026110307;
 if(argc>1)iters=std::atoi(argv[1]);if(argc>2)seed=strtoull(argv[2],nullptr,10);
 for(int i=0;i<N;i++){auto a=dec(i);for(int j=0;j<N;j++){auto b=dec(j);// Use fresh coordinate vector for each pair.
  auto ai=dec(i);std::array<int,7> c{};for(int x=0;x<7;x++)c[x]=(6-ai[x]-b[x])%3;third[i][j]=id(c);
 }}
 const char *witness_path=getenv("CAPSET_WITNESS");
 if(witness_path==nullptr){
  std::ifstream repo("research/capset_f3_7/candidates/calderbank_fishburn_236.txt");
  witness_path=repo.good()?"research/capset_f3_7/candidates/calderbank_fishburn_236.txt":"witness236.txt";
 }
 std::ifstream f(witness_path);assert(f.good());
 std::string line;std::vector<int> B;while(std::getline(f,line)){if(line.size()!=7||line.find_first_not_of("012")!=std::string::npos)continue;std::array<int,7>a{};for(int i=0;i<7;i++)a[i]=line[i]-'0';B.push_back(id(a));}
 assert(B.size()==236);std::array<uint8_t,N>inB{};for(int i:B){assert(!inB[i]);inB[i]=1;}
 std::array<int,N>gb{};for(int i=0;i<236;i++)for(int j=i+1;j<236;j++)gb[third[B[i]][B[j]]]++;
 for(int i:B)assert(gb[i]==0);
 int outsider=0,bestg=INT32_MAX;for(int i=0;i<N;i++)if(!inB[i]&&gb[i]<bestg){outsider=i;bestg=gb[i];}
 assert(bestg==10);
 std::mt19937_64 rng(seed);std::uniform_real_distribution<double> uni(0,1);
 State z;z.init(B,outsider);int best=z.score,bestOverlap=236;std::array<int,K> bestset=z.s;
 auto tic=std::chrono::steady_clock::now();int accepted=0;int rst=0;const int epoch=200000;
 for(int step=0;step<iters;step++){
  if(step%epoch==0){
   if(step){rst++;int extra=outsider;
    if(rst%3==0){
     extra=rng()%N;while(inB[extra])extra=rng()%N;
    }
    z.init(B,extra);
   }
  }
  double phase=(double)(step%epoch)/epoch;
  double temp=std::exp(std::log(10.0)*(1-phase)+std::log(0.45)*phase);
  int si=rng()%K;
  if(rng()%5){
   for(int k=0;k<7;k++){int s=rng()%K;if(z.g[z.s[s]]>z.g[z.s[si]])si=s;}
  }
  int v=-1;
  if(rng()%5){
   int gain=INT32_MAX;
   for(int k=0;k<20;k++){
    int t=rng()%N;
    if(z.in[t])continue;
    if(z.g[t]<gain){gain=z.g[t];v=t;}
   }
  }
  if(v<0){v=rng()%N;while(z.in[v])v=rng()%N;}
  int delta=z.delta(si,v);
  if(delta<=0 || uni(rng)<std::exp(-delta/temp)){
   z.move(si,v,delta);accepted++;
   if(z.score<best){
     best=z.score;bestset=z.s;
     int overlap=0;for(int p:z.s)overlap+=inB[p];bestOverlap=overlap;
     std::cout<<"NEW_BEST step="<<step<<" conflicts="<<best<<" overlap_with236="<<overlap<<"\n"<<std::flush;
     assert(z.direct_score()==z.score);
     if(best==0){
      std::set<int>check(bestset.begin(),bestset.end());assert(check.size()==K);
      for(int a:bestset)for(int b:bestset)if(a!=b)assert(!check.count(third[a][b]));
      std::ofstream w("NEW_CAP_237.txt");w<<"n: 7\n";
      for(int p:bestset){auto a=dec(p);for(int x:a)w<<x;w<<"\n";}
      std::cout<<"CLOSED_LOWER_237_INDEPENDENT_CHECK_PASS\n";return 0;
     }
   }
  }
  if(step%100000==99999){assert(z.direct_score()==z.score);}
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-tic).count();
 std::ofstream w("BEST_237_NEAR_CAP.txt");
 w<<"# conflicts="<<best<<" overlap="<<bestOverlap<<" seed="<<seed<<" iterations="<<iters<<"\n";
 for(int p:bestset){auto a=dec(p);for(int x:a)w<<x;w<<"\n";}
 std::cout<<"DONE seed="<<seed<<" iterations="<<iters<<" best_conflicts="<<best<<" best_overlap="<<bestOverlap<<" accepted="<<accepted<<" secs="<<sec<<" (NOT A CAP; root OPEN)\n";
}
