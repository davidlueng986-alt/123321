#include <bits/stdc++.h>
using namespace std;
using Clock=chrono::steady_clock;
struct Candidate {int r,c,a,b,d;};
struct DLX {
 bool use_psd=false;
 int feat_dim=0;
 vector<double> feat,root_pinv;
 long long psd_numerical_rejects=0, psd_uncertified=0;
 vector<vector<double>> chol;
 vector<int> selected_interior;
 long long psd_prunes=0, psd_tests=0;
 bool printed_first_cut=false;
 static int point_id(Candidate p){return ((((p.r*10+p.c)*10+p.a)*10+p.b)*10+p.d);}
 bool load_psd(const string& path){
  ifstream in(path,ios::binary); if(!in)throw runtime_error("missing PSD feature file");
  int count=0;in.read((char*)&count,4);in.read((char*)&feat_dim,4);
  if(count!=100000 || feat_dim!=17)throw runtime_error("bad PSD feature dimensions");
  feat.resize((size_t)count*feat_dim);in.read((char*)feat.data(),feat.size()*sizeof(double));
  if(!in)throw runtime_error("truncated features");
  root_pinv.resize(19*19);in.read((char*)root_pinv.data(),root_pinv.size()*sizeof(double));
  if(!in)throw runtime_error("missing root pseudoinverse");
  use_psd=true;return true;
 }
 double dot_feature(int u,int v){
  int p=point_id(cand[u]),q=point_id(cand[v]);
  double ans=0;for(int k=0;k<feat_dim;k++)ans+=feat[(size_t)p*feat_dim+k]*feat[(size_t)q*feat_dim+k];
  return ans;
 }

 bool verify_exact_R4_conflict(int id,const vector<double>&y,long long&outQ,vector<long long>&outVec){
  int d=selected_interior.size();
  vector<double> coeff(d+1);coeff[d]=1;
  for(int j=d-1;j>=0;j--){
   double val=-y[j];for(int k=j+1;k<d;k++)val-=chol[k][j]*coeff[k];
   coeff[j]=val/chol[j][j];
  }
  vector<double> bsum(19,0);
  for(int h=0;h<=d;h++){
   int cid=(h==d? id : selected_interior[h]);auto p=cand[cid];
   for(int j=0;j<19;j++){
    auto root=cand[chosen[j]];
    int same=(p.r==root.r)+(p.c==root.c)+(p.a==root.a)+(p.b==root.b)+(p.d==root.d);
    if(same>1)abort();
    bsum[j]+=coeff[h]*(2.0-5.0*(same==1));
   }
  }
  vector<double> qf(19+d+1);
  for(int j=0;j<19;j++){
   double val=0;for(int k=0;k<19;k++)val-=root_pinv[j*19+k]*bsum[k];
   qf[j]=val;
  }
  for(int k=0;k<=d;k++)qf[19+k]=coeff[k];
  const double scales[]={30.0,100.0,300.0,1000.0,3000.0,10000.0,30000.0,100000.0};
  for(double scale:scales){
   vector<long long> q(qf.size());long long weight=0;
   for(size_t i=0;i<q.size();i++){
    if(!isfinite(qf[i]) || abs(qf[i]*scale)>1e9)return false;
    q[i]=llround(qf[i]*scale);weight+=llabs(q[i]);
   }
   if(weight==0)continue;
   __int128 lines[5][10]={};__int128 sum=0,sum2=0;
   for(size_t j=0;j<q.size();j++){
    int cid=j<19? chosen[j] : (j==q.size()-1?id:selected_interior[j-19]);
    auto p=cand[cid];int a[]={p.r,p.c,p.a,p.b,p.d};
    sum+=q[j];sum2+=(__int128)q[j]*q[j];
    for(int k=0;k<5;k++)lines[k][a[k]]+=q[j];
   }
   __int128 val=50*sum2+2*sum*sum;
   for(int k=0;k<5;k++)for(int w=0;w<10;w++)val-=5*lines[k][w]*lines[k][w];
   if(val<0){outVec=q;outQ=(long long)val;return true;}
  }
  return false;
 }
 bool psd_push(int id){
  psd_tests++;
  double diag=27.0-dot_feature(id,id)+1e-7;int m=selected_interior.size();
  vector<double> y(m);
  for(int i=0;i<m;i++){
   auto a=cand[id],b=cand[selected_interior[i]];
   int same=(a.r==b.r)+(a.c==b.c)+(a.a==b.a)+(a.b==b.b)+(a.d==b.d);
   if(same>1)abort();
   double val=2.0-5.0*(same==1)-dot_feature(id,selected_interior[i]);
   for(int j=0;j<i;j++)val-=chol[i][j]*y[j];
   y[i]=val/chol[i][i];diag-=y[i]*y[i];
  }
  if(diag < -1e-5){
   psd_numerical_rejects++;
   long long intQ=0;vector<long long> cert;
   if(verify_exact_R4_conflict(id,y,intQ,cert)){
    psd_prunes++;
    if(!printed_first_cut){
     printed_first_cut=true;
     ofstream out("E070_DLX_FIRST_CUT_LIVE.json");
     out<<"{\"points\":["; bool first=true;
     auto emit=[&](Candidate p){if(!first)out<<",";first=false;
      out<<"["<<p.r<<","<<p.c<<","<<p.a<<","<<p.b<<","<<p.d<<"]";};
     for(int j=0;j<19;j++)emit(cand[chosen[j]]);
     for(int cid:selected_interior)emit(cand[cid]);
     emit(cand[id]);out<<"],\"integer_test_vector\":[";
     for(size_t j=0;j<cert.size();j++){if(j)out<<",";out<<cert[j];}
     out<<"],\"exact_negative_quadratic\":"<<intQ<<"}\n";
    }
    return false;
   } else psd_uncertified++;
  }
  if(diag<1e-7)diag=1e-7; // conservative regularization, benchmark ONLY, not proof
  y.push_back(sqrt(diag)); chol.push_back(move(y)); selected_interior.push_back(id);
  return true;
 }
 void psd_pop(){chol.pop_back();selected_interior.pop_back();}
 void select_forced_roots(){
  // First row has fixed A/B/C, first column A(r,0)=r and caller fixes B/C.
  for(int r=0;r<n;r++)for(int c=0;c<n;c++)if(r==0||c==0){
   int id=-1;
   for(int i=0;i<(int)cand.size();i++)if(cand[i].r==r && cand[i].c==c){id=i;break;}
   if(id<0)throw runtime_error("missing forced root placement");
   chosen.push_back(id);
   for(int col:cs[id])cover(col+1);
  }
  if((int)chosen.size()!=2*n-1)throw runtime_error("root selection failed");
 }

