#!/usr/bin/env python3
"""Numerical LP sanity comparison on each three-row parent, not exact primal proof."""
import json,time,collections,numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
D=json.load(open('E044_RESULTS.json'))
out=[];cnt=collections.Counter();t=time.monotonic()
for i,rec in enumerate(D['cases']):
 S=[[row[:] for row in sq[:3]] for sq in rec['prefix']]
 A,T,E=model(S)
 if np.any(np.diff(A.indptr)==0):status='EXACT_ZERO_SUPPORT';err=None
 else:
  z=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(A.shape[0]),bounds=(0,1),method='highs',options={'time_limit':2})
  status={0:'NUMERIC_FEASIBLE',1:'UNKNOWN',2:'NUMERIC_INFEASIBLE',3:'UNBOUNDED',4:'ERROR'}[z.status]
  err=float(max(abs(A@z.x-1))) if z.x is not None else None
 cnt[status]+=1;out.append({'index':i,'status':status,'variables':len(T),'error':err})
json.dump({'counts':dict(cnt),'elapsed_s':round(time.monotonic()-t,2),'cases':out},open('E044_K3_CONTROLS.json','w'),indent=2)
print('k3',cnt,'time',round(time.monotonic()-t,2))
