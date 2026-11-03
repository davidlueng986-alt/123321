#include <bits/stdc++.h>
using namespace std;
#include "E061_base.h"
struct Move{int s,a,b,mask;};
struct Engine {
  long long nodes=0,trades=0; int best=291,depthbest[4]={291,0,0,0}; vector<Move> stack,best_path; bool found=false;int answer[3][10][10]={};
  int score(int out[3]) {
    const int pair[3][2]={{0,1},{0,2},{1,2}};int tot=0;
    for(int p=0;p<3;p++){bool seen[100]={};int count=0;
      for(int r=0;r<10;r++)for(int c=0;c<10;c++){
       int k=Q[pair[p][0]][r][c]*10+Q[pair[p][1]][r][c];
       if(!seen[k]){seen[k]=true;count++;}
      }
      out[p]=count;tot+=count;
    }
    return tot;
  }
  void apply(Move m){for(int r=0;r<10;r++)if((m.mask>>r)&1)for(int c=0;c<10;c++){
     int &v=Q[m.s][r][c];if(v==m.a)v=m.b;else if(v==m.b)v=m.a;
  }}
  vector<Move> moves(){vector<Move> v;v.reserve(240);
   for(int s=0;s<3;s++)for(int a=0;a<10;a++)for(int b=a+1;b<10;b++){
     int parent[10],roots[10]={};iota(parent,parent+10,0);
     auto find=[&](int x){while(x!=parent[x])x=parent[x];return x;};
     for(int r=0;r<10;r++){
      int ca=-1,cb=-1;for(int c=0;c<10;c++){if(Q[s][r][c]==a)ca=c;if(Q[s][r][c]==b)cb=c;}
      if(ca<0||cb<0)abort();int x=find(ca),y=find(cb);parent[x]=y;
     }
     for(int r=0;r<10;r++)for(int c=0;c<10;c++)if(Q[s][r][c]==a)roots[find(c)]|=1<<r;
     for(int c=0;c<10;c++)if(roots[c]){
      int mask=roots[c],other=(1023^mask);if(other==0)continue;
      if(mask>other)mask=other;
      bool exists=false;
      // complementary pairs collapse, but distinct components not otherwise duplicated
      for(int j=0;j<(int)v.size();j++)if(v[j].s==s&&v[j].a==a&&v[j].b==b&&v[j].mask==mask){exists=true;break;}
      if(!exists)v.push_back({s,a,b,mask});
     }
   }
   return v;
  }
  void dfs(int depth){nodes++;int overlays[3];int sc=score(overlays);
   if(sc>depthbest[depth])depthbest[depth]=sc;
   if(sc>best){best=sc;best_path=stack;cerr<<"IMPROVED depth="<<depth<<" score="<<sc<<" overlays="<<overlays[0]<<","<<overlays[1]<<","<<overlays[2]<<" nodes="<<nodes<<"\n";
      memcpy(answer,Q,sizeof(Q));if(sc==300){found=true;return;}
   }
   if(depth==3)return;
   auto opts=moves();trades+=opts.size();
   for(auto m:opts){
     if(!stack.empty()&&m.s==stack.back().s&&m.a==stack.back().a&&m.b==stack.back().b&&m.mask==stack.back().mask)continue;
     apply(m);stack.push_back(m);dfs(depth+1);stack.pop_back();apply(m);
     if(found)return;
   }
  }
};
int main(){Engine E;auto start=chrono::steady_clock::now();E.dfs(0);double t=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"{\"base\":291,\"best\":"<<E.best<<",\"nodes\":"<<E.nodes<<",\"trades_generated\":"<<E.trades<<",\"seconds\":"<<setprecision(4)<<t<<",\"best_by_depth\":[";
  for(int i=0;i<=3;i++){if(i)cout<<",";cout<<E.depthbest[i];}cout<<"],\"witness\":";
  if(E.best==291)cout<<"null";
  else{cout<<"[";for(int s=0;s<3;s++){if(s)cout<<",";cout<<"[";for(int r=0;r<10;r++){if(r)cout<<",";cout<<"[";for(int c=0;c<10;c++){if(c)cout<<",";cout<<E.answer[s][r][c];}cout<<"]";}cout<<"]";}cout<<"]";}
  cout<<",\"moves\":[";for(int i=0;i<(int)E.best_path.size();i++){auto m=E.best_path[i];if(i)cout<<",";cout<<"["<<m.s<<","<<m.a<<","<<m.b<<","<<m.mask<<"]";}cout<<"],\"scope\":\"up to 3 symbol-pair cycle trades on one fixed Egan neartriple; complements quotient by global symbol relabeling\"}\n";
}