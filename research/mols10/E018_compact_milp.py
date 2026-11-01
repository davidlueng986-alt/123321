#!/usr/bin/env python3
"""Exact fixed-first-square 3-MOLS feasibility MILP (independent of E016/E017 pruning).
Two binary vectors x,y choose ten A-transversals each, exactly covering every cell.
For each selected transversal i on side x, ALL ten chosen y-transversals must
intersect it in exactly one cell; and conversely. This is an exact integer model.
The big-M value is n (the number of selected transversals), not an approximation.
SAT must be independently replayed; UNSAT requires solver-complete status.
"""
import argparse, itertools, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix, vstack

def enumerate_transversals(A):
 n=len(A);res=[]
 def visit(r,cols,syms,mask):
  if r==n:res.append(mask);return
  for c in range(n):
   bit=1<<c;v=1<<A[r][c]
   if not cols&bit and not syms&v:
    visit(r+1,cols|bit,syms|v,mask|(1<<(r*n+c)))
 visit(0,0,0,0)
 return res

def solve(A,seconds=10,paircuts=False):
 start=time.monotonic();n=len(A);assert all(set(row)==set(range(n)) for row in A)
 assert all({A[r][c] for r in range(n)}==set(range(n)) for c in range(n))
 masks=enumerate_transversals(A);m=len(masks)
 if m==0:
  out={"n":n,"transversals":0,"status":"UNSAT_FIXED_A_NO_TRANSVERSAL","total_seconds":round(time.monotonic()-start,3)}
  print(json.dumps(out));return out
 # Cell equalities: each chosen B and C partition the grid separately.
 row=[];col=[];data=[]
 for k,mask in enumerate(masks):
  for cell in range(n*n):
   if mask>>cell&1:
    for side in range(2):row.append(side*n*n+cell);col.append(side*m+k);data.append(1)
 exact=coo_matrix((np.asarray(data,dtype=np.float64),(row,col)),shape=(2*n*n,2*m)).tocsr()
 # Compatibility constraints: sum_{j: |Ti ∩ Tj|=1} y_j >= n*x_i,
 # and symmetric x/y swapped. Since exactly n y-classes are selected,
 # these force ALL selected cross-pairs to intersect exactly once.
 row=[];col=[];data=[]
 for i,u in enumerate(masks):
  for side in range(2):
   row.append(side*m+i);col.append(side*m+i);data.append(-n)
  for j,v in enumerate(masks):
   if (u&v).bit_count()==1:
    row.extend([i,m+j]);col.extend([m+j,i]);data.extend([1,1])
 compat=coo_matrix((np.asarray(data,dtype=np.float64),(row,col)),shape=(2*m,2*m)).tocsr()
 Acon=vstack([exact,compat],format='csr')
 cuts=0
 if paircuts:
  refs=[0]*(n*n)
  for i,mask in enumerate(masks):
   for cell in range(n*n):
    if mask>>cell&1:refs[cell]|=1<<i
  compatible=[]
  for u in masks:
   bits=0
   for j,v in enumerate(masks):
    if (u&v).bit_count()==1:bits|=1<<j
   compatible.append(bits)
  rr=[];cc=[];dd=[]
  for i,u in enumerate(masks):
   for j in range(i+1,m):
    if u&masks[j]:continue
    common=compatible[i]&compatible[j]
    if all(common&ref for ref in refs):continue
    for side in range(2):
     rr.extend([cuts,cuts]);cc.extend([side*m+i,side*m+j]);dd.extend([1,1]);cuts+=1
  if cuts:
   extra=coo_matrix((np.asarray(dd,dtype=np.float64),(rr,cc)),shape=(cuts,2*m)).tocsr()
   Acon=vstack([Acon,extra],format='csr')
 print(json.dumps({'phase':'model','n':n,'transversals':m,'variables':2*m,'constraints':2*n*n+2*m+cuts,'pair_cuts':cuts,'nnz':int(Acon.nnz),'setup_seconds':round(time.monotonic()-start,3)}),flush=True)
 lo=np.r_[np.ones(2*n*n),np.zeros(2*m)]
 hi=np.r_[np.ones(2*n*n),np.full(2*m,np.inf),np.ones(cuts)]
 lo=np.r_[lo,np.full(cuts,-np.inf)]
 res=milp(np.zeros(2*m),integrality=np.ones(2*m),bounds=Bounds(0,1),constraints=LinearConstraint(Acon,lo,hi),options={'time_limit':seconds,'disp':False})
 out={'n':n,'transversals':m,'solver_status':int(res.status),'message':str(res.message),'total_seconds':round(time.monotonic()-start,3),'objective':float(res.fun) if res.fun is not None else None,'mip_gap':float(res.mip_gap) if getattr(res,'mip_gap',None) is not None else None}
 if res.x is not None:
  ix=np.flatnonzero(res.x[:m]>.5).tolist();iy=np.flatnonzero(res.x[m:]>.5).tolist()
  out['selected_counts']=[len(ix),len(iy)]
  out['independent_replay']=len(ix)==len(iy)==n and all(sum(bool(masks[k]>>cell&1) for k in ids)==1 for ids in (ix,iy) for cell in range(n*n)) and all((masks[i]&masks[j]).bit_count()==1 for i in ix for j in iy)
  if out['independent_replay']:
   B=[[-1]*n for _ in range(n)];C=[[-1]*n for _ in range(n)]
   for side,ids in ((B,ix),(C,iy)):
    for sym,k in enumerate(ids):
     for cell in range(n*n):
      if masks[k]>>cell&1:side[cell//n][cell%n]=sym
   out['squares']=[B,C]
 print(json.dumps(out,indent=2),flush=True)
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--case',choices=['parker','gf4','order6'],default='parker');p.add_argument('--seconds',type=float,default=10);p.add_argument('--paircuts',action='store_true');args=p.parse_args()
 if args.case=='gf4':A=[[i^j for j in range(4)] for i in range(4)]
 elif args.case=='order6':
  A=[[(i+j)%6 for j in range(6)] for i in range(6)]
  A[0][0],A[0][3]=A[0][3],A[0][0]
  A[3][0],A[3][3]=A[3][3],A[3][0]
 else:A=json.loads((Path(__file__).resolve().parent/'parker_pair.json').read_text())['squares'][0]
 solve(A,args.seconds,args.paircuts)
