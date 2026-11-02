#!/usr/bin/env python3
"""E026: fixed-pair one-sided k-symbol orthogonality-preserving trades.
Run from research/mols10: python E026_symbol_support_milp.py
Dependencies: scipy, numpy, E024_appendix_six_replay.py.
No global MOLS(10) claim. Solver status 2 means proven infeasible for that instance.
"""
import itertools, json, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from E024_appendix_six_replay import RAW, parse, derive, latin

def overlay(a,b):
 n=len(a)
 return len({(a[r][c],b[r][c]) for r in range(n) for c in range(n)})

def find_trade(z,q,S,time_limit=1.0):
 n=len(z);k=len(S)
 cells=[(r,c) for r in range(n) for c in range(n) if z[r][c] in S]
 assert len(cells)==n*k
 rows=[];lower=[];upper=[]
 def add(indices,lo,hi):rows.append(indices);lower.append(lo);upper.append(hi)
 for i in range(n*k):add([k*i+j for j in range(k)],1,1)
 for dimension in range(3):
  for v in range(n):
   ids=[i for i,(r,c) in enumerate(cells) if (r,c,q[r][c])[dimension]==v]
   assert len(ids)==k
   for j in range(k):add([k*i+j for i in ids],1,1)
 # WLOG: independently relabel selected symbols to match original row zero.
 for i,(r,c) in enumerate(cells):
  if r==0:add([k*i+S.index(z[r][c])],1,1)
 # Exclude unchanged solution after this normalization.
 add([k*i+S.index(z[r][c]) for i,(r,c) in enumerate(cells)],0,n*k-1)
 a=lil_matrix((len(rows),n*k*k),dtype=float)
 for row,ids in enumerate(rows):
  for j in ids:a[row,j]=1
 res=milp(c=np.zeros(n*k*k),integrality=np.ones(n*k*k),bounds=Bounds(0,1),
          constraints=LinearConstraint(a.tocsr(),lower,upper),options={'time_limit':time_limit})
 if res.status==0:
  new=[row[:] for row in z]
  for i,(r,c) in enumerate(cells):new[r][c]=S[int(np.argmax(res.x[k*i:k*i+k]))]
  assert all(len(set(row))==n for row in new)
  assert all(len({new[r][c] for r in range(n)})==n for c in range(n))
  assert overlay(new,q)==n*n and new!=z
  return 0,new
 return int(res.status),None

def gf9_control():
 add=lambda x,y:(x%3+y%3)%3+3*((x//3+y//3)%3)
 mulalpha=lambda x:(2*(x//3)%3)+3*(x%3)
 z=[[add(r,c) for c in range(9)] for r in range(9)]
 q=[[add(r,mulalpha(c)) for c in range(9)] for r in range(9)]
 assert overlay(z,q)==81
 status,witness=find_trade(z,q,[0,1,2],time_limit=5.0)
 assert status==0 and witness is not None
 return {'status':'SAT','n':9,'k':3,'overlay':overlay(witness,q),
         'changed_cells':sum(witness[r][c]!=z[r][c] for r in range(9) for c in range(9)),
         'witness_rows':[''.join(map(str,row)) for row in witness]}

def main():
 results={'gf9_positive':gf9_control(),'cases':{}}
 for label,(pstr,qstr) in RAW.items():
  p,q=parse(pstr),parse(qstr);z=derive(p,q)
  assert latin(p) and latin(q) and latin(z) and overlay(z,q)==100
  byk={}
  for k in (3,4,5):
   start=time.monotonic();counts={};unknown=[];sat=[]
   for S in itertools.combinations(range(10),k):
    status,w=find_trade(z,q,list(S),time_limit=1.0)
    counts[str(status)]=counts.get(str(status),0)+1
    if status==0:sat.append({'symbols':S,'square':w})
    elif status!=2:unknown.append(S)
   byk[str(k)]={'counts':counts,'unknown':unknown,'sat':sat,
                'seconds':round(time.monotonic()-start,3)}
   print(label,k,counts,'unknown',len(unknown),flush=True)
  results['cases'][label]=byk
 with open('E026_MILP_RESULTS.json','w') as f:json.dump(results,f,indent=2)
 return results
if __name__=='__main__':main()
