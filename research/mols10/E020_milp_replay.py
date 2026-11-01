#!/usr/bin/env python3
"""Independent SciPy/HiGHS exact-cover replay of E020 selected roots.
Requires scipy, numpy; not needed for stdlib CI. Solver status 2 is
complete infeasibility; status 1 is UNKNOWN, never UNSAT.
"""
import argparse,json,time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
from E020_unary_exact_cover import PARKER_A

def independent_transversals(a):
 import itertools
 n=len(a)
 return [sum(1<<(n*r+p[r]) for r in range(n))
  for p in itertools.permutations(range(n))
  if len({a[r][p[r]] for r in range(n)})==n]

def solve(root,seconds=8):
 a=PARKER_A;n=len(a);T=independent_transversals(a)
 allowed=[k for k,v in enumerate(T) if (v&T[root]).bit_count()==1]
 rows=[];cols=[]
 for j,k in enumerate(allowed):
  for c in range(n*n):
   if T[k]>>c&1:rows.append(c);cols.append(j)
 mat=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(n*n,len(allowed))).tocsr()
 start=time.monotonic()
 res=milp(np.zeros(len(allowed)),integrality=np.ones(len(allowed)),
  bounds=Bounds(0,1),constraints=LinearConstraint(mat,1,1),
  options={'time_limit':seconds})
 out=dict(root=root,allowed=len(allowed),solver_status=int(res.status),
  interpretation={0:'SAT',1:'UNKNOWN_BUDGET',2:'UNSAT_FIXED_ROOT',3:'UNBOUNDED',4:'SOLVER_ERROR'}.get(int(res.status)),
  seconds=round(time.monotonic()-start,3),message=str(res.message))
 if res.x is not None:
  ids=[allowed[j] for j,x in enumerate(res.x) if x>.5]
  out['independent_replay']=len(ids)==n and all(
   sum((T[k]>>c)&1 for k in ids)==1 for c in range(n*n)) and all(
   (T[k]&T[root]).bit_count()==1 for k in ids)
  out['selected_ids']=ids
 print(json.dumps(out,indent=2))
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--roots',default='0,26,109')
 p.add_argument('--seconds',type=float,default=8)
 args=p.parse_args()
 for i in map(int,args.roots.split(',')):solve(i,args.seconds)
