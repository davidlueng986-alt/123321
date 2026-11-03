// CAP-032B: independent C++17 exact high-density AG(4,3) profile census.
// Enumerates all k=6..9 F3^3 caps, AGL3 orbits, and compatible third caps.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <unordered_set>
#include <vector>
using Mask=uint32_t;
constexpr Mask FULL=(1u<<27)-1;
int third[27][27];
std::vector<std::array<int,27>> generators;
int digit(int a,int i){while(i--)a/=3;return a%3;}
int enc(const std::array<int,3>&p){return p[0]+3*p[1]+9*p[2];}
void add_gen(const std::function<std::array<int,3>(std::array<int,3>)>&f){
 std::array<int,27> m{};
 for(int p=0;p<27;++p)m[p]=enc(f({digit(p,0),digit(p,1),digit(p,2)}));
 generators.push_back(m);
}
void setup(){
 for(int a=0;a<27;++a)for(int b=0;b<27;++b)
 third[a][b]=enc({(6-digit(a,0)-digit(b,0))%3,(6-digit(a,1)-digit(b,1))%3,(6-digit(a,2)-digit(b,2))%3});
 for(int i=0;i<3;++i)add_gen([i](auto a){a[i]=(a[i]+1)%3;return a;});
 add_gen([](auto a){std::swap(a[0],a[1]);return a;});
 add_gen([](auto a){std::swap(a[1],a[2]);return a;});
 add_gen([](auto a){a[0]=2*a[0]%3;return a;});
 for(int i=0;i<3;++i)for(int j=0;j<3;++j)if(i!=j)
 add_gen([i,j](auto a){a[i]=(a[i]+a[j])%3;return a;});
 assert(generators.size()==12);
}
bool cap(Mask s){
 for(int a=0;a<27;++a)if(s&(1u<<a))
 for(int b=a+1;b<27;++b)if((s&(1u<<b))&&(s&(1u<<third[a][b])))return false;
 return true;
}
std::vector<Mask> caps_of_size(int k){
 std::vector<Mask> out;Mask s=(1u<<k)-1;
 while(s<(1u<<27)){
  if(cap(s))out.push_back(s);
  Mask u=s&-s,v=s+u;
  s=v+(((v^s)/u)>>2);
 }
 return out;
}
Mask apply(Mask s,const std::array<int,27>&g){
 Mask out=0;
 while(s){int p=__builtin_ctz(s);s&=s-1;out|=1u<<g[p];}
 return out;
}
std::vector<Mask> representatives(const std::vector<Mask>&all,std::vector<int>&sizes){
 std::unordered_set<Mask> canonical(all.begin(),all.end()),seen;
 std::vector<Mask> reps;
 for(Mask start:all)if(!seen.count(start)){
  std::vector<Mask> q{start};seen.insert(start);
  for(size_t i=0;i<q.size();++i)for(const auto &g:generators){
   Mask m=apply(q[i],g);
   assert(canonical.count(m));
   if(seen.insert(m).second)q.push_back(m);
  }
  reps.push_back(start);sizes.push_back(static_cast<int>(q.size()));
 }
 assert(seen.size()==all.size());
 return reps;
}
int largest_cap_in(Mask subset,int bound){
 std::vector<int>p;
 for(Mask s=subset;s;s&=s-1)p.push_back(__builtin_ctz(s));
 int h=static_cast<int>(p.size());
 for(int k=h;k>bound;--k){
  int limit=1<<h;
  for(int mask=1;mask<limit;++mask){
   if(__builtin_popcount((unsigned)mask)!=k)continue;
   Mask s=0;
   for(int j=0;j<h;++j)if(mask&(1<<j))s|=1u<<p[j];
   if(cap(s))return k;
  }
 }
 return bound;
}
int main(){
 setup();
 std::map<int,std::vector<Mask>> all,reps;
 const std::map<int,int> counts{{6,107406},{7,126360},{8,63180},{9,2106}};
 const std::map<int,std::vector<int>> orbits{{6,{6318,25272,75816}},{7,{50544,75816}},{8,{6318,18954,37908}},{9,{2106}}};
 for(int k=6;k<=9;++k){
  all[k]=caps_of_size(k);assert(static_cast<int>(all[k].size())==counts.at(k));
  std::vector<int> sizes;reps[k]=representatives(all[k],sizes);
  std::sort(sizes.begin(),sizes.end());assert(sizes==orbits.at(k));
 }
 const std::map<std::pair<int,int>,int> expected{{{6,6},8},{{6,7},6},{{6,8},6},{{6,9},3},{{7,7},4},{{7,8},3},{{7,9},2},{{8,8},2},{{8,9},2},{{9,9},2}};
 std::cout<<"a,b,max_third,max_holes,pairs\n";
 for(int a=6;a<=9;++a)for(int b=a;b<=9;++b){
  int maxcap=0,maxholes=0;uint64_t pairs=0;
  for(Mask A:reps[a])for(Mask B:all[b]){
   Mask blocked=0;
   for(Mask p=A;p;p&=p-1){int i=__builtin_ctz(p);
    for(Mask q=B;q;q&=q-1){int j=__builtin_ctz(q);blocked|=1u<<third[i][j];}
   }
   Mask free=FULL^blocked;
   int holes=__builtin_popcount(free);
   maxholes=std::max(maxholes,holes);
   if(holes>maxcap)maxcap=std::max(maxcap,largest_cap_in(free,maxcap));
   ++pairs;
  }
  assert(maxcap==expected.at({a,b}));
  std::cout<<a<<","<<b<<","<<maxcap<<","<<maxholes<<","<<pairs<<"\n";
 }
}
