// Exact 237 candidate construction in 112+112+third family, with rigorous
// Fourier/self-dual intersection prefilter. NOT exhaustive over GL(6,3).
#include <bits/stdc++.h>
using namespace std;
using VI=array<uint8_t,6>; using MR=array<int,6>;
static VI vec[729];
static uint8_t dotv[729][729];
static uint16_t tr[729][729],radd1[729][729],radd2[729][729];
static uint16_t dbl[729];
static uint8_t inS[729];
static int S[112],T[112];
int en(const VI&v){int x=0;for(int i=0;i<6;i++)x=3*x+v[i];return x;}
void init(){
 for(int a=0;a<729;a++){int q=a;for(int i=5;i>=0;i--){vec[a][i]=q%3;q/=3;}}
 for(int a=0;a<729;a++)for(int b=0;b<729;b++){
  int dp=0,ab1=0,ab2=0,tt=0;
  for(int i=0;i<6;i++){
   dp+=vec[a][i]*vec[b][i];ab1=3*ab1+(vec[a][i]+vec[b][i])%3;
   ab2=3*ab2+(vec[a][i]+2*vec[b][i])%3;tt=3*tt+(6-vec[a][i]-vec[b][i])%3;
  }
  dotv[a][b]=dp%3;radd1[a][b]=ab1;radd2[a][b]=ab2;tr[a][b]=tt;
 }
 for(int a=0;a<729;a++)dbl[a]=radd1[a][a];
 const char *witness_path=getenv("CAPSET_WITNESS");
 if(witness_path==nullptr){
  ifstream repo("research/capset_f3_7/candidates/calderbank_fishburn_236.txt");
  witness_path=repo.good()?"research/capset_f3_7/candidates/calderbank_fishburn_236.txt":"witness236.txt";
 }
 ifstream f(witness_path);string s;int nS=0,nT=0;
 while(getline(f,s))if(s.size()==7&&s.find_first_not_of("012")==string::npos){int p=0;for(int k=1;k<7;k++)p=p*3+s[k]-'0';if(s[0]=='0')S[nS++]=p;if(s[0]=='1')T[nT++]=p;}
 assert(nS==112&&nT==112);
 for(int p:S)inS[p]=1;
}
MR identity(){MR M{};for(int i=0;i<6;i++){VI v{};v[i]=1;M[i]=en(v);}return M;}
void mutate(MR &M,mt19937_64 &rng){int k=rng()%100;
 if(k<72){int a=rng()%6,b=rng()%5;if(b>=a)b++;M[a]=(rng()%2?radd1[M[a]][M[b]]:radd2[M[a]][M[b]]);}
 else if(k<86){int a=rng()%6,b=rng()%6;swap(M[a],M[b]);}
 else{int a=rng()%6;M[a]=dbl[M[a]];}
}
uint64_t key(const MR &M){uint64_t out=0;for(int a:M)out=729*out+a;return out;}
void transform(const MR&M,int (&B)[112],int&t){t=0;for(int j=0;j<112;j++){
 int p=T[j],z=0;for(int i=0;i<6;i++)z=3*z+dotv[M[i]][p];B[j]=z;t+=inS[z];
}}
vector<int> holes(const int (&B)[112]){
 uint8_t blocked[729]={};for(int a:S)for(int b:B)blocked[tr[a][b]]=1;
 vector<int> h;for(int i=0;i<729;i++)if(!blocked[i])h.push_back(i);return h;
}
bool cap13(const vector<int>&h,vector<int>&out){
 vector<int> now;long long nodes=0;const long long limit=1'000'000;
 function<bool(int)>dfs=[&](int j){if(now.size()>=13){out=now;return true;}
 if(j>=(int)h.size()||now.size()+h.size()-j<13||++nodes>limit)return false;
 for(int i=j;i<(int)h.size();i++){
  int p=h[i];bool good=true;for(int a=0;a<(int)now.size()&&good;a++)for(int b=a+1;b<(int)now.size();b++)if(tr[now[a]][now[b]]==p){good=false;break;}
  if(good){now.push_back(p);if(dfs(i+1))return true;now.pop_back();}
 }return false;};return dfs(0);
}
bool verifyFull(const int (&B)[112],const vector<int>&c){
 set<array<int,7>>X;for(int p:S){array<int,7> x{};for(int j=0;j<6;j++)x[j+1]=vec[p][j];X.insert(x);}
 for(int p:B){array<int,7> x{};x[0]=1;for(int j=0;j<6;j++)x[j+1]=vec[p][j];X.insert(x);}
 for(int p:c){array<int,7> x{};x[0]=2;for(int j=0;j<6;j++)x[j+1]=vec[p][j];X.insert(x);}
 if(X.size()<237)return false;
 for(auto a=X.begin();a!=X.end();a++)for(auto b=next(a);b!=X.end();b++){
  array<int,7> z{};for(int j=0;j<7;j++)z[j]=(6-(*a)[j]-(*b)[j])%3;if(X.count(z))return false;
 }
 ofstream f("WITNESS_237.txt");f<<"n: 7\n";for(auto x:X){for(int i:x)f<<i;f<<"\n";}return true;
}
int main(int argc,char**argv){
 int trials=4000000;uint64_t seed=2026110308;if(argc>1)trials=atoi(argv[1]);if(argc>2)seed=strtoull(argv[2],nullptr,10);
 init();mt19937_64 rng(seed);MR M=identity();
 unordered_set<uint64_t>seen;seen.reserve(trials+100);map<int,int>thist,hhist;int evaluated=0,best=0,dup=0,large=0;
 auto start=chrono::steady_clock::now();int B[112]{};
 for(int step=0;step<trials;step++){
  if(step%31==0)M=identity();
  for(int j=0;j<1+(rng()%15);j++)mutate(M,rng);
  auto k=key(M);if(!seen.insert(k).second){dup++;continue;}
  int t=0;transform(M,B,t);thist[t]++;
  // Spectral identity proved from self-duality shows that for 0<t<32
  // the convolution has NO zero. If t=0, only zero itself is a hole.
  if(t>0 && t<32)continue;
  vector<int>H=holes(B);int h=H.size();evaluated++;hhist[h]++;
  if(h>best){best=h;cout<<"NEW_BEST step="<<step<<" intersect="<<t<<" holes="<<h<<"\n"<<flush;}
  if(h>=13){large++;vector<int>C;
   if(cap13(H,C)&&verifyFull(B,C)){cout<<"FOUND_NEW_CAP_237 verified\n";return 0;}
  }
 }
 double secs=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<"DONE trials="<<trials<<" unique="<<seen.size()<<" dup="<<dup<<" seed="<<seed<<" evaluated_holes="<<evaluated<<" max_holes="<<best<<" >=13_hole_cases="<<large<<" elapsed_sec="<<secs<<"\n";
 for(auto [t,n]:thist)cout<<"intersection="<<t<<":"<<n<<" ";cout<<"\n";
 for(auto [h,n]:hhist)cout<<"holes="<<h<<":"<<n<<" ";cout<<"\n";
}
