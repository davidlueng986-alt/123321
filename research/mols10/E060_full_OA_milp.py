#!/usr/bin/env python3
"""FULL 5-coordinate OA(n^2,5,n,2) direct exact-cover MILP, no fixed
near-triple. Any solution corresponds exactly to three MOLS(n).
Sound normalizations: independently relabel symbols in three squares to
make first row identical [0..n-1]; permute rows 1..n-1 so A[r,0]==r.
Consequently every non-first-row cell has a,b,d distinct (otherwise a pair
repeats the first-row diagonal). The model retains all normalized solutions.
A solver timeout is UNKNOWN, never UNSAT. Independent witness validation.
"""
import json,sys,time,itertools,numpy as np
from pathlib import Path
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

def verify(S):
 n=len(S[0]); T=set(range(n))
 assert len(S)==3
 for M in S:
  assert len(M)==n and all(set(r)==T for r in M)
  assert all({M[r][c] for r in range(n)}==T for c in range(n))
 overlays=[]
 for a,b in ((0,1),(0,2),(1,2)):
  pairs={(S[a][r][c],S[b][r][c]) for r in range(n) for c in range(n)}
  overlays.append(len(pairs));assert len(pairs)==n*n
 return overlays

def build(n):
 m=10*n*n;triples=[]; rr=[];cc=[]
 def add(r,c,a,b,d):
  j=len(triples);triples.append((r,c,a,b,d))
  indices=[r*n+c]
  for s,v in enumerate((a,b,d)):
   indices.extend([n*n+(2*s)*n*n+r*n+v,n*n+(2*s+1)*n*n+c*n+v])
  for z,(x,y) in enumerate(((a,b),(a,d),(b,d))):
   indices.append(7*n*n+z*n*n+x*n+y)
  assert len(indices)==10
  rr.extend(indices);cc.extend([j]*10)
 for r in range(n):
  for c in range(n):
   if r==0:
    add(r,c,c,c,c);continue
   # Symbols cannot equal c after normalized first row; pairwise distinct.
   vals=[x for x in range(n) if x!=c]
   for a in ([r] if c==0 else vals):
    for b in vals:
     if b==a:continue
     for d in vals:
      if d==a or d==b:continue
      add(r,c,a,b,d)
 A=coo_matrix((np.ones(len(rr),dtype=np.float64),(rr,cc)),shape=(m,len(triples))).tocsr()
 assert A.nnz==len(rr)
 return A,triples

def solve(n,budget):
 A,options=build(n);m=A.shape[0]
 print('MODEL',n,'vars',len(options),'constraints',m,'ones',A.nnz,flush=True)
 t=time.monotonic()
 res=milp(np.zeros(len(options)),integrality=np.ones(len(options)),bounds=Bounds(0,1),
          constraints=LinearConstraint(A,np.ones(m),np.ones(m)),
          options={'time_limit':budget,'mip_rel_gap':0.0,'presolve':True,'disp':False})
 secs=round(time.monotonic()-t,4)
 report={'n':n,'solver_status_code':int(res.status),'message':str(res.message),
         'elapsed_solve':secs,'variables':len(options),'constraints':m,'nonzeros':int(A.nnz),
         'status': {0:'SAT',1:'UNKNOWN_BUDGET',2:'UNSAT_EXHAUSTIVE',3:'UNBOUNDED',4:'ERROR'}.get(int(res.status),'ERROR')}
 if res.status==0:
  S=[[[-1]*n for _ in range(n)] for __ in range(3)]
  xs=np.where(res.x>0.5)[0]
  assert len(xs)==n*n
  for j in xs:
   r,c,a,b,d=options[j]
   for i,v in enumerate((a,b,d)):
    assert S[i][r][c]==-1
    S[i][r][c]=v
  report['overlays']=verify(S);report['witness']=S
  print('SUCCESS',report['overlays'],flush=True)
 print('RESULT',json.dumps({k:v for k,v in report.items() if k!='witness'}),flush=True)
 return report
if __name__=='__main__':
 runs=[(4,3),(5,5),(10,20)]
 if len(sys.argv)>1:runs=[(int(sys.argv[1]),float(sys.argv[2]) if len(sys.argv)>2 else 20)]
 out=[solve(n,t) for n,t in runs]
 json.dump(out,open(Path(__file__).with_name('E060_GLOBAL_OA_MILP_RESULTS.json'),'w'),indent=2)