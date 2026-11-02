// CAP-005J: independent direct F3 arithmetic and all C(27,7) neighborhoods.
// Necessary gate only, not a 237-point witness or global upper bound.
#include <array>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using P=std::array<int,7>;
int encode(const P& p){int v=0;for(int x:p)v=3*v+x;return v;}
P decode(int v){P p{};for(int i=6;i>=0;--i){p[i]=v%3;v/=3;}return p;}
int fiber(const P& p){return 9*p[0]+3*p[1]+p[2];}
struct Outsider{std::array<uint32_t,6> edges{};int k=0;};
int main(int argc,char**argv){
 if(argc!=2){std::cerr<<"Usage: checker baseline.txt\n";return 2;}
 std::ifstream in(argv[1]);if(!in){std::cerr<<"cannot read baseline\n";return 2;}
 std::string s;std::vector<P> pts;std::array<bool,2187> present{};
 while(in>>s){if(s.size()!=7||s.find_first_not_of("012")!=std::string::npos)continue;
  P p{};for(int j=0;j<7;j++)p[j]=s[j]-'0';int id=encode(p);
  if(present[id]){std::cerr<<"duplicate point\n";return 1;}present[id]=true;pts.push_back(p);
 }
 if(pts.size()!=236){std::cerr<<"not 236 points\n";return 1;}
 std::array<std::set<uint32_t>,2187> edgeSets;
 for(size_t i=0;i<pts.size();i++)for(size_t j=i+1;j<pts.size();j++){
  P z{};for(int a=0;a<7;a++)z[a]=(6-pts[i][a]-pts[j][a])%3;
  int id=encode(z);if(present[id]){std::cerr<<"baseline has a line\n";return 1;}
  int a=fiber(pts[i]),b=fiber(pts[j]);
  if(a!=b)edgeSets[id].insert((uint32_t(1)<<a)|(uint32_t(1)<<b));
 }
 std::array<std::vector<Outsider>,27> by{};
 std::map<int,int> kHist;int outside=0;
 for(int id=0;id<2187;id++)if(!present[id]){
  outside++;P x=decode(id);int f=fiber(x);const auto& ee=edgeSets[id];int k=int(ee.size());kHist[k]++;
  uint32_t used=uint32_t(1)<<f;
  for(auto e:ee){if(__builtin_popcount(e)!=2||(used&e)){std::cerr<<"matching violated\n";return 1;}used|=e;}
  if(k<=6){Outsider o;o.k=k;int t=0;for(auto e:ee)o.edges[t++]=e;by[f].push_back(o);}
 }
 if(outside!=1951||kHist!=std::map<int,int>{{1,8},{2,16},{3,64},{4,142},{5,712},{6,297},{7,320},{8,8},{9,384}}){std::cerr<<"outsider histogram mismatch\n";return 1;}
 std::map<int,int> hist;std::vector<uint32_t> maxMasks;
 int maximum=-1;uint64_t total=0;int n=0,excluded=0;
 for(uint32_t mask=(1u<<7)-1;mask<(1u<<27);){
  int cnt=0;uint32_t rem=mask;
  while(rem){int f=__builtin_ctz(rem);rem&=rem-1;
   for(const auto& o:by[f]){bool ok=true;
    for(int j=0;j<o.k;j++)if(!(mask&o.edges[j])){ok=false;break;}
    if(ok)cnt++;
   }
  }
  hist[cnt]++;total+=cnt;n++;if(cnt<=16)excluded++;
  if(cnt>maximum){maximum=cnt;maxMasks={mask};}
  else if(cnt==maximum)maxMasks.push_back(mask);
  uint32_t c=mask&-mask,r=mask+c;
  if(r==0)break;
  mask=(((r^mask)>>2)/c)|r;
 }
 if(n!=888030||excluded!=862906||maximum!=198||maxMasks.size()!=8||total!=2946160){
  std::cerr<<"census regression failed: "<<n<<" "<<excluded<<" "<<maximum<<" "<<maxMasks.size()<<" "<<total<<"\n";return 1;}
 std::cout<<"{\"total\":"<<n<<",\"excluded_by_16_outsider_gate\":"<<excluded
          <<",\"not_excluded\":"<<(n-excluded)<<",\"max_admissible_outsiders\":"<<maximum
          <<",\"incidence_count\":"<<total<<",\"histogram\":{";
 bool first=true;for(auto [k,v]:hist){if(!first)std::cout<<',';first=false;std::cout<<'"'<<k<<"\":"<<v;}
 std::cout<<"},\"max_groups\":[";first=true;
 for(auto mask:maxMasks){if(!first)std::cout<<',';first=false;std::cout<<'[';
  bool first2=true;for(int f=0;f<27;f++)if(mask&(1u<<f)){if(!first2)std::cout<<',';first2=false;std::cout<<f;}
  std::cout<<']';}
 std::cout<<"]}\n";
 return 0;
}
