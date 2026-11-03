#!/usr/bin/env python3
"""Search FULL OA(100,5,10,2) with seven known C-class cell sets.
A, B both free; normalize all three first rows to identity. This is an exact
model of that particular C pattern but not an unrestricted MOLS10 search.
Independent Latin/overlay verifier on every SAT return.
"""
import ctypes as T,collections,json,sys,time,os
from pathlib import Path
DIR=Path(__file__).parent
z=json.loads((DIR/'C7_all_complete.json').read_text()); CF=z['Cfixed'] if len(sys.argv)<=2 else z['C_completions'][int(sys.argv[2])]
P=T.c_void_p; U=T.c_uint; I=T.c_int
lib=T.CDLL('libz3.so.4')
def F(name, restype, argtypes):
 z=getattr(lib,'Z3_'+name);z.restype=restype;z.argtypes=argtypes;return z
mkconfig=F('mk_config',P,[]);ctxmaker=F('mk_context',P,[P]);delconfig=F('del_config',None,[P]);delctx=F('del_context',None,[P]);
mk_solver=F('mk_solver',P,[P]);solver_inc_ref=F('solver_inc_ref',None,[P,P]);solver_dec_ref=F('solver_dec_ref',None,[P,P]);
mk_params=F('mk_params',P,[P]);params_inc=F('params_inc_ref',None,[P,P]);params_dec=F('params_dec_ref',None,[P,P]);
mk_string=F('mk_string_symbol',P,[P,T.c_char_p]);set_param=F('params_set_uint',None,[P,P,P,U]);solver_params=F('solver_set_params',None,[P,P,P]);
mk_bool=F('mk_bool_sort',P,[P]);mk_fresh=F('mk_fresh_const',P,[P,T.c_char_p,P]);mk_atmost=F('mk_atmost',P,[P,U,T.POINTER(P),U]);mk_atleast=F('mk_atleast',P,[P,U,T.POINTER(P),U]);assertf=F('solver_assert',None,[P,P,P]);check=F('solver_check',I,[P,P]);reason=F('solver_get_reason_unknown',T.c_char_p,[P,P]);
get_model=F('solver_get_model',P,[P,P]);model_inc=F('model_inc_ref',None,[P,P]);model_dec=F('model_dec_ref',None,[P,P]);model_eval=F('model_eval',T.c_bool,[P,P,P,T.c_bool,T.POINTER(P)]);get_bool=F('get_bool_value',I,[P,P]);
n=10
R=collections.defaultdict(list);placements=[]
for r in range(n):
 for c in range(n):
  opts=[(c,c,c)] if r==0 else [(a,b,d) for a in range(n) if a!=c for b in range(n) if b!=c and b!=a for d in range(n) if d!=c and d!=a and d!=b and (CF[r][c]==-1 or d==CF[r][c])]
  for a,b,d in opts:
   i=len(placements);placements.append((r,c,a,b,d));
   keys=[('X',r,c)]+[('R',s,r,v) for s,v in enumerate((a,b,d))]+[('C',s,c,v) for s,v in enumerate((a,b,d))]+[('P',0,a,b),('P',1,a,d),('P',2,b,d)]
   for key in keys:R[key].append(i)
assert len(R)==10*n*n,(len(R),len(placements))
for key,ids in R.items():
 if not ids:
  print('ZERO_SUPPORT',key);sys.exit(0)
t0=time.monotonic(); config=mkconfig();ctx=ctxmaker(config);delconfig(config)
solver=mk_solver(ctx);solver_inc_ref(ctx,solver)
params=mk_params(ctx);params_inc(ctx,params);timeout_ms=int(sys.argv[1])*1000 if len(sys.argv)>1 else 30000
set_param(ctx,params,mk_string(ctx,b'timeout'),timeout_ms);solver_params(ctx,solver,params)
bsort=mk_bool(ctx);vars=[mk_fresh(ctx,b'v',bsort) for _ in placements]
for ix,ids in enumerate(R.values()):
 a=(P*len(ids))(*(vars[j] for j in ids));assertf(ctx,solver,mk_atmost(ctx,len(ids),a,1));assertf(ctx,solver,mk_atleast(ctx,len(ids),a,1))
 if ix%100==0:print('SETUP',ix,len(R),'vars',len(vars),'sec',round(time.monotonic()-t0,2),flush=True)
print('SEARCH',json.dumps({'vars':len(vars),'constraints':len(R),'incidences':sum(map(len,R.values())),'setup_sec':round(time.monotonic()-t0,2),'z3_timeout_sec':timeout_ms/1000}),flush=True)
z=check(ctx,solver);out={'status':{1:'SAT',0:'UNKNOWN',-1:'UNSAT'}[z],'c_fixed':sum(v>=0 for row in CF for v in row),'vars':len(vars),'constraints':len(R),'seconds':round(time.monotonic()-t0,2)}
if z==0:out['reason']=reason(ctx,solver).decode(errors='replace')
if z==1:
 model=get_model(ctx,solver);model_inc(ctx,model);Sq=[[[-1]*n for r in range(n)] for s in range(3)];selected=0
 for i,v in enumerate(vars):
  q=P();assert model_eval(ctx,model,v,True,T.byref(q));
  if get_bool(ctx,q)==1:
   r,c,a,b,d=placements[i];selected+=1
   for s,t in enumerate((a,b,d)):
    assert Sq[s][r][c]==-1;Sq[s][r][c]=t
 assert selected==100
 for s in range(3):
  assert all(sorted(row)==list(range(n)) for row in Sq[s])
  assert all(sorted(Sq[s][r][c] for r in range(n))==list(range(n)) for c in range(n))
 for a,b in [(0,1),(0,2),(1,2)]:
  assert len({(Sq[a][r][c],Sq[b][r][c]) for r in range(n) for c in range(n)})==100
 out['witness']=Sq;out['validation']='100/100/100'
 model_dec(ctx,model)
(DIR/('E063_z3_7C_results.json' if len(sys.argv)<=2 else f'E063_z3_C{sys.argv[2]}_results.json')).write_text(json.dumps(out,indent=2)+'\n')
print('RESULT',json.dumps({k:v for k,v in out.items() if k!='witness'}),flush=True)
solver_dec_ref(ctx,solver);params_dec(ctx,params);delctx(ctx)