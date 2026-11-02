#!/usr/bin/env python3
"""E047 deterministic full two-disjoint-swap regeneration for eight fixed k4 inputs.
Requires E035_column_residual.py, NumPy, SciPy. Restricted theorem only."""
import json,itertools,time
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
S=json.load(open('E047_SOURCES.json'))['sources']
def valid(U):
 for X in U:
  if any(set(r)!=set(range(10)) for r in X):return False
  if any(len({r[c] for r in X})!=4 for c in range(10)):return False
 for i,j in ((0,1),(0,2),(1,2)):
  if len({(U[i][r][c],U[j][r][c]) for r in range(4) for c in range(10)})!=40:return False
 return True
pairs=list(itertools.combinations(range(10),2))
disjoint=[(p,q) for k,p in enumerate(pairs) for q in pairs[k+1:] if len(set(p+q))==4]
assert len(disjoint)==630
records=[];counts={};start=time.monotonic()
for sid,U in S.items():
 count=0
 for (a,b),(c,d) in disjoint:
  for m in range(1,8):
   for n in range(1,8):
    V=[[r[:] for r in X] for X in U]
    for i in range(3):
     if m>>i&1:V[i][3][a],V[i][3][b]=V[i][3][b],V[i][3][a]
     if n>>i&1:V[i][3][c],V[i][3][d]=V[i][3][d],V[i][3][c]
    if not valid(V):continue
    count+=1;A,T,E=model(V)
    zeros=np.flatnonzero(np.diff(A.indptr)==0)
    if len(zeros):cert=['Z',list(E[int(zeros[0])])]
    else:
     z=linprog(-np.ones(A.shape[0]),A_ub=A.T,b_ub=np.zeros(len(T)),bounds=[(-1,1)]*A.shape[0],method='highs',options={'time_limit':3})
     if z.status!=0 or -z.fun<1e-6:raise RuntimeError(('UNKNOWN',sid,a,b,c,d,m,n,z.status))
     found=None
     for scale in (10,30,100,300,1000,3000,10000,30000,100000,300000,1000000):
      w=np.floor(z.x*scale+1e-9).astype(np.int64)-1
      if int(w.sum())>0 and np.max(A.T@w)<=0:found=w;break
     if found is None:raise RuntimeError(('UNKNOWN_DUAL',sid,a,b,c,d,m,n))
     cert=['D',int(w.sum()),[[int(i),int(v+1)] for i,v in enumerate(w) if v!=-1]]
    records.append([int(sid),a,b,c,d,m,n,cert])
 counts[sid]=count
 print('SOURCE',sid,count,'elapsed',round(time.monotonic()-start,1),flush=True)
assert sum(counts.values())==479
assert sum(x[7][0]=='Z' for x in records)==79
assert sum(x[7][0]=='D' for x in records)==400
json.dump({'counts':counts,'records':records,'scope':'Eight fixed-prefix local two-swap neighborhoods only'},open('E047_REGENERATED.json','w'),separators=(',',':'))
print('PASS',len(records),'exact certificates','elapsed',round(time.monotonic()-start,1))
