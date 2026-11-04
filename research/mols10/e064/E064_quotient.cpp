#include <bits/stdc++.h>
using namespace std;
using P=array<uint8_t,9>;
int fact[]={1,1,2,6,24,120,720,5040,40320,362880};
int rank9(const P&a){int k=0;for(int i=0;i<9;i++){int less=0;for(int j=i+1;j<9;j++)less+=(a[j]<a[i]);k+=less*fact[8-i];}return k;}
P invers(const P&a){P q;for(int i=0;i<9;i++)q[a[i]]=i;return q;}
P comp(const P&a,const P&b){P h;for(int i=0;i<9;i++)h[i]=a[b[i]];return h;}
vector<int> parsearr(const string&s,const string& name){size_t start=s.find("\""+name+"\":[");if(start==string::npos)throw runtime_error("no "+name);start+=name.size()+4;size_t end=s.find(']',start);vector<int>v;string p=s.substr(start,end-start);stringstream ss(p);string t;while(getline(ss,t,','))v.push_back(stoi(t));return v;}
P pack(const vector<int>&x){P p;if(x.size()!=9)throw runtime_error("not nine");for(int i=0;i<9;i++)p[i]=x[i];return p;}
struct Entry{P f,g;vector<int> typ;};
vector<vector<int>> types;
void parts(int rem,int k,vector<int>cur){if(rem==0){types.push_back(cur);return;}for(int i=k;i<=rem;i++)if(i>=2){auto a=cur;a.push_back(i);parts(rem-i,i,a);}}
vector<vector<P>> centrals;
vector<P> makecentral(const vector<int>&typ){vector<vector<int>> cycles;int i=0;for(int x:typ){vector<int>cy;for(int j=0;j<x;j++)cy.push_back(i+j);cycles.push_back(cy);i+=x;}vector<vector<vector<int>>> groups;for(auto&cy:cycles){if(groups.empty()||groups.back()[0].size()!=cy.size())groups.push_back({});groups.back().push_back(cy);}vector<P> autos;P p{};function<void(int)> recgroup=[&](int g){if(g==groups.size()){autos.push_back(p);return;}auto&group=groups[g];int m=group.size(),len=group[0].size();vector<int>perm(m);iota(perm.begin(),perm.end(),0);do{function<void(int)> recursion=[&](int q){if(q==m){recgroup(g+1);return;}for(int rotation=0;rotation<len;rotation++){for(int j=0;j<len;j++)p[group[q][j]]=group[perm[q]][(j+rotation)%len];recursion(q+1);}};recursion(0);}while(next_permutation(perm.begin(),perm.end()));};recgroup(0);return autos;}
int find_type(const vector<int>&v){for(size_t i=0;i<types.size();i++)if(types[i]==v)return i;throw runtime_error("type lookup failed");}
struct DSU{vector<int> par;DSU(int n):par(n){iota(par.begin(),par.end(),0);}int find(int x){return par[x]==x?x:par[x]=find(par[x]);}void join(int a,int b){a=find(a);b=find(b);if(a!=b)par[max(a,b)]=min(a,b);}};
int main(){parts(9,2,{});for(auto typ:types)centrals.push_back(makecentral(typ));vector<Entry> e;string line;ifstream in("E064_ordered_representatives.jsonl");while(getline(in,line))e.push_back({pack(parsearr(line,"f")),pack(parsearr(line,"g")),parsearr(line,"type")});if(e.size()!=16085)throw runtime_error("bad input count");unordered_map<int,int> key;key.reserve(e.size()*2);for(int i=0;i<e.size();i++)key[find_type(e[i].typ)*362880+rank9(e[i].g)]=i;
 auto canonical=[&](P f,P g)->int{
    vector<vector<int>> cy;P seen{};for(int i=0;i<9;i++)if(!seen[i]){vector<int> x;int j=i;do{x.push_back(j);seen[j]=1;j=f[j];}while(j!=i);int pos=min_element(x.begin(),x.end())-x.begin();rotate(x.begin(),x.begin()+pos,x.end());cy.push_back(x);}sort(cy.begin(),cy.end(),[](const auto&a,const auto&b){if(a.size()!=b.size())return a.size()<b.size();return a[0]<b[0];});vector<int> tp;P p;int k=0;for(auto &x:cy){tp.push_back(x.size());for(int t:x)p[t]=k++;}int id=find_type(tp);P h;for(int j=0;j<9;j++)h[p[j]]=p[g[j]];P best;best.fill(255);for(auto &q:centrals[id]){P z;for(int j=0;j<9;j++)z[q[j]]=q[h[j]];if(z<best)best=z;}auto it=key.find(id*362880+rank9(best));if(it==key.end())throw runtime_error("canonical representative absent");return it->second;
 };
 vector<int> BC(e.size()),AB(e.size());DSU d(e.size());for(int i=0;i<e.size();i++){auto f=e[i].f,g=e[i].g,fi=invers(f);BC[i]=canonical(g,f);AB[i]=canonical(fi,comp(g,fi));d.join(i,BC[i]);d.join(i,AB[i]);}
 for(int i=0;i<e.size();i++){if(BC[BC[i]]!=i || AB[AB[i]]!=i)throw runtime_error("not involutions");if(BC[AB[BC[AB[BC[AB[i]]]]]]!=i)throw runtime_error("S3 relation fail");}
 long fix_bc=0,fix_ab=0,fix_ac=0,fix_cycle1=0,fix_cycle2=0;for(int i=0;i<e.size();i++){fix_bc+=BC[i]==i;fix_ab+=AB[i]==i;fix_ac+=(BC[AB[BC[i]]]==i);fix_cycle1+=(BC[AB[i]]==i);fix_cycle2+=(AB[BC[i]]==i);}
 map<int,vector<int>> comps;for(int i=0;i<e.size();i++)comps[d.find(i)].push_back(i);long burnside_num=(long)e.size()+fix_bc+fix_ab+fix_ac+fix_cycle1+fix_cycle2;if(burnside_num%6||burnside_num/6!=comps.size())throw runtime_error("independent Burnside disagree");map<int,int>size_hist;for(auto [id,v]:comps)size_hist[v.size()]++;
 ofstream out("E064_quotient_representatives.jsonl");for(auto&[id,v]:comps){auto&z=e[id];out<<"{\"ordered_orbit_id\":"<<id<<",\"type\":[";for(int i=0;i<z.typ.size();i++){if(i)out<<",";out<<z.typ[i];}out<<"],\"B_col0\":[0";for(int i=0;i<9;i++)out<<","<<int(z.f[i])+1;out<<"],\"C_col0\":[0";for(int i=0;i<9;i++)out<<","<<int(z.g[i])+1;out<<"],\"S3_orbit_size\":"<<v.size()<<"}\n";}
 vector<int> IX(e.size());DSU d12(e.size());for(int i=0;i<(int)e.size();i++){
   IX[i]=canonical(invers(e[i].f),invers(e[i].g));
   d12.join(i,BC[i]);d12.join(i,AB[i]);d12.join(i,IX[i]);
 }
 for(int i=0;i<(int)e.size();i++){
   if(IX[IX[i]]!=i)throw runtime_error("inversion not involution");
   if(IX[BC[i]]!=BC[IX[i]] || IX[AB[i]]!=AB[IX[i]])throw runtime_error("inversion not commuting with S3");
 }
 map<int,vector<int>> classes12;for(int i=0;i<(int)e.size();i++)classes12[d12.find(i)].push_back(i);
 long burn12=0;map<int,int>hist12;for(int i=0;i<(int)e.size();i++){
   int all[12]={i,BC[i],AB[i],BC[AB[i]],AB[BC[i]],BC[AB[BC[i]]],IX[i],BC[IX[i]],AB[IX[i]],BC[AB[IX[i]]],AB[BC[IX[i]]],BC[AB[BC[IX[i]]]]};
   for(int k:all)burn12+=(k==i);
 }
 if(burn12%12 || burn12/12 != classes12.size())throw runtime_error("Burnside12 fails");
 ofstream out12("E064_12_representatives.jsonl");
 for(auto &[rep,v]:classes12){auto &z=e[rep];hist12[v.size()]++;out12<<"{\"ordered_orbit_id\":"<<rep<<",\"type\":[";
 for(int i=0;i<(int)z.typ.size();i++){if(i)out12<<",";out12<<z.typ[i];}
 out12<<"],\"B_col0\":[0";for(int i=0;i<9;i++)out12<<","<<int(z.f[i])+1;
 out12<<"],\"C_col0\":[0";for(int i=0;i<9;i++)out12<<","<<int(z.g[i])+1;
 out12<<"],\"S3xC2_orbit_size\":"<<v.size()<<"}\n";
 }
 cout<<"E064_TWELVE {\"ordered_orbits\":"<<e.size()<<",\"S3xC2_orbits\":"<<classes12.size()<<",\"burnside_sum\":"<<burn12<<",\"orbit_size_hist\":{";
 int ccc=0;for(auto [k,v]:hist12){if(ccc++)cout<<",";cout<<"\""<<k<<"\":"<<v;}cout<<"}}\n";
 cout<<"{\"ordered_orbits\":"<<e.size()<<",\"S3_unordered_orbits\":"<<comps.size()<<",\"fixed_BC\":"<<fix_bc<<",\"fixed_AB\":"<<fix_ab<<",\"fixed_AC\":"<<fix_ac<<",\"fixed_cycle1\":"<<fix_cycle1<<",\"fixed_cycle2\":"<<fix_cycle2<<",\"S3_orbit_size_hist\":{";int v=0;for(auto [a,b]:size_hist){if(v++)cout<<",";cout<<"\""<<a<<"\":"<<b;}cout<<"}}\n";
}