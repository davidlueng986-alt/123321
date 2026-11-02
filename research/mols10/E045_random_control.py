#!/usr/bin/env python3
"""Matched-parent randomized control for E045 LP-guided k4 row selection."""
import json,random,time
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
from E044_disjoint_probe import add_row
D=json.load(open("E044_RESULTS.json"));G=json.load(open("E045_GUIDED_RESULTS.json"))
parents=[p["parent_index"] for p in G["parents"]]
rng=random.Random(20261102047);t0=time.monotonic();cases=[];counts={}
for i in parents:
 S=[a[:3] for a in D["cases"][i]["prefix"]]
 for j in range(12):
  U,nodes=add_row(S,rng,12000)
  if U is None:st="BOUNDED_DFS_UNKNOWN";v=0;zero=-1
  else:
   A,T,E=model(U);v=len(T);zero=int(sum(np.diff(A.indptr)==0))
   if zero:st="ZERO_SUPPORT"
   else:
    z=linprog(np.zeros(v),A_eq=A,b_eq=np.ones(A.shape[0]),bounds=(0,1),method="highs",options={"time_limit":2})
    st={0:"LP_FEASIBLE",1:"UNKNOWN",2:"LP_INFEASIBLE",3:"UNKNOWN",4:"UNKNOWN"}[z.status]
  counts[st]=counts.get(st,0)+1
  cases.append({"parent":i,"attempt":j,"nodes":nodes,"variables":v,"zero_support":zero,"status":st})
res={"experiment":"E045-MATCHED-RANDOM","seed":20261102047,"parents":parents,"per_parent":12,"cases":cases,"summary":counts,"elapsed_s":round(time.monotonic()-t0,2),"scope":"Numerical LP screen and exact zero-support only; same k3 parents as guided."}
json.dump(res,open("E045_RANDOM_CONTROL.json","w"),separators=(",",":"))
print("RESULT",counts,"seconds",res["elapsed_s"])
