#!/usr/bin/env python3
"""Complete SAT query for a *different* B mate of one Egan A,
with seven common transversals preserved as cell sets. No global inference.
Pure ctypes on system libz3.so.4. Verify any SAT mate and packing independently.
"""
import ctypes as C,json,sys,time,collections,os
from pathlib import Path
from E061_transversal_route import common_transversals,maxpack,verify_pair
D=Path(__file__).parent
A,B0=json.loads((D/'E061_near_triple.json').read_text())['squares'][:2]
tr,tnodes=common_transversals(A,B0);pack=maxpack(tr,10);assert len(pack)==7
T=[tr[i] for i in pack];C7=[[-1]*10 for _ in range(10)]
for t,z in enumerate(T):
 for r,c in enumerate(z):
  assert C7[r][c]<0;C7[r][c]=t
R=collections.defaultdict(list)
for r in range(10):
 for c in range(10):
  for b in range(10):
   ix=(r*10+c)*10+b
   for k in ((0,r,c),(1,r,b),(2,c,b),(3,A[r][c],b)):
    R[k].append(ix)
   if C7[r][c]>=0:R[(4,C7[r][c],b)].append(ix)
assert len(R)==470 and all(len(x)==10 for x in R.values())
lib=C.CDLL('libz3.so.4');P=C.c_void_p;U=C.c_uint;I=C.c_int
Z=lambda name,ret,args:(lambda f:(setattr(f,'restype',ret),setattr(f,'argtypes',args),f)[-1])(getattr(lib,'Z3_'+name))
config=Z('mk_config',P,[])();ctx=Z('mk_context',P,[P])(config);Z('del_config',None,[P])(config)
sol=Z('mk_solver',P,[P])(ctx);Z('solver_inc_ref',None,[P,P])(ctx,sol)
pars=Z('mk_params',P,[P])(ctx);Z('params_inc_ref',None,[P,P])(ctx,pars)
mk_symbol=Z('mk_string_symbol',P,[P,C.c_char_p]);setparam=Z('params_set_uint',None,[P,P,P,U]);setparam(ctx,pars,mk_symbol(ctx,b'timeout'),30000)
Z('solver_set_params',None,[P,P,P])(ctx,sol,pars)
bool_sort=Z('mk_bool_sort',P,[P])(ctx)
mk_fresh=Z('mk_fresh_const',P,[P,C.c_char_p,P]);var=[mk_fresh(ctx,b'x',bool_sort) for _ in range(1000)]
mk_atmost=Z('mk_atmost',P,[P,U,C.POINTER(P),U]);mk_atleast=Z('mk_atleast',P,[P,U,C.POINTER(P),U]);mk_not=Z('mk_not',P,[P,P]);mk_or=Z('mk_or',P,[P,U,C.POINTER(P)]);assertf=Z('solver_assert',None,[P,P,P])
t0=time.monotonic()
for z in R.values():
 a=(P*len(z))(*[var[x] for x in z]);assertf(ctx,sol,mk_atmost(ctx,len(z),a,1));assertf(ctx,sol,mk_atleast(ctx,len(z),a,1))
# B first row pinned under free independent relabeling of B symbols.
for c in range(10):assertf(ctx,sol,var[c*10+B0[0][c]])
# B must differ from the known Egan mate after pinning row0.
old=[(r*10+c)*10+B0[r][c] for r in range(10) for c in range(10)]
no=(P*len(old))(*[mk_not(ctx,var[x]) for x in old]);assertf(ctx,sol,mk_or(ctx,len(old),no))
setup=time.monotonic()-t0
res=Z('solver_check',I,[P,P])(ctx,sol)
out={'solver_status':{1:'SAT',0:'UNKNOWN',-1:'UNSAT'}[res], 'setup_seconds':round(setup,3),'elapsed':round(time.monotonic()-t0,3),'scope':'FIXED Egan A and seven common-transversal cell sets; original B excluded'}
if res==1:
 m=Z('solver_get_model',P,[P,P])(ctx,sol);Z('model_inc_ref',None,[P,P])(ctx,m)
 ev=Z('model_eval',C.c_bool,[P,P,P,C.c_bool,C.POINTER(P)]);val=Z('get_bool_value',I,[P,P]);xx=[]
 for v in var:
  q=P();assert ev(ctx,m,v,True,C.byref(q));xx.append(val(ctx,q)==1)
 B=[[-1]*10 for _ in range(10)]
 for idx,v in enumerate(xx):
  if v:r=idx//100;c=(idx//10)%10;b=idx%10;assert B[r][c]==-1;B[r][c]=b
 verify_pair(A,B)
 assert all({B[r][Z[r]] for r in range(10)}==set(range(10)) for Z in T)
 ntr,nd=common_transversals(A,B);p=maxpack(ntr,10)
 out.update({'changed_cells':sum(B[r][c]!=B0[r][c] for r in range(10) for c in range(10)),'B':B,'common_transversals':len(ntr),'max_disjoint':len(p),'packing_indices':p})
 if len(p)>=9:
  from E061_transversal_route import close_pair
  ovs,C=close_pair(A,B,[ntr[i] for i in p[:9]]);out['full_verified_witness']=[A,B,C];out['overlays']=ovs
 Z('model_dec_ref',None,[P,P])(ctx,m)
(D/'E062_REPAIR_7_PACK_Z3_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('B','full_verified_witness')},indent=2),flush=True)
Z('solver_dec_ref',None,[P,P])(ctx,sol);Z('del_context',None,[P])(ctx)