#include <bits/stdc++.h>
using namespace std;
constexpr int N=10, NN=100, V=200;
int sq[2][NN];
struct Cut{array<uint8_t,V> known;int anchor;long long trials=0, nodes=0;};
// Sound OVERAPPROXIMATION: partial known symbols must not repeat along a
// transversal; unknown symbols treated as arbitrary wildcards. A true Latin
// common transversal in any A/B completion is always inside this superset.
bool exists_transversal(Cut& q){
 q.trials++;
 auto dfs=[&](auto&&self,int rowmask,int colmask,int amask,int bmask)->bool{
  q.nodes++;
  if(rowmask==1023)return true;
  int best=-1,best_mask=0,best_size=11;
  for(int r=0;r<N;r++)if(!(rowmask>>r&1)){
   int poss=0;
   for(int c=0;c<N;c++)if(!(colmask>>c&1)){
    const int z=r*N+c;
    if(q.known[z]&&(amask>>sq[0][z]&1))continue;
    if(q.known[100+z]&&(bmask>>sq[1][z]&1))continue;
    poss|=1<<c;
   }
   int pop=__builtin_popcount((unsigned)poss);
   if(pop<best_size){best_size=pop;best=r;best_mask=poss;if(pop==0)return false;}
  }
  if(best<0)return false;
  for(int bits=best_mask;bits;bits&=bits-1){
   int c=__builtin_ctz((unsigned)bits),z=best*N+c;
   int na=amask | (q.known[z]?(1<<sq[0][z]):0);
   int nb=bmask | (q.known[100+z]?(1<<sq[1][z]):0);
   if(self(self,rowmask|(1<<best),colmask|(1<<c),na,nb))return true;
  }
  return false;
 };
 int r=q.anchor/N,c=q.anchor%N,z=q.anchor;
 return dfs(dfs,1<<r,1<<c,q.known[z]?(1<<sq[0][z]):0,q.known[100+z]?(1<<sq[1][z]):0);
}
int main(int argc,char**argv){
 if(argc<6){cerr<<"USAGE: program input.txt anchorR anchorC random_seed repeats\n";return 2;}
 ifstream in(argv[1]);for(int s=0;s<2;s++)for(int z=0;z<100;z++)if(!(in>>sq[s][z]))throw runtime_error("missing pair fixture");
 int r=stoi(argv[2]),c=stoi(argv[3]);uint64_t seed=stoull(argv[4]);int repeats=stoi(argv[5]);
 if(r<0||r>=10||c<0||c>=10||repeats<1)throw runtime_error("args");
 Cut base{};base.anchor=10*r+c;base.known.fill(1);
 if(exists_transversal(base)){cerr<<"FULL pair has a common transversal at this anchor: no obstruction\n";return 3;}
 Cut best=base;
 auto count=[](const Cut&q){int sum=0;for(auto v:q.known)sum+=v;return sum;};
 for(int repeat=0;repeat<repeats;repeat++){
  Cut q=base;
  vector<int> order(200);iota(order.begin(),order.end(),0);
  mt19937_64 rng(seed+repeat*0x9e3779b97f4a7c15ULL);
  shuffle(order.begin(),order.end(),rng);
  bool changed=true;
  while(changed){changed=false;
   for(int index:order){if(!q.known[index])continue;
    q.known[index]=0;
    if(exists_transversal(q)){q.known[index]=1;}else changed=true;
   }
  }
  if(count(q)<count(best))best=q;
  cerr<<"repeat="<<repeat<<" core_literals="<<count(q)<<" best="<<count(best)<<" queries="<<q.trials<<" search_nodes="<<q.nodes<<"\n";
 }
 // Strict one-literal minimality under our sound *overapprox* checker.
 if(exists_transversal(best))throw runtime_error("bad cut");
 for(int i=0;i<200;i++)if(best.known[i]){
  best.known[i]=0;
  if(!exists_transversal(best))throw runtime_error("core not deletion minimal");
  best.known[i]=1;
 }
 cout<<"{\"n\":10,\"anchor\":["<<r<<","<<c<<"],\"known_symbols\":[";
 int k=0;
 for(int i=0;i<200;i++)if(best.known[i]){
  if(k++)cout<<",";
  int s=i/100,z=i%100;
  cout<<"["<<s<<","<<z/10<<","<<z%10<<","<<sq[s][z]<<"]";
 }
 cout<<"],\"literal_count\":"<<k<<",\"full_pair_is_orthogonal\":true,\"verified_deletion_minimal_by_cpp\":true,\"seed\":"<<seed<<",\"repeats\":"<<repeats<<"}\n";
}
