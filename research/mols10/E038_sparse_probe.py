#!/usr/bin/env python3
"""Optional bounded search for sparse exact {0, +/-1} Farkas motifs (one case per f-type)."""
import json,sys,time,numpy as np
from pathlib import Path
BASE=Path(__file__).resolve().parent
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import hstack,vstack,csr_matrix
sys.path.insert(0,str(BASE));from E035_column_residual import model
D=json.load(open(str(BASE/'E037_ALL_CYCLES.json')))
OUT=[]
for i,b in enumerate(D['cycle_results']):
 z=next(x for x in b['results'] if x['status']=='INFEASIBLE_SOLVER' and not x['hall15']);A,T,E=model(z['prefix']);m=len(E)
 # x=(pos,neg); min cardinality, each in {0,1}; sum(pos-neg)>=1; A.T(pos-neg)<=0
 from scipy.sparse import csr_matrix
 M=hstack([A.T,-A.T],format='csr')
 demand=csr_matrix(np.r_[np.ones(m),-np.ones(m)].reshape(1,-1))
 X=vstack([M,demand],format='csr');lo=np.r_[np.full(len(T),-np.inf),1.];hi=np.r_[np.zeros(len(T)),np.inf]
 start=time.time();r=milp(np.ones(2*m),integrality=np.ones(2*m),bounds=Bounds(0,1),constraints=LinearConstraint(X,lo,hi),options={'time_limit':8,'mip_rel_gap':0})
 record={'cycle':b['cycle'],'instance':b['results'].index(z),'status':int(r.status),'seconds':round(time.time()-start,3)}
 if r.x is not None:
  w=np.rint(r.x[:m]-r.x[m:]).astype(int)
  if w.sum()>0 and max(A.T@w)<=0:
   record.update({'certified':True,'support':int(np.count_nonzero(w)),'weight_sum':int(w.sum()),'weights':[[list(E[j]),int(w[j])] for j in np.flatnonzero(w)]})
  else:record['certified']=False
 OUT.append(record)
 print('SPARSE',b['cycle'],record['status'],record.get('support'),record['seconds'],flush=True)
json.dump(OUT,open(str(BASE/'E038_SPARSE_PROBES.json'),'w'),indent=2)