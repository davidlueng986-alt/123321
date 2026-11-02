#!/usr/bin/env python3
"""E045 exact integer Farkas certificates for fixed k4 prefixes. Bounded batch."""
import json,time,argparse
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
p=argparse.ArgumentParser();p.add_argument("--start",type=int,default=0);p.add_argument("--end",type=int,default=110);args=p.parse_args()
D=json.load(open("E045_GUIDED_RESULTS.json"));out=[];failed=[];t0=time.monotonic()
for ix in range(args.start,min(args.end,len(D["cases"]))):
    rec=D["cases"][ix];S=rec.get("prefix")
    if S is None:continue
    A,T,E=model(S);deg=np.diff(A.indptr)
    if np.any(deg==0):
        out.append({"index":ix,"kind":"ZERO","demand":list(E[int(np.flatnonzero(deg==0)[0])])});continue
    z=linprog(-np.ones(A.shape[0]),A_ub=A.T,b_ub=np.zeros(len(T)),bounds=[(-1,1)]*A.shape[0],method="highs",options={"time_limit":3})
    if z.status!=0 or -z.fun<1e-5:
        failed.append({"index":ix,"reason":"dual_solver","status":int(z.status)});continue
    found=None
    for scale in (10,30,100,300,1000,3000,10000,30000,100000,300000,1000000):
        w=np.floor(z.x*scale+1e-9).astype(np.int64)-1
        if int(w.sum())>0 and np.max(A.T@w)<=0:found=(scale,w);break
    if found is None:
        failed.append({"index":ix,"reason":"dual_rounding"});continue
    scale,w=found
    delta=[[int(i),int(v+1)] for i,v in enumerate(w) if v!=-1]
    out.append({"index":ix,"kind":"DUAL","delta":delta,"sum":int(w.sum()),"max":int(np.max(A.T@w)),"scale":scale})
    if ix%100==0:print("certified",ix,"elapsed",round(time.monotonic()-t0,2),flush=True)
J={"experiment":"E045","scope":"LP-guided fixed k4 prefixes, not unrestricted","certificates":out,"failed":failed,"seconds":round(time.monotonic()-t0,3)}
json.dump(J,open(f"E045_CERT_{args.start}_{args.end}.json","w"),separators=(",",":"))
print("DONE",len(out),"failed",len(failed),"seconds",J["seconds"],flush=True)
