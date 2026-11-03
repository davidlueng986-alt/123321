#!/usr/bin/env python3
"""Construct single orthogonal mate A to specified complete order-10 Latin square C, exact 4D OA encoding.
If SAT, independently verify Latin square A and 100/100 overlay; then compute common transversals for A,C.
This is not a complete 3-MOLS10 solver.
"""
import ctypes as Z,json,collections,time,sys
from pathlib import Path
D=Path(__file__).parent
qq=json.load(open(D/'C7_all_complete.json'))['C_completions'];idx=int(sys.argv[1]);seconds=int(sys.argv[2]) if len(sys.argv)>2 else 10;Q=qq[idx]
P=Z.c_void_p; U=Z.c_uint; I=Z.c_int
lib=Z.CDLL('libz3.so.4')
def mk(k,ret,args):
 f=getattr(lib,'Z3_'+k);f.restype=ret;f.argtypes=args;return f
cfg=mk('mk_config',P,[])();ctx=mk('mk_context',P,[P])(cfg);mk('del_config',None,[P])(cfg)
solver=mk('mk_solver',P,[P])(ctx);mk('solver_inc_ref',None,[P,P])(ctx,solver)
params=mk('mk_params',P,[P])(ctx);mk('params_inc_ref',None,[P,P])(ctx,params)
sym=mk('mk_string_symbol',P,[P,Z.c_char_p]);mk('params_set_uint',None,[P,P,P,U])(ctx,params,sym(ctx,b'timeout'),seconds*1000)
mk('solver_set_params',None,[P,P,P])(ctx,solver,params)
bs=mk('mk_bool_sort',P,[P])(ctx);newvar=mk('mk_fresh_const',P,[P,Z.c_char_p,P]);
assertf=mk('solver_assert',None,[P,P,P]);atmost=mk('mk_atmost',P,[P,U,Z.POINTER(P),U]);atleast=mk('mk_atleast',P,[P,U,Z.POINTER(P),U]);
check=mk('solver_check',I,[P,P]);model=mk('solver_get_model',P,[P,P]);modelinc=mk('model_inc_ref',None,[P,P]);eval=mk('model_eval',Z.c_bool,[P,P,P,Z.c_bool,Z.POINTER(P)]);boolval=mk('get_bool_value',I,[P,P]);
res=collections.defaultdict(list);placements=[];n=10
for r in range(n):
 for c in range(n):
  opts=[c] if r==0 else [a for a in range(n) if a!=c and a!=Q[r][c]]
  for a in opts:
   j=len(placements);placements.append((r,c,a))
   for k in [('X',r,c),('R',r,a),('C',c,a),('P',Q[r][c],a)]:res[k].append(j)
assert len(res)==400
vars=[newvar(ctx,b'x',bs) for _ in placements]
t0=time.monotonic()
for ids in res.values():
 ar=(P*len(ids))(*(vars[k] for k in ids));assertf(ctx,solver,atmost(ctx,len(ids),ar,1));assertf(ctx,solver,atleast(ctx,len(ids),ar,1))
v=check(ctx,solver);out={'index':idx,'status':{1:'SAT',0:'UNKNOWN',-1:'UNSAT'}[v],'seconds':round(time.monotonic()-t0,3),'variables':len(placements),'constraints':len(res)}
if v==1:
 m=model(ctx,solver);modelinc(ctx,m);A=[[-1]*n for _ in range(n)]
 for j,z in enumerate(vars):
  q=P();assert eval(ctx,m,z,True,Z.byref(q))
  if boolval(ctx,q)==1:
   r,c,a=placements[j];assert A[r][c]==-1;A[r][c]=a
 assert all(sorted(row)==list(range(n)) for row in A)
 assert all(sorted(A[r][c] for r in range(n))==list(range(n)) for c in range(n))
 assert len({(A[r][c],Q[r][c]) for r in range(n) for c in range(n)})==100
 out['A']=A;out['Q']=Q;out['validated']='10 Latin rows;10 Latin cols;100 distinct pairs'
(D/f'E063_C{idx}_single_mate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ('A','Q')}),flush=True)