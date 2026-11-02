#!/usr/bin/env python3
"""E046 bounded neighbor LP probe: exact certificates for infeasible cases; no global claim."""
import json,time
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
D=json.load(open("E045_GUIDED_RESULTS.json"))
start=time.monotonic()
out={"experiment":"E046_PHASE1","source":"E045 remote 570 exact-certified fixed prefixes",
"selection":"every eighth source index, first support-positive valid swap for masks 1 and 7",
"cases":[],"failed":[],"status_counts":{}}
def valid(S):
 for A in S:
  if any(len(set(row))!=10 for row in A):return False
  if any(len(set(A[r][c] for r in range(4)))!=4 for c in range(10)):return False
 for i,j in ((0,1),(0,2),(1,2)):
  if len({(S[i][r][c],S[j][r][c]) for r in range(4) for c in range(10)})!=40:return False
 return True
for ix in range(0,len(D["cases"]),8):
 S=D["cases"][ix]["prefix"]
 for mask in (1,7):
  selected=None
  for c in range(10):
   if selected:break
   for d in range(c+1,10):
    U=[[row[:] for row in A] for A in S]
    for s in range(3):
     if mask&(1<<s):U[s][3][c],U[s][3][d]=U[s][3][d],U[s][3][c]
    if not valid(U):continue
    A,T,E=model(U)
    if np.any(np.diff(A.indptr)==0):continue
    selected=(U,c,d,A,T,E);break
  if selected is None:continue
  U,c,d,A,T,E=selected
  rec={"source_index":ix,"mask":mask,"swap":[c,d],"prefix":U,"variables":len(T)}
  z=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(A.shape[0]),bounds=(0,1),
   method="highs",options={"time_limit":2})
  if z.status==0:
   rec["status"]="NUMERICAL_LP_FEASIBLE"
   rec["max_residual"]=float(np.max(np.abs(A@z.x-1)))
  elif z.status==2:
   y=linprog(-np.ones(A.shape[0]),A_ub=A.T,b_ub=np.zeros(len(T)),
    bounds=[(-1,1)]*A.shape[0],method="highs",options={"time_limit":3})
   found=None
   if y.status==0 and -y.fun>1e-5:
    for scale in (10,30,100,300,1000,3000,10000,30000,100000,300000,1000000):
     w=np.floor(y.x*scale+1e-9).astype(np.int64)-1
     if int(w.sum())>0 and np.max(A.T@w)<=0:found=(scale,w);break
   if found is not None:
    scale,w=found
    rec.update(status="EXACT_DUAL",dual={"delta":[[int(i),int(v+1)] for i,v in enumerate(w) if v!=-1],
     "sum":int(w.sum()),"max":int(np.max(A.T@w)),"scale":scale})
   else:rec.update(status="UNKNOWN_DUAL_FAILED",lp_status=2,dual_status=int(y.status))
  else:rec.update(status="UNKNOWN_LP",lp_status=int(z.status))
  out["cases"].append(rec);out["status_counts"][rec["status"]]=out["status_counts"].get(rec["status"],0)+1
  print(ix,mask,c,d,rec["status"],len(T),flush=True)
out["elapsed_s"]=round(time.monotonic()-start,2)
json.dump(out,open("E046_PHASE1_RESULTS.json","w"),separators=(",",":"))
print("SUMMARY",out["status_counts"],"n",len(out["cases"]),"elapsed",out["elapsed_s"])
