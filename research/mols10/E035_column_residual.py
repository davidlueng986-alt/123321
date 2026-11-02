#!/usr/bin/env python3
"""Six-resource residual exact-cover relaxation for partial 3-MOLS.
A fixed k-row prefix consumes P_AB, P_AC, P_BC ordered symbol pairs
and C_A, C_B, C_C column-symbol resources. Every remaining placement
consumes exactly one of each. Ax=1 is necessary, not sufficient.
"""
import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
from itertools import product
PAIRS=((0,1),(0,2),(1,2))

def model(S):
 n=len(S[0][0]);k=len(S[0]);assert len(S)==3 and all(len(A)==k for A in S)
 for A in S:
  assert all(set(row)==set(range(n)) for row in A)
  assert all(len(set(A[r][c] for r in range(k)))==k for c in range(n))
 occ=[{(S[i][r][c],S[j][r][c]) for r in range(k) for c in range(n)} for i,j in PAIRS]
 assert all(len(x)==k*n for x in occ)
 missing=[[set(range(n))-{S[i][r][c] for r in range(k)} for c in range(n)] for i in range(3)]
 pair=[[(a,b) for a in range(n) for b in range(n) if (a,b) not in occ[t]] for t in range(3)]
 constraints=[('P',t,a,b) for t in range(3) for a,b in pair[t]]
 constraints += [('C',s,c,v) for s in range(3) for c in range(n) for v in sorted(missing[s][c])]
 mapping={x:i for i,x in enumerate(constraints)}
 candidates=[];rows=[];cols=[]
 for c in range(n):
  for a,b,z in product(*(sorted(missing[s][c]) for s in range(3))):
   if (a,b) in occ[0] or (a,z) in occ[1] or (b,z) in occ[2]:continue
   j=len(candidates);candidates.append((c,a,b,z))
   for key in [('P',0,a,b),('P',1,a,z),('P',2,b,z),('C',0,c,a),('C',1,c,b),('C',2,c,z)]:
    rows.append(mapping[key]);cols.append(j)
 mat=coo_matrix((np.ones(len(rows),dtype=np.int8),(rows,cols)),shape=(len(constraints),len(candidates))).tocsr()
 return mat,candidates,constraints

def analyze(S,do_lp=True,do_milp=False,sec=3):
 A,T,E=model(S)
 deg=np.diff(A.indptr)
 res={'n':len(S[0][0]),'k':len(S[0]),'variables':len(T),'constraints':len(E),
      'zero_rows':int(sum(deg==0)), 'zero_pair_rows':int(sum(deg[i]==0 for i,e in enumerate(E) if e[0]=='P')),
      'zero_column_rows':int(sum(deg[i]==0 for i,e in enumerate(E) if e[0]=='C'))}
 if res['zero_rows']:
  res['status']='UNSAT_BY_SUPPORT';res['zero_examples']=[E[i] for i in range(len(E)) if deg[i]==0][:12];return res
 if not do_lp:return {**res,'status':'SUPPORT_PASS'}
 z=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(len(E)),bounds=(0,1),method='highs',options={'time_limit':sec})
 res['LP_status']={0:'SAT_RELAXED',1:'UNKNOWN_LIMIT',2:'INFEASIBLE_SOLVER',3:'UNBOUNDED',4:'ERROR'}.get(int(z.status));res['status']=res['LP_status']
 if z.status==0:
  err=float(np.max(np.abs(A@z.x-1)));res['LP_maxerr']=err
  assert err<1e-6
 if do_milp and z.status==0:
  z2=milp(np.zeros(len(T)),integrality=np.ones(len(T)),bounds=Bounds(0,1),constraints=LinearConstraint(A,1,1),options={'time_limit':sec,'mip_rel_gap':0})
  res['ILP_status']={0:'SAT_RELAXED',1:'UNKNOWN_LIMIT',2:'INFEASIBLE_SOLVER',3:'UNBOUNDED',4:'ERROR'}.get(int(z2.status))
  if z2.status==0:
   chosen=[T[i] for i,x in enumerate(z2.x) if x>.5]
   assert len(chosen)==len(S[0][0])*(len(S[0][0])-len(S[0]))
   assert all(abs(v-1)<1e-6 for v in A@np.round(z2.x))
   res['integer_witness']=chosen
 return res

def column_unit(S):
 A,T,E=model(S)
 m=A.shape[0];nvar=A.shape[1]
 incid=[A.indices[A.indptr[r]:A.indptr[r+1]].tolist() for r in range(m)]
 colrows=[[] for _ in range(nvar)]
 for r,row in enumerate(incid):
  for j in row:colrows[j].append(r)
 active=[True]*nvar;covered=[False]*m;to_check=list(range(m));forced=0;removed=0
 while to_check:
  r=to_check.pop()
  if covered[r]:continue
  cand=[j for j in incid[r] if active[j]]
  if not cand:return {'status':'UNSAT_UNIT','forced':forced,'removed':removed,'row':E[r]}
  if len(cand)>1:continue
  j=cand[0];forced+=1
  for e in colrows[j]:
   if covered[e]:return {'status':'UNSAT_UNIT','forced':forced,'removed':removed,'row':E[e]}
   covered[e]=True
  for e in colrows[j]:
   for j2 in incid[e]:
    if j2!=j and active[j2]:
     active[j2]=False;removed+=1
     for e2 in colrows[j2]:
      if not covered[e2]:to_check.append(e2)
 return {'status':'SURVIVES_UNIT','forced':forced,'removed':removed}
