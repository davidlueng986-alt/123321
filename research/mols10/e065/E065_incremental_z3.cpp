// E065 direct complete 3-MOLS(n) CNF via native Z3 C API.
// No external pip package or z3.h required. Compile:
// g++ -std=c++17 -O2 E065_incremental_z3.cpp -o E065_incremental_z3 -l:libz3.so.4
// The SAT/UNSAT is Z3's answer, NOT an LRAT or independently verified UNSAT
// certificate. On SAT reconstruct and independently verify full 100/100/100.
#include <bits/stdc++.h>
using namespace std;
extern "C" {
  typedef void *Z3_config,*Z3_context,*Z3_solver,*Z3_ast,*Z3_sort,*Z3_symbol,*Z3_params,*Z3_model;
  Z3_config Z3_mk_config();void Z3_del_config(Z3_config);
  Z3_context Z3_mk_context(Z3_config);void Z3_del_context(Z3_context);
  Z3_solver Z3_mk_solver(Z3_context);void Z3_solver_inc_ref(Z3_context,Z3_solver);void Z3_solver_dec_ref(Z3_context,Z3_solver);
  Z3_sort Z3_mk_bool_sort(Z3_context);Z3_ast Z3_mk_fresh_const(Z3_context,const char*,Z3_sort);
  Z3_ast Z3_mk_not(Z3_context,Z3_ast);Z3_ast Z3_mk_or(Z3_context,unsigned,Z3_ast const*);
  void Z3_solver_assert(Z3_context,Z3_solver,Z3_ast);
  int Z3_solver_check(Z3_context,Z3_solver);int Z3_solver_check_assumptions(Z3_context,Z3_solver,unsigned,Z3_ast const*);
  Z3_params Z3_mk_params(Z3_context);void Z3_params_inc_ref(Z3_context,Z3_params);void Z3_params_dec_ref(Z3_context,Z3_params);
  Z3_symbol Z3_mk_string_symbol(Z3_context,const char*);void Z3_params_set_uint(Z3_context,Z3_params,Z3_symbol,unsigned);
  void Z3_solver_set_params(Z3_context,Z3_solver,Z3_params);
  Z3_model Z3_solver_get_model(Z3_context,Z3_solver);void Z3_model_inc_ref(Z3_context,Z3_model);void Z3_model_dec_ref(Z3_context,Z3_model);
  bool Z3_model_eval(Z3_context,Z3_model,Z3_ast,bool,Z3_ast*);int Z3_get_bool_value(Z3_context,Z3_ast);
  const char* Z3_solver_get_reason_unknown(Z3_context,Z3_solver);
}
struct Clock{chrono::steady_clock::time_point start=chrono::steady_clock::now();double sec() const{return chrono::duration<double>(chrono::steady_clock::now()-start).count();}};
int vid(int n,int s,int r,int c,int v){return 1+(((s*n+r)*n+c)*n+v);} // E065_cnf.py x mapping
vector<array<array<int,10>,10>> decode(Z3_context c,Z3_solver sl,vector<Z3_ast>& xs,int n){
  auto m=Z3_solver_get_model(c,sl);if(!m)throw runtime_error("Z3 returned SAT without model");Z3_model_inc_ref(c,m);
  vector<array<array<int,10>,10>> W(3);
  for(int s=0;s<3;s++)for(int r=0;r<n;r++)for(int col=0;col<n;col++){
    int count=0,value=-1;
    for(int v=0;v<n;v++){
      Z3_ast z=nullptr;if(!Z3_model_eval(c,m,xs[vid(n,s,r,col,v)],true,&z))throw runtime_error("Z3 model eval failed");
      if(Z3_get_bool_value(c,z)==1){count++;value=v;}
    }
    if(count!=1)throw runtime_error("Z3 model not onehot");W[s][r][col]=value;
  }
  Z3_model_dec_ref(c,m);return W;
}
void independently_verify(const vector<array<array<int,10>,10>>& W,int n){
 auto check=[](bool b,const char* msg){if(!b)throw runtime_error(msg);};
 vector<int> target(n);iota(target.begin(),target.end(),0);
 for(int s=0;s<3;s++){
  for(int r=0;r<n;r++){vector<int> z;for(int c=0;c<n;c++)z.push_back(W[s][r][c]);sort(z.begin(),z.end());check(z==target,"non Latin row");}
  for(int c=0;c<n;c++){vector<int> z;for(int r=0;r<n;r++)z.push_back(W[s][r][c]);sort(z.begin(),z.end());check(z==target,"non Latin column");}
 }
 int I[3]={0,0,1},J[3]={1,2,2};
 for(int p=0;p<3;p++){
   set<pair<int,int>> S;
   for(int r=0;r<n;r++)for(int c=0;c<n;c++)S.insert({W[I[p]][r][c],W[J[p]][r][c]});
   check((int)S.size()==n*n,"orthogonality failure");
 }
}
void show_witness(const vector<array<array<int,10>,10>>& W,int n){
 cout<<",\"witness\":[";for(int s=0;s<3;s++){if(s)cout<<',';cout<<'[';
 for(int r=0;r<n;r++){if(r)cout<<',';cout<<'[';for(int c=0;c<n;c++){if(c)cout<<',';cout<<W[s][r][c];}cout<<']';}cout<<']';}cout<<']';
}
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: ./E065_incremental_z3 dimacs.cnf n seconds_per_branch branch_reps.jsonl|- [max_count=5] [start=0] [out.jsonl]\n";return 2;}
 string path=argv[1];int n=stoi(argv[2]),seconds=stoi(argv[3]),maxcount=argc>5?stoi(argv[5]):5,start=argc>6?stoi(argv[6]):0;
 string repath=argv[4],logpath=argc>7?argv[7]:"E065_solver_results.jsonl";
 Clock clock;ifstream src(path);if(!src)throw runtime_error("No CNF: "+path);
 string line;int vars=0,clauses=0,asserted=0;vector<vector<int>> constraints;
 while(getline(src,line)){
  if(line.empty()||line[0]=='c')continue;
  if(line[0]=='p'){istringstream t(line);string a,b;t>>a>>b>>vars>>clauses;constraints.reserve(clauses);continue;}
  istringstream ss(line);vector<int> cl;int k;while(ss>>k){if(k==0)break;cl.push_back(k);} if(!cl.empty())constraints.push_back(move(cl));
 }
 if((int)constraints.size()!=clauses||vars!=3*n*n*n+3*n*n*n*n)throw runtime_error("CNF header mismatch");
 auto cfg=Z3_mk_config();auto ctx=Z3_mk_context(cfg);Z3_del_config(cfg);
 auto solver=Z3_mk_solver(ctx);Z3_solver_inc_ref(ctx,solver);auto sort=Z3_mk_bool_sort(ctx);
 vector<Z3_ast> pos(vars+1),neg(vars+1);
 for(int i=1;i<=vars;i++)pos[i]=Z3_mk_fresh_const(ctx,"e065",sort);
 for(int i=1;i<=vars;i++)neg[i]=Z3_mk_not(ctx,pos[i]);
 for(const auto& cl:constraints){vector<Z3_ast> args;args.reserve(cl.size());for(int k:cl)args.push_back(k>0?pos[k]:neg[-k]);Z3_solver_assert(ctx,solver,cl.size()==1?args[0]:Z3_mk_or(ctx,args.size(),args.data()));asserted++;}
 constraints.clear();constraints.shrink_to_fit();
 auto params=Z3_mk_params(ctx);Z3_params_inc_ref(ctx,params);
 Z3_params_set_uint(ctx,params,Z3_mk_string_symbol(ctx,"timeout"),seconds*1000);
 Z3_solver_set_params(ctx,solver,params);Z3_params_dec_ref(ctx,params);
 double construction=clock.sec();cerr<<"E065 BUILT n="<<n<<" vars="<<vars<<" clauses="<<asserted<<" time="<<construction<<"s\n";
 vector<vector<int>> brB,brC;
 if(repath=="-"){brB.push_back({});brC.push_back({});}
 else{
  // The representative file is JSONL. Avoid a third-party JSON lib.
  ifstream in(repath);if(!in)throw runtime_error("No reps file");
  auto extract=[&](const string& s,const string& key){vector<int> a;size_t p=s.find("\""+key+"\"");if(p==string::npos)throw runtime_error("missing JSON key "+key);
    p=s.find('[',p);auto q=s.find(']',p);if(q==string::npos)throw runtime_error("bad JSON array");
    string v=s.substr(p+1,q-p-1);replace(v.begin(),v.end(),',',' ');istringstream ss(v);int x;while(ss>>x)a.push_back(x);return a;};
  while(getline(in,line)){if(line.empty())continue;auto b=extract(line,"B_col0"),c=extract(line,"C_col0");if((int)b.size()!=n||(int)c.size()!=n)throw runtime_error("bad rep length");brB.push_back(move(b));brC.push_back(move(c));}
 }
 if(start<0||start>=(int)brB.size())throw runtime_error("start out of range");
 int stop=min((int)brB.size(),start+maxcount);
 ofstream log(logpath,ios::app);if(!log)throw runtime_error("Cannot write log");
 int sat=0,unsat=0,unknown=0;
 for(int i=start;i<stop;i++){
  vector<Z3_ast> assumptions;
  if(!brB[i].empty())for(int r=0;r<n;r++){
    assumptions.push_back(pos[vid(n,1,r,0,brB[i][r])]);
    assumptions.push_back(pos[vid(n,2,r,0,brC[i][r])]);
  }
  double begin=clock.sec();int result=assumptions.empty()?Z3_solver_check(ctx,solver):Z3_solver_check_assumptions(ctx,solver,assumptions.size(),assumptions.data());
  double elapsed=clock.sec()-begin;string status=result==1?"SAT":result==-1?"UNSAT":"UNKNOWN";
  string reason=result==0?Z3_solver_get_reason_unknown(ctx,solver):"";
  if(result==1)sat++;else if(result==-1)unsat++;else unknown++;
  ostringstream lineout;
  lineout<<"{\"n\":"<<n<<",\"branch\":"<<i<<",\"status\":\""<<status<<"\",\"seconds\":"<<setprecision(6)<<elapsed<<",\"assumptions\":"<<assumptions.size()<<",\"reason\":\""<<reason<<"\"";
  if(result==1){auto W=decode(ctx,solver,pos,n);independently_verify(W,n);lineout<<",\"verified\":\"INDEPENDENT_"<<n*n<<"_"<<n*n<<"_"<<n*n<<"\"";
    // Reconstruct JSON separately: avoid injecting nested strings into lineout.
    stringstream tmp;auto* saved=cout.rdbuf(tmp.rdbuf());show_witness(W,n);cout.rdbuf(saved);lineout<<tmp.str();
  }
  lineout<<"}";cout<<lineout.str()<<"\n"<<flush;log<<lineout.str()<<"\n"<<flush;
  if(result==1)break;
 }
 cerr<<"E065 SUMMARY sat="<<sat<<" unsat="<<unsat<<" unknown="<<unknown<<" construction_s="<<construction<<" total_s="<<clock.sec()<<"\n";
 Z3_solver_dec_ref(ctx,solver);Z3_del_context(ctx);
}