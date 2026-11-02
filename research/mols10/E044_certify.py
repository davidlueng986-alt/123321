#!/usr/bin/env python3
"""Upgrade E044 randomized fixed-prefix LP negatives to exact integer Farkas certificates.
Numerical duals only used to propose integer coefficients; integer inequalities are checked exactly.
"""
import json,time
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
D=json.load(open('E044_RESULTS.json'));out=[];failed=[];start=time.monotonic()
for ix,rec in enumerate(D['cases']):
 S=rec['prefix'];A,T,E=model(S);deg=np.diff(A.indptr)
 if np.any(deg==0):
  out.append({'index':ix,'kind':'ZERO','demand':list(E[int(np.flatnonzero(deg==0)[0])])});continue
 z=linprog(-np.ones(A.shape[0]),A_ub=A.T,b_ub=np.zeros(len(T)),bounds=[(-1,1)]*A.shape[0],method='highs',options={'time_limit':3})
 if z.status!=0 or -z.fun<1e-5:
  failed.append({'index':ix,'reason':'dual_solver','status':int(z.status)});continue
 found=None
 for scale in (10,30,100,300,1000,3000,10000,30000,100000,300000,1000000):
  w=np.floor(z.x*scale+1e-9).astype(np.int64)-1
  if int(w.sum())>0 and np.max(A.T@w)<=0:found=(scale,w);break
 if found is None:
  failed.append({'index':ix,'reason':'dual_rounding'});continue
 scale,w=found
 delta=[[int(i),int(v+1)] for i,v in enumerate(w) if v!=-1]
 out.append({'index':ix,'kind':'DUAL','delta':delta,'sum':int(w.sum()),'max':int(np.max(A.T@w)),'scale':scale})
 if ix%100==0:print('certified',ix,'elapsed',round(time.monotonic()-start,1),flush=True)
J={'experiment':'E044','scope':'512 independent random valid k4 fixed prefixes, NOT unrestricted','seed':D['seed'],'certificates':out,'failed':failed,'seconds':round(time.monotonic()-start,3)}
json.dump(J,open('E044_CERTIFICATES.json','w'),separators=(',',':'))
print('DONE',len(out),'failed',len(failed),'seconds',J['seconds'])
