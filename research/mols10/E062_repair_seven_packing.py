#!/usr/bin/env python3
"""Goal-backward: keep seven *specific* disjoint common transversals of Egan's
A, search for different orthogonal mates B satisfying the seven C-class/B-symbol
constraints. Exact 470-row 1000-variable 0-1 covering MILP (plus exclusions).
Even if all tested B fail, that is a local construction attempt only.
"""
from pathlib import Path
import json,time,random,sys,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix,vstack,csr_matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from E061_transversal_route import common_transversals,maxpack,verify_pair
D=Path(__file__).resolve().parent
S=json.load(open(D/'E061_near_triple.json'))['squares'];A,oldB=S[:2];n=10
tr,nd=common_transversals(A,oldB);pack=maxpack(tr,n);assert len(pack)==7
T=[tr[i] for i in pack];C=[[-1]*n for _ in range(n)]
for t,V in enumerate(T):
 for r,c in enumerate(V):assert C[r][c]==-1;C[r][c]=t
assert all(sum(v>=0 for v in row)==7 for row in C)
# 100 cell + 100 B row + 100 B col +100 AB + 70 C7/B
rr=[];cc=[];vals=[];choices=[]
for r in range(n):
 for c in range(n):
  for b in range(n):
   ix=len(choices);choices.append((r,c,b))
   cols=[r*10+c,100+r*10+b,200+c*10+b,300+A[r][c]*10+b]
   if C[r][c]>=0:cols.append(400+C[r][c]*10+b)
   for k in cols:rr.append(k);cc.append(ix)
M=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(470,1000)).tocsr()
assert np.array_equal(np.unique(M.sum(axis=0)),[4,5]);assert np.all(np.asarray(M.sum(axis=1))>=1)
# initial Egan solution exact constraints
xold=np.array([1 if oldB[r][c]==b else 0 for r,c,b in choices]);assert np.all(M@xold==1)
excluded=[xold];results=[];t0=time.monotonic()
for seed in range(3):
 cutoff=4
 rng=np.random.default_rng(20261103+seed)
 obj=rng.uniform(-.2,.2,size=1000)
 # Each found solution excluded by <=99 of its exact original cells;
 # it may differ in as few as 4 Latin cells, which is allowed.
 E=csr_matrix(np.array(excluded))
 F=vstack([M,E]).tocsr()
 lo=np.r_[np.ones(470),np.zeros(len(excluded))]
 hi=np.r_[np.ones(470),np.ones(len(excluded))*99]
 tic=time.monotonic()
 ub=np.ones(1000)
 for j,(r,c,b) in enumerate(choices):
  if r==0 and b!=oldB[0][c]:ub[j]=0
 z=milp(obj,integrality=np.ones(1000),bounds=Bounds(0,ub),constraints=LinearConstraint(F,lo,hi),options={'time_limit':cutoff,'mip_rel_gap':0,'presolve':True,'disp':False})
 item={'seed':seed,'solver_status_code':int(z.status),'status':{0:'SAT',1:'UNKNOWN_BUDGET',2:'UNSAT_EXHAUSTIVE',3:'UNBOUNDED',4:'ERROR'}.get(z.status,'ERROR'),'seconds':round(time.monotonic()-tic,2)}
 if z.x is not None:
  arr=(z.x>.5).astype(int)
  if arr.sum()==100 and np.all(M@arr==1):
   B=[[-1]*n for _ in range(n)]
   for (r,c,b),v in zip(choices,arr):
    if v:B[r][c]=b
   verify_pair(A,B)
   for Tt in T:assert {B[r][Tt[r]] for r in range(n)}==set(range(n))
   new_tr,new_nd=common_transversals(A,B);new_pack=maxpack(new_tr,n)
   item.update({'status':'SAT','changed_cells':int(sum(B[r][c]!=oldB[r][c] for r in range(n) for c in range(n))),'new_total_common_transversals':len(new_tr),'max_disjoint':len(new_pack),'newB':B,'new_transversal_indices':new_pack})
   results.append(item);excluded.append(arr);print('SAT_PAIR',json.dumps({k:v for k,v in item.items() if k not in ['newB','new_transversal_indices']}),flush=True)
   if len(new_pack)>=9:
    from E061_transversal_route import close_pair
    ovs,Cw=close_pair(A,B,[new_tr[i] for i in new_pack[:9]])
    item['full_witness']=[A,B,Cw];item['overlays']=ovs
    print('CLOSED_100_100_100',json.dumps(item),flush=True)
    break
   if len(new_pack)>=8:
    from E061_two_transversal_completion import residual_graph
    q=residual_graph(A,B,[new_tr[i] for i in new_pack[:8]])
    if q['bipartite']:
     from E061_transversal_route import close_pair
     ovs,Cw=close_pair(A,B,[new_tr[i] for i in new_pack[:8]]+[q['new_common_transversal']]);item['full_witness']=[A,B,Cw];item['overlays']=ovs
     print('CLOSED_100_100_100',json.dumps(item),flush=True)
     break
   continue
 print('TRY',json.dumps(item),flush=True)
 results.append(item)
 if z.status==2:break
summary={'scope':'fixed Egan A and 7 Egan common transversals, variable B; not global','fixedA':A,'fixed_seven_transversals':T,'model_binary_variables':1000,'model_exact_constraints':470,'samples':results,'seconds':round(time.monotonic()-t0,2),'global_status':'CLOSED' if any('full_witness' in q for q in results) else 'OPEN'}
(D/'E062_REPAIR_7_PACK_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n');print('FINAL',json.dumps({'trials':len(results),'SAT':sum(x['status']=='SAT' for x in results),'UNKNOWN':sum(x['status']=='UNKNOWN_BUDGET' for x in results),'max_pack':max((x.get('max_disjoint',7) for x in results),default=7),'status':summary['global_status'],'seconds':summary['seconds']}),flush=True)