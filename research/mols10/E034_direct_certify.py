#!/usr/bin/env python3
"""Create exact integer Farkas certificates from floating LP duals; all claims checked with integer arithmetic."""
import itertools,json,collections,time
import numpy as np
from scipy.optimize import linprog
from E034_direct_completion import completion,make
out=[];t0=time.monotonic()
for I in itertools.combinations(range(10),4):
 if not make(I):continue
 A,C=completion(I,return_model=True)
 z=linprog(-np.ones(A.shape[0]),A_ub=A.T,b_ub=np.zeros(A.shape[1]),bounds=[(-1,1)]*A.shape[0],method='highs-ipm',options={'time_limit':12})
 if z.status!=0:
  print('UNKNOWN',I,z.status,flush=True);out.append({'rows':list(I),'status':'UNKNOWN_DUAL'});continue
 found=False
 for scale in (1000,10000,100000,1000000):
  w=np.rint(scale*z.x).astype(np.int64)-1
  if int(w.sum())>0 and int((A.T@w).max())<=0:
   out.append({'rows':list(I),'status':'EXACT_INTEGER_FARKAS','weights':w.tolist(),'sum':int(w.sum()),'max_candidate_sum':int((A.T@w).max()),'scale':scale,'variables':A.shape[1],'constraints':A.shape[0]});found=True;break
 if not found:
  print('FAILED INTEGER ROUND',I,flush=True);out.append({'rows':list(I),'status':'UNKNOWN_RATIONAL'});continue
 print('EXACT',I,'scale',scale,'sum',int(w.sum()),'maxcol',int((A.T@w).max()),'sec',round(time.monotonic()-t0,2),flush=True)
json.dump({'source':'near_triple.json','layout':'cell;row-square-symbol;column-square-missing-symbol;pair-type-remaining-pair','certificates':out},open('/mnt/data/E034_FOUR_ROW_EXACT_DUALS.json','w'),separators=(',',':'))
print('SUMMARY',collections.Counter(x['status'] for x in out),'time',time.monotonic()-t0,flush=True)
