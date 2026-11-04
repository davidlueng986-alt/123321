#include <bits/stdc++.h>
using namespace std;
using P=array<unsigned char,9>;
vector<vector<int>> parts;
void genparts(int rem,int mn,vector<int> x){if(rem==0){parts.push_back(x);return;}for(int i=mn;i<=rem;i++){if(i==1)continue;auto y=x;y.push_back(i);genparts(rem-i,i,y);}}
int main(){genparts(9,2,{});long total=0;for(auto typ:parts){P f{};vector<vector<int>> cyc;int v=0;for(int len:typ){vector<int> c;for(int i=0;i<len;i++){c.push_back(v+i);f[v+i]=v+(i+1)%len;}cyc.push_back(c);v+=len;}
 vector<vector<vector<int>>> groups;
 for(auto &c:cyc){if(groups.empty()||groups.back()[0].size()!=c.size())groups.push_back({});groups.back().push_back(c);}
 vector<P> autom;P p{};
 function<void(int)> group=[&](int gi){if(gi==(int)groups.size()){autom.push_back(p);return;}auto &grp=groups[gi];int m=grp.size(),l=grp[0].size();vector<int>perm(m);iota(perm.begin(),perm.end(),0);do{function<void(int)>offset=[&](int ix){if(ix==m){group(gi+1);return;}for(int z=0;z<l;z++){for(int j=0;j<l;j++)p[grp[ix][j]]=grp[perm[ix]][(j+z)%l];offset(ix+1);}};offset(0);}while(next_permutation(perm.begin(),perm.end()));};group(0);
 vector<P> allowed;P g; iota(g.begin(),g.end(),0);do{bool ok=true;for(int i=0;i<9;i++)if(g[i]==i||g[i]==f[i]){ok=false;break;}if(ok)allowed.push_back(g);}while(next_permutation(g.begin(),g.end()));long fixedsum=0;for(const auto&p:autom){for(const auto&g:allowed){bool fixed=true;for(int i=0;i<9;i++)if(g[p[i]]!=p[g[i]]){fixed=false;break;}fixedsum+=fixed;}}
 assert(fixedsum%(long)autom.size()==0);long orbits=fixedsum/autom.size();total+=orbits;cout<<"{\"type\":[";for(size_t i=0;i<typ.size();i++){if(i)cout<<",";cout<<typ[i];}cout<<"],\"centralizer\":"<<autom.size()<<",\"allowed_g\":"<<allowed.size()<<",\"fixed_sum\":"<<fixedsum<<",\"orbits\":"<<orbits<<"}\n";
 }cout<<"TOTAL "<<total<<"\n";}