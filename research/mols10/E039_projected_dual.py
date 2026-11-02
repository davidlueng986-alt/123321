#!/usr/bin/env python3
"""E039: exact integer Farkas certificate generator for a FIXED partial triple.
Usage: python E039_projected_dual.py prefix.json P0 C1 C2
Input: {"prefix":[A,B,C]} or [A,B,C], with k full rows in each.
P0=AB, P1=AC, P2=BC; C0=A, C1=B, C2=C.
The numerical LP proposes a witness; all claims are integer-verified.
"""
import sys,json,numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
def generate(S,selectors):
    A,T,E=model(S);n=len(T)
    cl=[]
    for v in selectors:
        assert len(v)==2 and v[0] in "PC" and v[1] in "012"
        cl.append((v[0],int(v[1])))
    assert len(set(cl))==len(cl) and 1<=len(cl)<=6
    rows=[i for i,e in enumerate(E) if e[:2] in cl]
    B=A[rows,:]
    deg=np.diff(B.indptr)
    if len(np.flatnonzero(deg==0)):
        j=rows[int(np.flatnonzero(deg==0)[0])]
        return {"kind":"ZERO_SUPPORT","demand":list(E[j]),"scope":"FIXED_PREFIX_ONLY"}
    primal=linprog(np.zeros(n),A_eq=B,b_eq=np.ones(len(rows)),
                   bounds=(0,None),method="highs",options={"time_limit":3})
    if primal.status!=2:
        return {"kind":"NO_EXACT_OBSTRUCTION","solver_status":int(primal.status),
                "scope":"FIXED_PREFIX_ONLY"}
    dual=linprog(-np.ones(len(rows)),A_ub=B.T,b_ub=np.zeros(n),
                 bounds=[(-1,1)]*len(rows),method="highs",options={"time_limit":3})
    if dual.status!=0 or dual.fun is None or -dual.fun<=1e-8:
        return {"kind":"UNKNOWN_DUAL","scope":"FIXED_PREFIX_ONLY"}
    for scale in (10,30,100,300,1000,3000,10000,100000):
        y=np.floor(dual.x*scale+1e-9).astype(np.int64)-1
        val=B.T@y
        if int(y.sum())>0 and int(val.max())<=0:
            # Independent re-enumeration, not just trusting the LP result.
            assert int(y.sum())>0
            assert all(int(v)<=0 for v in val)
            return {"kind":"EXACT_PROJECTED_FARKAS","classes":[list(c) for c in cl],
                    "weights":[[list(E[rows[i]]),int(y[i])] for i in np.flatnonzero(y)],
                    "weight_sum":int(y.sum()),"max_candidate_weight":int(val.max()),
                    "candidate_count":n,"scale":scale,"scope":"FIXED_PREFIX_ONLY"}
    return {"kind":"UNKNOWN_INTEGER_RECOVERY","scope":"FIXED_PREFIX_ONLY"}
if __name__=="__main__":
    assert len(sys.argv)>=3
    data=json.load(open(sys.argv[1]));S=data.get("prefix",data) if isinstance(data,dict) else data
    print(json.dumps(generate(S,sys.argv[2:]),indent=2))
