#!/usr/bin/env python3
"""Reproducible constrained multi-fiber MILP search for F3^7.

Choose k=3 or k=4 among 9 coordinate fibers {(x1,x2)=(a,b)}.
Each fiber contains 3 four-dimensional blocks (x0 fixed).
Release old points in these fibers, freeze all other old points, and
exclude every exterior point blocked by two frozen old points.
The remaining variables encode all admissible new cap memberships.

For each triple of collinear points:
  * with one frozen original, x_i+x_j<=1;
  * with all three variables, x_i+x_j+x_k<=2.
No other constraints are necessary. Exact checker replays every solution.
Only a proven MIP status warrants a restricted-optimum claim.
"""
import argparse
import itertools
import json
import time
from collections import defaultdict
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
from generate_calderbank_fishburn import construction
from verify_capset import verify

A=set(construction())
space=list(itertools.product(range(3),repeat=7))
sec=defaultdict(list)
AA=sorted(A)
for i,x in enumerate(AA):
    for y in AA[i+1:]:
        z=tuple((-p-q)%3 for p,q in zip(x,y))
        sec[z].append((x,y))

def solve(combination,limit=10.0):
    released=set(combination)
    frozen={p for p in A if p[1:3] not in released}
    incumbent=A-frozen
    outsiders={p for p in sec if p[1:3] in released
        and all(x not in frozen or y not in frozen for x,y in sec[p])}
    pool=sorted(incumbent|outsiders)
    idx={p:i for i,p in enumerate(pool)}
    rows=[];cols=[];data=[];upper=[];seen=set()
    for i,p in enumerate(pool):
        for j in range(i+1,len(pool)):
            q=pool[j];z=tuple((-x-y)%3 for x,y in zip(p,q))
            if z in frozen:
                for u in (i,j):rows.append(len(upper));cols.append(u);data.append(1)
                upper.append(1)
            elif z in idx:
                k=idx[z];tri=tuple(sorted((i,j,k)))
                if tri in seen:continue
                seen.add(tri)
                for u in tri:rows.append(len(upper));cols.append(u);data.append(1)
                upper.append(2)
    matrix=coo_matrix((data,(rows,cols)),shape=(len(upper),len(pool))).tocsr()
    tic=time.monotonic()
    res=milp(-np.ones(len(pool)),integrality=np.ones(len(pool)),
       bounds=Bounds(np.zeros(len(pool)),np.ones(len(pool))),
       constraints=LinearConstraint(matrix,-np.inf,upper),
       options={"time_limit":limit,"mip_rel_gap":0.0})
    report={"fibers":[list(p) for p in combination],"incumbent_released":len(incumbent),
      "new_exterior_candidates":len(outsiders),
      "binary_variables":len(pool),"constraints":len(upper),
      "runtime_s":round(time.monotonic()-tic,4),
      "proven_optimal":bool(res.success),"solver_message":res.message,
      "root_objective_upper_bound":float(-res.mip_dual_bound) if res.mip_dual_bound is not None else None}
    if res.x is not None:
        selection={p for i,p in enumerate(pool) if res.x[i]>.5}
        full=frozen|selection
        assert verify(full)==len(full)
        report.update({"verified_cap_size":len(full),
          "optimized_released_size":len(selection),
          "improvement":len(full)-236,
          "result_exactly_replayed":True})
        if res.success:
            assert round(-res.fun)==len(selection)
    return report

def run(k,limit,top):
    classes=list(itertools.product(range(3),repeat=2))
    candidates=[]
    for comb in itertools.combinations(classes,k):
        released=set(comb)
        frozen={p for p in A if p[1:3] not in released}
        avail=sum(p[1:3] in released and
          all(x not in frozen or y not in frozen for x,y in sec[p]) for p in sec)
        candidates.append((avail,comb))
    candidates.sort(key=lambda t:(-t[0],t[1]))
    all_results=[]
    for avail,comb in candidates[:top]:
        r=solve(comb,limit);all_results.append(r)
        print(json.dumps(r,sort_keys=True),flush=True)
        if r.get("verified_cap_size",0)>236:
            raise RuntimeError("Candidate exceeds 236: preserve witness + independently audit immediately.")
    return all_results

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--fibers",type=int,choices=[3,4],default=3)
    p.add_argument("--top",type=int,default=8)
    p.add_argument("--time-limit",type=float,default=10.)
    args=p.parse_args()
    results=run(args.fibers,args.time_limit,args.top)
    # These represent known 236-cap optimum only in the specified neighborhoods.
    if args.fibers in (3,4) and args.top==8:
        assert all(r["proven_optimal"] and r["verified_cap_size"]==236 for r in results)
    print("SUBPROBLEM AUDIT COMPLETE",len(results),"restricted MILP problems")
