#!/usr/bin/env python3
"""Attempt to close M=287 by finding contradiction from full 2nd/3rd hyperplane moments + CAP019 high-slice bound.
A *feasible* moment histogram is not a cap; it refutes the sufficiency of that relaxation only.
"""
import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
from math import floor
from collections import Counter
from fractions import Fraction
UP=[56,58,59,61,63]

def profiles(M):
 out=[]
 for a in range(112,-1,-1):
  for b in range(min(a,112),-1,-1):
   c=M-a-b
   if c<0 or c>b or c>112:continue
   if a>=110 and b>=110 and c>UP[(112-a)+(112-b)]:continue
   out.append((a,b,c))
 return out

def target(M):
 return [1093, 364*M*M+729*M,121*M*(M-1)*(M-2)+1092*M*(M-1)+1093*M]

for M in range(287,280,-1):
 P=profiles(M)
 A=np.array([[1]*len(P),[sum(v*v for v in t) for t in P], [sum(v**3 for v in t) for t in P]],dtype=float)
 b=target(M)
 # center moments to avoid conditioning: sum S2-3(around M/3)^2; sum S3 similarly
 A[1]-=(M*M/3)
 A[2]-=(M*M*M/9)
 b[1]-=1093*M*M/3
 b[2]-=1093*M*M*M/9
 B=A/np.array([[1],[1000],[10000]])
 tgt=np.array(b)/[1,1000,10000]
 r=linprog(np.zeros(len(P)),A_eq=B,b_eq=tgt,bounds=(0,None),method='highs')
 print('M',M,'num profiles',len(P),'LP',r.status,'success',r.success,'message',r.message)
 if r.success:
  x=r.x
  print('  nonzero fractional support',[(P[i],round(v,3)) for i,v in enumerate(x) if v>1e-6][:10])
  if M==287:
   intres=milp(c=np.zeros(len(P)),integrality=np.ones(len(P)),bounds=Bounds(np.zeros(len(P)),np.ones(len(P))*1093),constraints=LinearConstraint(B,tgt,tgt),options={'time_limit':8})
   print('  M287 integer',intres.status,intres.message,'support',[(P[i],round(v)) for i,v in enumerate(intres.x) if v>.5][:12] if intres.x is not None else None)