 int n,roots,head,tot, selected=0,maxdepth=0;
 vector<int> L,R,U,D,C,S,ROW; vector<Candidate> cand; vector<array<int,10>> cs;
 vector<int> chosen,solution; long long nodes=0, prune=0, branches=0; bool timedout=false; Clock::time_point started; double limit=5.0; long long node_budget=1000000;
 DLX(int n_):n(n_),roots(10*n*n),head(0),tot(roots+1){
  L.resize(roots+1);R.resize(roots+1);U.resize(roots+1);D.resize(roots+1);C.resize(roots+1);S.resize(roots+1);ROW.resize(roots+1);
  for(int i=0;i<=roots;i++){L[i]=i-1;R[i]=i+1;U[i]=D[i]=i;C[i]=i;}
  L[0]=roots;R[roots]=0;
 }
 void add(int r,int c,int a,int b,int d){
   int id=cand.size();cand.push_back({r,c,a,b,d});
   array<int,10> cols{};cols[0]=r*n+c;
   int x[3]={a,b,d};
   for(int i=0;i<3;i++){
    cols[1+2*i]=n*n+(2*i)*n*n+r*n+x[i];
    cols[2+2*i]=n*n+(2*i+1)*n*n+c*n+x[i];
   }
   cols[7]=7*n*n+a*n+b;cols[8]=8*n*n+a*n+d;cols[9]=9*n*n+b*n+d;
   int first=tot;
   for(int k=0;k<10;k++){
    int col=cols[k]+1;int u=U[col];
    U.push_back(u);D.push_back(col);L.push_back(tot-1);R.push_back(tot+1);C.push_back(col);S.push_back(0);ROW.push_back(id);
    U[col]=tot;D[u]=tot;S[col]++;tot++;
   }
   L[first]=tot-1;R[tot-1]=first;
   cs.push_back(cols);
 }
 void cover(int c){R[L[c]]=R[c];L[R[c]]=L[c];for(int i=D[c];i!=c;i=D[i])for(int j=R[i];j!=i;j=R[j]){U[D[j]]=U[j];D[U[j]]=D[j];S[C[j]]--;}}
 void uncover(int c){for(int i=U[c];i!=c;i=U[i])for(int j=L[i];j!=i;j=L[j]){S[C[j]]++;U[D[j]]=j;D[U[j]]=j;}R[L[c]]=c;L[R[c]]=c;}
 bool go(int d){
  nodes++;if(d>maxdepth)maxdepth=d;
  if(nodes>=node_budget || ((nodes&16383)==0 && chrono::duration<double>(Clock::now()-started).count()>limit)) {timedout=true;return false;}
  if(R[head]==head){solution=chosen;return true;}
  int c=-1,best=INT_MAX;
  for(int i=R[head];i!=head;i=R[i]){if(S[i]<best){best=S[i];c=i;if(best<=1)break;}}
  if(best==0){prune++;return false;}
  cover(c);
  for(int r=D[c];r!=c;r=D[r]){
   int id=ROW[r];
   if(use_psd && !psd_push(id))continue;
   chosen.push_back(id); branches++;
   for(int j=R[r];j!=r;j=R[j])cover(C[j]);
   if(go(d+1))return true;
   for(int j=L[r];j!=r;j=L[j])uncover(C[j]);
   chosen.pop_back();
   if(use_psd)psd_pop();
   if(timedout)break;
  }
  uncover(c);
  return false;
 }
 string solve(double secs,long long nbudget){limit=secs;node_budget=nbudget;started=Clock::now();bool sat=go((int)chosen.size());double elapsed=chrono::duration<double>(Clock::now()-started).count();
  string status=sat?"SAT":timedout?"UNKNOWN_BUDGET":"UNSAT_EXHAUSTIVE";
  cerr << "E061 order "<<n<<" candidates "<<cand.size()<<" nodes "<<nodes<<" branches "<<branches<<" prune "<<prune<<" maxdepth "<<maxdepth<<" psd_tests "<<psd_tests<<" psd_cuts "<<psd_prunes<<" psd_uncertified "<<psd_uncertified<<" sec "<<elapsed<<" status "<<status<<"\n";
  cout << "{\"n\":"<<n<<",\"status\":\""<<status<<"\",\"candidates\":"<<cand.size()<<",\"nodes\":"<<nodes<<",\"branches\":"<<branches<<",\"dead_ends\":"<<prune<<",\"maxdepth\":"<<maxdepth<<",\"psd_tests\":"<<psd_tests<<",\"psd_cuts\":"<<psd_prunes<<",\"psd_uncertified\":"<<psd_uncertified<<",\"seconds\":"<<setprecision(5)<<elapsed;
  if(sat){vector<vector<vector<int>>> mats(3,vector<vector<int>>(n,vector<int>(n,-1)));for(int id:solution){auto v=cand[id];mats[0][v.r][v.c]=v.a;mats[1][v.r][v.c]=v.b;mats[2][v.r][v.c]=v.d;}for(auto&m:mats)for(auto&row:m)for(int v:row)if(v<0)abort();cout<<",\"witness\":[";for(int s=0;s<3;s++){if(s)cout<<",";cout<<"[";for(int r=0;r<n;r++){if(r)cout<<",";cout<<"[";for(int c=0;c<n;c++){if(c)cout<<",";cout<<mats[s][r][c];}cout<<"]";}cout<<"]";}cout<<"]";}
  cout<<"}\n";
  return status;
 }
};
int main(int argc,char**argv){int n=argc>1?atoi(argv[1]):10;double sec=argc>2?atof(argv[2]):5;long long budget=argc>3?atoll(argv[3]):10000000;
 vector<int> Bfixed(n,-1), Cfixed(n,-1);
 if(argc>4){istringstream bs(argv[4]);string v;int i=0;while(getline(bs,v,',')){if(i>=n)abort();Bfixed[i++]=stoi(v);}if(i!=n)abort();}
 if(argc>5){istringstream cs(argv[5]);string v;int i=0;while(getline(cs,v,',')){if(i>=n)abort();Cfixed[i++]=stoi(v);}if(i!=n)abort();}
DLX solver(n);for(int r=0;r<n;r++)for(int c=0;c<n;c++){
 if(r==0){solver.add(r,c,c,c,c);continue;}
 for(int a=0;a<n;a++){if(a==c||(c==0&&a!=r))continue;
 for(int b=0;b<n;b++){if(b==c||b==a||(c==0&&!Bfixed.empty()&&Bfixed[r]>=0&&b!=Bfixed[r]))continue;
 for(int d=0;d<n;d++){if(d==c||d==a||d==b||(c==0&&!Cfixed.empty()&&Cfixed[r]>=0&&d!=Cfixed[r]))continue;solver.add(r,c,a,b,d);}}
 }
 }
 if(argc>6 && string(argv[6])!="-")solver.load_psd(argv[6]);
 solver.select_forced_roots();
 solver.solve(sec,budget);
}
