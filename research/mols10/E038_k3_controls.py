#!/usr/bin/env python3
"""Reproduce numerical k3 LP-feasibility controls for all E037 k4 sampled prefixes."""
import json,time,collections
from pathlib import Path
from E035_column_residual import analyze
BASE=Path(__file__).resolve().parent
D=json.load(open(BASE/'E037_ALL_CYCLES.json'));out=[];C=collections.Counter();start=time.time()
for t in D['cycle_results']:
 for idx,z in enumerate(t['results']):
  S=[A[:3] for A in z['prefix']]
  r=analyze(S,do_lp=True,sec=2)
  C[r['status']]+=1
  out.append({'cycle':t['cycle'],'index':idx,'status':r['status'],'maxerr':r.get('LP_maxerr')})
print('k3',dict(C),'seconds',round(time.time()-start,2))
with open(BASE/'E038_K3_LP_CONTROLS.json','w') as f:json.dump({'counts':dict(C),'results':out,'seconds':round(time.time()-start,2)},f,indent=2)