#!/usr/bin/env python3
"""E012 reproducible bounded HiGHS MILP for first-square trade orthogonal mates.

Requires scipy and numpy. Solver statuses: verified integral solution -> SAT;
time limit without witness -> UNKNOWN; infeasibility only if proved by HiGHS.
Never interpret a bounded timeout as UNSAT.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
from first_square_trades import first_square_trades
from sample_mates import transversals_single, transversals_pair
from verify import analyze

ROOT=Path(__file__).resolve().parent

def cover_matrix(trans, n):
    rows=[]; cols=[]
    for k,p in enumerate(trans):
        for i,j in enumerate(p):
            rows.append(i*n+j); cols.append(k)
    return coo_matrix((np.ones(len(rows)),(rows,cols)),
                      shape=(n*n,len(trans))).tocsr()

def solve(a, time_limit=6.0, objective=None):
    n=len(a);trans=transversals_single(a)
    mat=cover_matrix(trans,n)
    costs=np.zeros(len(trans)) if objective is None else np.array(objective,dtype=float)
    start=time.monotonic()
    r=milp(c=costs,integrality=np.ones(len(trans)),
           bounds=Bounds(0,1),
           constraints=LinearConstraint(mat,np.ones(n*n),np.ones(n*n)),
           options={"time_limit":time_limit,"mip_rel_gap":0.001})
    output={"solver_status_code":int(r.status),"message":str(r.message),
            "elapsed_seconds":round(time.monotonic()-start,3),
            "A_transversals":len(trans),
            "mip_dual_bound":None if getattr(r,"mip_dual_bound",None) is None else float(r.mip_dual_bound),
            "mip_gap":None if getattr(r,"mip_gap",None) is None else float(r.mip_gap)}
    if r.x is not None:
        indices=np.flatnonzero(r.x>0.5)
        valid=len(indices)==n and np.all(np.asarray(mat[:,indices].sum(axis=1)).ravel()==1)
        if valid:
            b=[[-1]*n for _ in range(n)]
            for symbol,k in enumerate(indices):
                for i,j in enumerate(trans[k]): b[i][j]=symbol
            assert all(p["orthogonal"] for p in analyze([a,b],n))
            output.update(status="SAT_WITNESS",mate=b)
            return output
    output["status"]="UNSAT_FIXED_A" if r.status==2 else "UNKNOWN_BUDGET"
    return output

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--seconds",type=float,default=6.0)
    parser.add_argument("--indices",type=int,nargs="+",default=[12,20,30,40,47])
    parser.add_argument("--output",default="E012_milp_replay.json")
    args=parser.parse_args()
    base=json.loads((ROOT/"near_triple.json").read_text())["squares"]
    trades=first_square_trades(base[0])
    result=[]
    for i in args.indices:
        a=trades[i]["square"]
        r=solve(a,time_limit=args.seconds)
        if r["status"]=="SAT_WITNESS":
            common,support=transversals_pair(a,r["mate"])
            r["common_transversals"]=len(common)
            r["unsupported_cells"]=sum(v==0 for v in support)
        result.append({"trade_index":i,"trade_symbols":trades[i]["symbols"],
                       "trade_size":trades[i]["size"],**r})
        print(i,r["status"],r.get("common_transversals"),
              r.get("unsupported_cells"),flush=True)
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+"\n")
