#!/usr/bin/env python3
"""E041 all-six-class fractional exact-cover deletion audit (SciPy HiGHS).
Exploratory numerical feasibility is NOT a rational primal certificate.
Input: E040_EXACT_MINIMAL_CORES.json in this directory.
"""
import json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
Z=json.load(open('E040_EXACT_MINIMAL_CORES.json'))['results']
def resources(c,a,b,d):
 return (a*10+b,100+a*10+d,200+b*10+d,300+c*10+a,400+c*10+b,500+c*10+d)
def model(z,excluded):
 P=z['source_prefix']
 keep=set(z['forced_cell_indices'])-set(excluded)
 used=set()
 for j in keep:
  r,c=divmod(j,10);a,b,d=[P[s][r][c] for s in range(3)]
  es=resources(c,a,b,d)
  assert all(e not in used for e in es)
  used.update(es)
 un=[e for e in range(600) if e not in used]
 idx={e:i for i,e in enumerate(un)}
 rr=[];cc=[];cand=[]
 for c in range(10):
  for a in range(10):
   for b in range(10):
    for d in range(10):
     es=resources(c,a,b,d)
     if any(e in used for e in es):continue
     j=len(cand);cand.append((c,a,b,d))
     for e in es:rr.append(idx[e]);cc.append(j)
 A=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(un),len(cand))).tocsr()
 return A,np.ones(len(un)),cand,un,keep
if __name__=='__main__':
 t0=time.time();out=[]
 for i,z in enumerate(Z):
  for j in [-1]+z['forced_cell_indices']:
   A,b,cand,un,keep=model(z,[] if j==-1 else [j])
   t=time.time()
   sol=linprog(np.zeros(len(cand)),A_eq=A,b_eq=b,bounds=(0,None),method='highs',options={'time_limit':8})
   x=sol.x
   error=float(np.max(np.abs(A@x-b))) if x is not None else None
   row={'motif':i,'removed_cell':j,'status':int(sol.status),'seconds':round(time.time()-t,3),'candidates':len(cand),'constraints':len(un),'positive':int(np.count_nonzero(x>1e-8)) if x is not None else None,'max_error':error}
   print(row,flush=True);out.append(row)
 json.dump({'results':out,'total_seconds':round(time.time()-t0,2)},open('E041_LP_MINIMALITY.json','w'),indent=2)
