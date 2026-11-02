#!/usr/bin/env python3
"""Generate exact integer Farkas/zero-support certificates for E037 360 samples.
Only fixed-prefix conclusions. Solver outputs are NOT trusted by verifier.
"""
import json,sys,time,collections,math
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from E035_column_residual import model
SRC=BASE/'E037_ALL_CYCLES.json'
OUT=BASE/'E038_CERTIFICATES.json'
data=json.loads(SRC.read_text());out=[];start=time.time();counters=collections.Counter()
for t,block in enumerate(data['cycle_results']):
 for idx,z in enumerate(block['results']):
  S=z['prefix'];A,T,E=model(S)
  assert len(E)==360 and len(S[0])==4
  deg=np.diff(A.indptr)
  if (deg==0).any():
   row=int(np.flatnonzero(deg==0)[0]);cert={'cycle':block['cycle'],'index':idx,'prefix':S,'kind':'ZERO_SUPPORT','demand':list(E[row])}
  else:
   r=linprog(-np.ones(len(E)),A_ub=A.T,b_ub=np.zeros(len(T)),bounds=[(-1,1)]*len(E),method='highs',options={'time_limit':2})
   if r.status!=0 or r.fun is None or -r.fun<0.01:
    cert={'cycle':block['cycle'],'index':idx,'prefix':S,'kind':'UNRESOLVED','status':int(r.status),'dual_objective':None if r.fun is None else float(-r.fun)}
   else:
    # Round DOWN and shift by one: exact verification below is decisive.
    found=None
    for scale in (30,50,100,200,500,1000,10000):
     w=np.floor(r.x*scale+1e-9).astype(np.int64)-1
     maxw=int(np.max(A.T@w))
     if int(w.sum())>0 and maxw<=0:
      found=(scale,w,maxw);break
    if found is None:
     cert={'cycle':block['cycle'],'index':idx,'prefix':S,'kind':'UNRESOLVED','status':'INTEGER_RECOVERY_FAILED'}
    else:
     scale,w,maxw=found
     cert={'cycle':block['cycle'],'index':idx,'prefix':S,'kind':'EXACT_INTEGER_FARKAS','weights':[int(x) for x in w], 'weight_sum':int(w.sum()),'max_candidate_weight':maxw,'scale':scale,'candidates':len(T)}
  counters[cert['kind']]+=1;out.append(cert)
 print('TYPE',block['cycle'],dict(counters),flush=True)
obj={'experiment':'E038','source':'E037_ALL_CYCLES.json','sample_scope':'360 FIXED four-row prefixes, 30 per 12 f cycle types, NOT exhaustive','certificates':out,'summary':dict(counters),'seconds':round(time.time()-start,2)}
OUT.write_text(json.dumps(obj,separators=(',',':'))+'\n')
print('FINAL',dict(counters),'seconds',round(time.time()-start,2),'bytes',OUT.stat().st_size,flush=True)