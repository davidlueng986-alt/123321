// CAP-052 actual root-complete dense-H-centre Z3 SAT attempt.
// All 237-caps can be normalized to this instance by the CAP052 theorem.
// A Z3 UNKNOWN or timeout is NOT a no-237 proof. CPU-only.
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cassert>
#include <vector>
#include <chrono>
#include <fstream>
extern "C" {
typedef void* Z3_config;typedef void* Z3_context;typedef void* Z3_symbol;
typedef void* Z3_sort;typedef void* Z3_ast;typedef void* Z3_solver;
typedef void* Z3_params;typedef void* Z3_model;
Z3_config Z3_mk_config();
void Z3_set_param_value(Z3_config,const char*,const char*);
void Z3_del_config(Z3_config);
Z3_context Z3_mk_context(Z3_config);
Z3_sort Z3_mk_bool_sort(Z3_context);
Z3_symbol Z3_mk_int_symbol(Z3_context,int);
Z3_symbol Z3_mk_string_symbol(Z3_context,const char*);
Z3_ast Z3_mk_const(Z3_context,Z3_symbol,Z3_sort);
Z3_ast Z3_mk_not(Z3_context,Z3_ast);
Z3_ast Z3_mk_or(Z3_context,unsigned,Z3_ast const*);
Z3_ast Z3_mk_atleast(Z3_context,unsigned,Z3_ast const*,unsigned);
Z3_ast Z3_mk_implies(Z3_context,Z3_ast,Z3_ast);
Z3_solver Z3_mk_solver(Z3_context);
void Z3_solver_inc_ref(Z3_context,Z3_solver);
void Z3_solver_assert(Z3_context,Z3_solver,Z3_ast);
int Z3_solver_check(Z3_context,Z3_solver);
const char* Z3_solver_get_reason_unknown(Z3_context,Z3_solver);
Z3_model Z3_solver_get_model(Z3_context,Z3_solver);
bool Z3_model_eval(Z3_context,Z3_model,Z3_ast,bool,Z3_ast*);
int Z3_get_bool_value(Z3_context,Z3_ast);
Z3_params Z3_mk_params(Z3_context);
void Z3_params_inc_ref(Z3_context,Z3_params);
void Z3_params_set_uint(Z3_context,Z3_params,Z3_symbol,unsigned);
void Z3_solver_set_params(Z3_context,Z3_solver,Z3_params);
}
static constexpr int N=2187;
std::array<std::array<uint8_t,7>,N> point;
void setup(){for(int i=0;i<N;i++){int x=i;for(int j=6;j>=0;j--){point[i][j]=x%3;x/=3;}}}
int third(int i,int j){int r=0;for(int k=0;k<7;k++)r=3*r+(6-point[i][k]-point[j][k])%3;return r;}
int main(int argc,char**argv){
  int ms=argc>1?atoi(argv[1]):15000;
  setup();
  auto start=std::chrono::steady_clock::now();
  Z3_config cfg=Z3_mk_config();
  Z3_set_param_value(cfg,"model","true");
  Z3_context ctx=Z3_mk_context(cfg);Z3_del_config(cfg);
  Z3_solver slv=Z3_mk_solver(ctx);Z3_solver_inc_ref(ctx,slv);
  Z3_params opt=Z3_mk_params(ctx);Z3_params_inc_ref(ctx,opt);
  Z3_params_set_uint(ctx,opt,Z3_mk_string_symbol(ctx,"timeout"),ms);
  Z3_solver_set_params(ctx,slv,opt);
  Z3_sort bs=Z3_mk_bool_sort(ctx);
  std::array<int,N> fixed{};fixed.fill(-1);
  std::vector<int> picked{729,243,81,27,9,3,1,1458,486,162,54};
  for(int p:picked){assert(fixed[p]==-1);fixed[p]=1;}
  int zeros=0;
  for(int i=0;i<11;i++)for(int j=i+1;j<11;j++){
    int p=third(picked[i],picked[j]);
    assert(fixed[p]!=1);
    if(fixed[p]<0){fixed[p]=0;zeros++;}
  }
  assert(zeros==52 && fixed[0]==0);
  std::array<int,N> id{};id.fill(-1);
  std::vector<int> free_points,H;
  for(int i=0;i<N;i++)if(fixed[i]<0){
    id[i]=(int)free_points.size();free_points.push_back(i);
    if(i%3==0)H.push_back(i);
  }
  assert(free_points.size()==2124 && H.size()==677);
  std::vector<Z3_ast> X(free_points.size()),NX(free_points.size()),Y;
  for(size_t i=0;i<X.size();i++){
    X[i]=Z3_mk_const(ctx,Z3_mk_int_symbol(ctx,(int)i+1),bs);
    NX[i]=Z3_mk_not(ctx,X[i]);
  }
  int dropped=0,binary=0,ternary=0;
  for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){
    int k=third(i,j);if(k<=j)continue;
    if(fixed[i]==0||fixed[j]==0||fixed[k]==0){dropped++;continue;}
    Z3_ast clause[3];unsigned t=0;
    if(fixed[i]<0)clause[t++]=NX[id[i]];
    if(fixed[j]<0)clause[t++]=NX[id[j]];
    if(fixed[k]<0)clause[t++]=NX[id[k]];
    assert(t==2||t==3);
    Z3_solver_assert(ctx,slv,Z3_mk_or(ctx,t,clause));
    if(t==2)binary++;else ternary++;
  }
  assert(dropped==55554 && binary==11475 && ternary==729768);
  Z3_solver_assert(ctx,slv,Z3_mk_atleast(ctx,X.size(),X.data(),226));
  std::vector<Z3_ast> HX;
  for(int p:H)HX.push_back(X[id[p]]);
  Z3_solver_assert(ctx,slv,Z3_mk_atleast(ctx,HX.size(),HX.data(),79));
  // Four pairs +/-e1...+/-e4 already fixed. Need >=3 other pairs inside H.
  for(int p=1;p<N;p++){
    int m=third(p,0);
    if(p>m || p%3!=0)continue;
    if(fixed[p]==1 && fixed[m]==1)continue;
    if(fixed[p]==0 || fixed[m]==0)continue;
    if(fixed[p]==1 || fixed[m]==1){
      int z=fixed[p]==1?m:p;
      assert(fixed[z]==-1);
      Y.push_back(X[id[z]]);
    } else {
      int yid=5000+(int)Y.size();
      Z3_ast y=Z3_mk_const(ctx,Z3_mk_int_symbol(ctx,yid),bs);
      Z3_solver_assert(ctx,slv,Z3_mk_implies(ctx,y,X[id[p]]));
      Z3_solver_assert(ctx,slv,Z3_mk_implies(ctx,y,X[id[m]]));
      Y.push_back(y);
    }
  }
  assert(Y.size()==331);
  Z3_solver_assert(ctx,slv,Z3_mk_atleast(ctx,Y.size(),Y.data(),3));
  auto built=std::chrono::steady_clock::now();
  printf("ROOT_SINGLE dense11 selected=11 zeros=52 free=2124 Hfree=677 dropped=%d binary=%d ternary=%d additional_pair_potentials=%zu build_sec=%.3f\n",dropped,binary,ternary,Y.size(),std::chrono::duration<double>(built-start).count());
  fflush(stdout);
  int result=Z3_solver_check(ctx,slv);
  auto end=std::chrono::steady_clock::now();
  printf("SAT_STATUS %s elapsed_sec=%.3f\n",result==1?"SAT":result==-1?"UNSAT":"UNKNOWN",std::chrono::duration<double>(end-start).count());
  if(result==0)printf("UNKNOWN_REASON %s\n",Z3_solver_get_reason_unknown(ctx,slv));
  if(result==1){
    Z3_model model=Z3_solver_get_model(ctx,slv);
    std::vector<int> cap=picked;
    for(size_t i=0;i<X.size();i++){
      Z3_ast z=nullptr;
      if(Z3_model_eval(ctx,model,X[i],true,&z)&&Z3_get_bool_value(ctx,z)==1)
        cap.push_back(free_points[i]);
    }
    std::vector<char> seen(N,0);for(int p:cap)seen[p]=1;
    int bad=0;for(size_t i=0;i<cap.size();i++)for(size_t j=i+1;j<cap.size();j++)
      bad+=seen[third(cap[i],cap[j])];
    int dense=0;for(int p:cap)dense+=(p%3==0);
    printf("INDEPENDENT_CHECK size=%zu bad_triples=%d Hsize=%d\n",cap.size(),bad,dense);
    if(cap.size()>=237 && bad==0 && dense>=89){
      std::ofstream f("/mnt/data/CAPSET_237_NEW_WITNESS.txt");f<<"n: 7\n";
      for(int p:cap){for(int j=0;j<7;j++)f<<(int)point[p][j];f<<'\n';}
    }
  }
  return 0;
}
