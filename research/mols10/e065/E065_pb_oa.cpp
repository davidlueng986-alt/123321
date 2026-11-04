// E065 PB-5D: complete OA(n^2,5,n,2) encoding with 0-1 cell-placement variables
// and 10n^2 exact-one pseudo-Boolean constraints (native libz3).
// Compile: g++ -std=c++17 -O2 E065_pb_oa.cpp -o E065_pb_oa -l:libz3.so.4
// Each SAT model independently verifies all Latin rows, columns, and pair overlays.
// UNSAT is an SMT solver result only, NOT external LRAT certificate.
#include <bits/stdc++.h>
using namespace std;
extern "C" {
 typedef void *Z3_config,*Z3_context,*Z3_solver,*Z3_ast,*Z3_sort,*Z3_symbol,*Z3_params,*Z3_model;
 Z3_config Z3_mk_config();void Z3_del_config(Z3_config);
 Z3_context Z3_mk_context(Z3_config);void Z3_del_context(Z3_context);
 Z3_solver Z3_mk_solver(Z3_context);void Z3_solver_inc_ref(Z3_context,Z3_solver);void Z3_solver_dec_ref(Z3_context,Z3_solver);
 Z3_sort Z3_mk_bool_sort(Z3_context);Z3_ast Z3_mk_fresh_const(Z3_context,const char*,Z3_sort);
 Z3_ast Z3_mk_pbeq(Z3_context,unsigned,Z3_ast const*,int const*,int);
 void Z3_solver_assert(Z3_context,Z3_solver,Z3_ast);
 int Z3_solver_check(Z3_context,Z3_solver);int Z3_solver_check_assumptions(Z3_context,Z3_solver,unsigned,Z3_ast const*);
 Z3_params Z3_mk_params(Z3_context);void Z3_params_inc_ref(Z3_context,Z3_params);void Z3_params_dec_ref(Z3_context,Z3_params);
 Z3_symbol Z3_mk_string_symbol(Z3_context,const char*);void Z3_params_set_uint(Z3_context,Z3_params,Z3_symbol,unsigned);
 void Z3_solver_set_params(Z3_context,Z3_solver,Z3_params);
 Z3_model Z3_solver_get_model(Z3_context,Z3_solver);void Z3_model_inc_ref(Z3_context,Z3_model);void Z3_model_dec_ref(Z3_context,Z3_model);
 bool Z3_model_eval(Z3_context,Z3_model,Z3_ast,bool,Z3_ast*);int Z3_get_bool_value(Z3_context,Z3_ast);
 const char* Z3_solver_get_reason_unknown(Z3_context,Z3_solver);
}
struct Timer{chrono::steady_clock::time_point start=chrono::steady_clock::now();double sec() const{return chrono::duration<double>(chrono::steady_clock::now()-start).count();}};
struct Placement{int r,c,a,b,d;};
void independentVerify(const vector<vector<vector<int>>>& W,int n){
 vector<int> target(n);iota(target.begin(),target.end(),0);
 for(int s=0;s<3;s++){
  for(int r=0;r<n;r++){auto row=W[s][r];sort(row.begin(),row.end());if(row!=target)throw runtime_error("nonlatin row");}
  for(int c=0;c<n;c++){vector<int> col;for(int r=0;r<n;r++)col.push_back(W[s][r][c]);sort(col.begin(),col.end());if(col!=target)throw runtime_error("nonlatin col");}
 }
 int U[]={0,0,1},V[]={1,2,2};for(int p=0;p<3;p++){
  set<pair<int,int>> e;for(int r=0;r<n;r++)for(int c=0;c<n;c++)e.insert({W[U[p]][r][c],W[V[p]][r][c]});
  if((int)e.size()!=n*n)throw runtime_error("bad overlay");
 }
}
vector<int> extract(const string& line,const string& name){
 string key="\""+name+"\"";auto p=line.find(key);if(p==string::npos)throw runtime_error("missing key: "+name);
 p=line.find('[',p);auto q=line.find(']',p);string s=line.substr(p+1,q-p-1);replace(s.begin(),s.end(),',',' ');
 vector<int> a;istringstream in(s);int t;while(in>>t)a.push_back(t);return a;
}
int main(int argc,char** argv){
 if(argc<5){cerr<<"usage ./E065_pb_oa n seconds_per_branch reps.jsonl|- count [start=0] [log.jsonl]\n";return 2;}
 int n=stoi(argv[1]),timeout=stoi(argv[2]),count=stoi(argv[4]),start=argc>5?stoi(argv[5]):0;
 string reps=argv[3],logpath=argc>6?argv[6]:"E065_pb_log.jsonl";
 Timer timer;const int NN=n*n,resources=10*NN;
 vector<Placement> cand;vector<vector<int>> covers(resources);
 unordered_map<int,int> lookup;lookup.reserve(n*n*n);
 auto encode=[&](int r,int c,int a,int b,int d){return (((r*n+c)*n+a)*n+b)*n+d;};
 for(int r=0;r<n;r++)for(int c=0;c<n;c++)for(int a=0;a<n;a++){
  if(r==0 && a!=c)continue;
  if(r>0 && (a==c || (c==0 && a!=r)))continue;
  for(int b=0;b<n;b++){
   if(r==0 && b!=c)continue;
   if(r>0 && (b==c || b==a))continue;
   for(int d=0;d<n;d++){
    if(r==0 && d!=c)continue;
    if(r>0 && (d==c || d==a || d==b))continue;
    int id=cand.size();cand.push_back({r,c,a,b,d});lookup[encode(r,c,a,b,d)]=id;
    int ids[]={r*n+c,NN+r*n+a,2*NN+c*n+a,3*NN+r*n+b,4*NN+c*n+b,5*NN+r*n+d,6*NN+c*n+d,7*NN+a*n+b,8*NN+a*n+d,9*NN+b*n+d};
    for(int z:ids)covers[z].push_back(id);
   }
  }
 }
 auto config=Z3_mk_config();auto ctx=Z3_mk_context(config);Z3_del_config(config);
 auto s=Z3_mk_solver(ctx);Z3_solver_inc_ref(ctx,s);auto sort=Z3_mk_bool_sort(ctx);
 vector<Z3_ast> X(cand.size());for(auto& x:X)x=Z3_mk_fresh_const(ctx,"cell",sort);
 int empty=0;for(auto& slots:covers){if(slots.empty()){empty++;continue;}vector<Z3_ast> args;args.reserve(slots.size());vector<int> coeffs(slots.size(),1);
   for(auto id:slots)args.push_back(X[id]);
   Z3_solver_assert(ctx,s,Z3_mk_pbeq(ctx,args.size(),args.data(),coeffs.data(),1));
 }
 Z3_params params=Z3_mk_params(ctx);Z3_params_inc_ref(ctx,params);
 Z3_params_set_uint(ctx,params,Z3_mk_string_symbol(ctx,"timeout"),timeout*1000);
 Z3_solver_set_params(ctx,s,params);Z3_params_dec_ref(ctx,params);
 cerr<<"E065 PB BUILT: n="<<n<<" placements="<<cand.size()<<" equations="<<resources<<" empty_resources="<<empty<<" compile_seconds="<<timer.sec()<<"\n";
 if(empty)throw runtime_error("Model has empty exact-cover resource -- trivially UNSAT, check constraints");
 vector<vector<int>> Bs,Cs;
 if(reps=="-"){Bs.push_back({});Cs.push_back({});}
 else{ifstream in(reps);if(!in)throw runtime_error("no reps");string line;while(getline(in,line)){if(line.empty())continue;
  auto b=extract(line,"B_col0"),c=extract(line,"C_col0");if((int)b.size()!=n||(int)c.size()!=n)throw runtime_error("wrong rep length");Bs.push_back(move(b));Cs.push_back(move(c));}}
 if(start<0||start>=(int)Bs.size())throw runtime_error("start out of range");
 ofstream log(logpath,ios::app);if(!log)throw runtime_error("cannot write log");int SAT=0,UNSAT=0,UNK=0;
 for(int bi=start;bi<min((int)Bs.size(),start+count);bi++){
  vector<Z3_ast> assumptions;
  if(!Bs[bi].empty())for(int r=1;r<n;r++){
    auto it=lookup.find(encode(r,0,r,Bs[bi][r],Cs[bi][r]));if(it==lookup.end())throw runtime_error("invalid canonical firstcolumn pair");
    assumptions.push_back(X[it->second]);
  }
  double t=timer.sec();int result=assumptions.empty()?Z3_solver_check(ctx,s):Z3_solver_check_assumptions(ctx,s,assumptions.size(),assumptions.data());double took=timer.sec()-t;
  string status=result==1?"SAT":result==-1?"UNSAT":"UNKNOWN";
  if(result==1)SAT++;else if(result==-1)UNSAT++;else UNK++;
  ostringstream o;o<<"{\"n\":"<<n<<",\"branch\":"<<bi<<",\"status\":\""<<status<<"\",\"seconds\":"<<setprecision(6)<<took<<",\"assumptions\":"<<assumptions.size()<<",\"placements\":"<<cand.size();
  if(result==0)o<<",\"reason\":\""<<Z3_solver_get_reason_unknown(ctx,s)<<"\"";
  if(result==1){auto model=Z3_solver_get_model(ctx,s);Z3_model_inc_ref(ctx,model);
    vector<vector<vector<int>>> W(3,vector<vector<int>>(n,vector<int>(n,-1)));
    int chosen=0;for(int i=0;i<(int)cand.size();i++){Z3_ast val=nullptr;if(!Z3_model_eval(ctx,model,X[i],true,&val))throw runtime_error("model eval");
     if(Z3_get_bool_value(ctx,val)==1){chosen++;auto p=cand[i];W[0][p.r][p.c]=p.a;W[1][p.r][p.c]=p.b;W[2][p.r][p.c]=p.d;}}
    if(chosen!=NN)throw runtime_error("wrong selected placements");independentVerify(W,n);
    Z3_model_dec_ref(ctx,model);o<<",\"verified\":\"INDEPENDENT_"<<NN<<"_"<<NN<<"_"<<NN<<"\",\"witness\":[";
    for(int i=0;i<3;i++){if(i)o<<',';o<<'[';for(int r=0;r<n;r++){if(r)o<<',';o<<'[';for(int c=0;c<n;c++){if(c)o<<',';o<<W[i][r][c];}o<<']';}o<<']';}o<<']';
  }
  o<<"}";cout<<o.str()<<"\n"<<flush;log<<o.str()<<"\n"<<flush;
  if(result==1)break;
 }
 cerr<<"E065 PB SUMMARY SAT="<<SAT<<" UNSAT="<<UNSAT<<" UNKNOWN="<<UNK<<" total_s="<<timer.sec()<<"\n";
 Z3_solver_dec_ref(ctx,s);Z3_del_context(ctx);
}