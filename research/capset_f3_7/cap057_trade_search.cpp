#include <array>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>
#include <tuple>
#include <cassert>
#include <chrono>
using namespace std;
constexpr int N=2187, K=236;
static uint16_t third[N][N];
static array<array<uint8_t,7>,N> D;
static vector<int> A;
static int cov0[N];
static array<bool,N> oldcap;
int code(string x){int y=0;for(char c:x)y=y*3+c-'0';return y;}
void init(){
 for(int i=0;i<N;i++){int x=i;for(int j=6;j>=0;j--){D[i][j]=x%3;x/=3;}}
 for(int i=0;i<N;i++)for(int j=0;j<N;j++){
  int s=0;for(int k=0;k<7;k++)s=3*s+(6-D[i][k]-D[j][k])%3;third[i][j]=s;
 }
 ifstream f("/mnt/data/capset_v5/witness236.txt");string x;
 while(f>>x)if(x.size()==7 && x.find_first_not_of("012")==string::npos)A.push_back(code(x));
 assert(A.size()==K);
 for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)cov0[third[A[i]][A[j]]]++;
 for(int p:A){assert(!cov0[p]);oldcap[p]=true;}
}
int main(){init();
 auto start=chrono::steady_clock::now();
 long long total=0,promising=0;int maxF=-1,maxouts=-1;int maxQ=-1,maxmask=-1;array<int,80> hist{};
 int minD=100;
 for(int q=0;q<N;q++)if(!oldcap[q]&&cov0[q]<minD)minD=cov0[q];
 for(int q=0;q<N;q++)if(!oldcap[q]&&cov0[q]==minD){
  vector<pair<int,int>> M;
  for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)if(third[A[i]][A[j]]==q)M.push_back({i,j});
  assert((int)M.size()==minD);
  int localMax=-1,good=0;
  for(int mask=0;mask<(1<<minD);mask++){
   int cov[N];copy(cov0,cov0+N,cov);
   bool excluded[K]={};int rem[20];
   for(int i=0;i<minD;i++){rem[i]=(mask&(1<<i))?M[i].second:M[i].first;excluded[rem[i]]=true;}
   for(int i=0;i<minD;i++)for(int j=0;j<K;j++)if(j!=rem[i])cov[third[A[rem[i]]][A[j]]]--;
   for(int i=0;i<minD;i++)for(int j=i+1;j<minD;j++)cov[third[A[rem[i]]][A[rem[j]]]]++;
   assert(cov[q]==0);
   bool no[N]={};
   for(int i=0;i<K;i++)if(!excluded[i]){
    no[A[i]]=true;no[third[q][A[i]]]=true;
   }
   no[q]=true;
   int freeCount=0,outsiderCount=0;
   vector<int> freePoints;
   for(int p=0;p<N;p++)if(!no[p] && cov[p]==0){freeCount++;outsiderCount+=!oldcap[p];freePoints.push_back(p);}
   if(freeCount>maxF){maxF=freeCount;maxouts=outsiderCount;maxQ=q;maxmask=mask;}
   localMax=max(localMax,freeCount);if(freeCount>=minD){good++;promising++;}
   total++;hist[min(freeCount,79)]++;
   if(freeCount>=minD){
    // Write a complete local SAT subinstance for independent solving.
    // Keep has exactly 236-minD selected, plus q=1; >=minD free additions ->237.
    ofstream o("/mnt/data/capset_v5/trade_candidate.txt");
    o<<"q "<<q<<" mask "<<mask<<" d "<<minD<<" free "<<freeCount<<"\n";
    o<<"keep";for(int i=0;i<K;i++)if(!excluded[i])o<<' '<<A[i];o<<' '<<q<<"\nfree";
    for(int p:freePoints)o<<' '<<p;o<<"\n";
    cout<<"POTENTIAL q="<<q<<" mask="<<mask<<" d="<<minD<<" free="<<freeCount<<"\n";
    if(freeCount>=minD+2)break;
   }
  }
  cout<<"EXTERNAL q="<<q<<" secant_degree="<<minD<<" best_eligible="<<localMax<<" orientations_eligible_for_237="<<good<<"\n";
 }
 double t=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<"FINAL minDegree="<<minD<<" total_orientations="<<total<<" promising="<<promising<<" max_free="<<maxF<<" best_q="<<maxQ<<" best_mask="<<maxmask<<" elapsed="<<t<<"\n";
 for(int i=0;i<80;i++)if(hist[i])cout<<i<<":"<<hist[i]<<" ";cout<<"\n";
}
