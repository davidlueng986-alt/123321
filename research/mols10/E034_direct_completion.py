#!/usr/bin/env python3
"""Exact direct MILP for completing all 3 Latin squares from fixed near-triple rows.
Status 0=SAT only after exact independent integer replay; 2=UNSAT only solver-complete; 1=UNKNOWN.
"""
import json,itertools,time,argparse,collections
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
def make(I):
 P=((0,1),(0,2),(1,2))
 return all(len({(S[a][r][c],S[b][r][c]) for r in I for c in range(10)})==10*len(I) for a,b in P)
D=json.load(open(str(__import__('pathlib').Path(__file__).with_name('near_triple.json'))));S=D['squares'];P=((0,1),(0,2),(1,2))

def validate(Q):
 n=len(Q[0]);assert len(Q)==3 and all(len(x)==n for x in Q)
 for X in Q:
  for row in X:assert sorted(row)==list(range(n))
  for c in range(n):assert sorted(X[r][c] for r in range(n))==list(range(n))
 for x,y in P:assert len({(Q[x][r][c],Q[y][r][c]) for r in range(n) for c in range(n)})==n*n
 return True

def completion(I,secs=1,return_model=False,S_override=None):
 S=S_override if S_override is not None else globals()["S"]
 n=len(S[0]);k=len(I);m=n-k;used=[{(S[x][r][c],S[y][r][c]) for r in I for c in range(n)} for x,y in P]
 missing=[ [set(range(n))-{S[s][r][c] for r in I} for c in range(n)] for s in range(3)]
 edges=[[(a,b) for a in range(n) for b in range(n) if (a,b) not in used[p]] for p in range(3)]
 eidx=[{v:i for i,v in enumerate(e)} for e in edges]
 # rows: 6*n cell + m*3*n row symbol + 3*n*m col symbol + 3*n*m pair
 # all 1 exact-cover constraints, each candidate covers 1+3+3+3 = 10 constraints
 ncell=m*n;nrow=m*3*n;ncol=3*n*m;npair=3*n*m;total=ncell+nrow+ncol+npair
 cand=[];rr=[];cc=[]
 for r in range(m):
  for c in range(n):
   for a,b,d in itertools.product(*[sorted(missing[s][c]) for s in range(3)]):
    if (a,b) in used[0] or (a,d) in used[1] or (b,d) in used[2]:continue
    j=len(cand);cand.append((r,c,a,b,d));rows=[r*n+c]
    for s,v in enumerate((a,b,d)):
     rows.append(ncell+(r*3+s)*n+v)
     rows.append(ncell+nrow+(s*n+c)*m+sorted(missing[s][c]).index(v))
    for p,edge in enumerate(((a,b),(a,d),(b,d))):rows.append(ncell+nrow+ncol+p*n*m+eidx[p][edge])
    rr.extend(rows);cc.extend([j]*10)
 if not cand:return {'status':'UNSAT_EMPTY_DOMAIN','vars':0}
 A=coo_matrix((np.ones(len(rr),dtype=np.int8),(rr,cc)),shape=(total,len(cand))).tocsr()
 # sanity: every row has at least one candidate, otherwise sound UNSAT
 if any(np.diff(A.indptr)==0):return {'status':'UNSAT_EMPTY_ROW','vars':len(cand)}
 if return_model:return A,cand
 z=milp(np.zeros(len(cand)),integrality=np.ones(len(cand)),bounds=Bounds(0,1),constraints=LinearConstraint(A,1,1),options={'time_limit':secs,'mip_rel_gap':0})
 res={'status':{0:'SAT',1:'UNKNOWN_TIME',2:'UNSAT_COMPLETE',3:'UNBOUNDED',4:'ERROR'}.get(z.status,'ERROR'), 'vars':len(cand),'constraints':total,'nodes':int(getattr(z,'mip_node_count',0) or 0),'mip_gap':float(getattr(z,'mip_gap',0) or 0)}
 if z.status==0:
  Q=[[[S[s][rr][c] for c in range(n)] for rr in I]+[[None]*n for _ in range(m)] for s in range(3)]
  for j,v in enumerate(z.x):
   if v>.5:
    r,c,a,b,d=cand[j]
    for s,x in enumerate((a,b,d)):Q[s][k+r][c]=x
  validate(Q);res['solution']=Q
 return res

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=1.0);ap.add_argument('--max',type=int,default=39);arg=ap.parse_args()
 start=time.monotonic();out=[]
 for I in itertools.combinations(range(10),4):
  if not make(I):continue
  t=time.monotonic();z=completion(I,arg.seconds);z['rows']=list(I);z['wall_s']=round(time.monotonic()-t,3);out.append(z)
  print(I,z['status'],z['vars'],z['wall_s'],'nodes',z['nodes'],flush=True)
  if z['status']=='SAT' or len(out)>=arg.max:break
 print('SUMMARY',collections.Counter(x['status'] for x in out),'wall',round(time.monotonic()-start,3),flush=True)
 json.dump({'source':'near_triple.json','seconds_per_instance':arg.seconds,'results':out},open(str(__import__('pathlib').Path(__file__).with_name('E034_DIRECT_COMPLETION_RESULTS.json')),'w'),indent=2)
