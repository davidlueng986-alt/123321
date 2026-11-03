#!/usr/bin/env python3
"""Goal-first: test whether M287 can be excluded from exact hyperplane moments + all quadratic rank classes.
Uses CAP020 rigorous high-slice bound; LP feasibility is ONLY necessary, NOT actual cap.
"""
from itertools import product
from collections import Counter
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
import numpy as np
M=287;UP=[56,58,59,61,63]
P=[]
for a in range(112,-1,-1):
 for b in range(a,-1,-1):
  c=M-a-b
  if 0<=c<=b:
   if a>=110 and b>=110 and c>UP[(112-a)+(112-b)]:continue
   P.append((a,b,c))
assert len(P)==219
Rtypes={(0,0,2):0,(1,2,2):1,(0,1,1):2}
def resid(p):return Rtypes[tuple(sorted(x%3 for x in p))]
def spectra(n):
 for r in range(n+1):
  for sig in ([0] if r==0 else [1,2]):
   q=Counter()
   for x in product(range(3),repeat=r):
    v=(sum(t*t for t in x[:-1]) + (sig*x[-1]**2 if r else 0))%3
    q[v]+=3**(n-r)
   q[0]-=1
   if any(q[t]%2 for t in range(3)):raise ValueError('projective counts not even')
   yield (r,sig),tuple(q[t]//2 for t in range(3))
TARGET=[1093,364*M*M+729*M,121*M*(M-1)*(M-2)+1092*M*(M-1)+1093*M]

def model(zero_mode,spec):
 if zero_mode:
  opts=[(p,0,resid(p)) for p in P]
  required=[spec[0],spec[1],spec[2]]
 else:
  opts=[(p,t,resid(p)) for p in P for t in [0,1]]
  required=[spec[0],spec[1],spec[2]]
  # L!=0 q distribution unconstrained for now.
 rows=[]
 for p,l,q in opts:
  a,b,c=p
  v=[1,a*a+b*b+c*c, a**3+b**3+c**3]
  if zero_mode:v +=[int(q==j) for j in range(3)]
  else:v +=[int(l==0 and q==j) for j in range(3)]
  rows.append(v)
 A=np.array(rows,dtype=float).T
 targets=TARGET+required
 # center and scale all rows
 A[1]-=27000*A[0];A[2]-=2600000*A[0]
 targets[1]-=27000*TARGET[0];targets[2]-=2600000*TARGET[0]
 scales=np.array([1,1000,100000]+[1]*3)[:,None]
 A=A/scales;tgt=np.array(targets)/scales.ravel()
 r=linprog(np.zeros(len(opts)),A_eq=A,b_eq=tgt,bounds=(0,None),method='highs')
 return r,opts,A,tgt

if __name__=='__main__':
 for mode,n in [('b0',7),('b1',6)]:
  total=0; feasible=[]
  for (rank,sig),s in spectra(n):
   res,opts,A,tgt=model(mode=='b0',s)
   total+=1
   if res.success:
    feasible.append((rank,sig,s,opts,res))
   print(mode,rank,sig,s,'LP',res.status)
  print('SUMMARY',mode, 'of',total,'LP feasible',len(feasible))
  if feasible:
   rank,sig,s,opts,res=feasible[0]
   print('first LP support',[(opts[i],round(v,5)) for i,v in enumerate(res.x) if v>1e-6][:15])
