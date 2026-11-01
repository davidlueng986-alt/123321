#!/usr/bin/env python3
"""Finite 0/1 MILP for coordinated deletion-and-reconstruction of a cap.

Binary u_i: delete original cap point a_i; binary v_j: add candidate outsider b_j.
For every 3-term line, forbid all three endpoints surviving/selected.
Objective minimizes #deletions - #additions (negative means record improvement).
Candidate pool is restricted by a secant-count threshold, so the optimum
ONLY certifies the chosen restricted pool, NOT the global cap-set problem.

Requires numpy and scipy (CPU only).
"""
import argparse
import collections
import itertools
import json
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
from generate_calderbank_fishburn import construction
from verify_capset import verify

def solve(max_secants=10,min_additions=1,time_limit=25):
    A=construction()
    original=set(A)
    index={p:i for i,p in enumerate(A)}
    secants=collections.defaultdict(list)
    for i,p in enumerate(A):
        for j in range(i+1,len(A)):
            q=A[j]
            z=tuple((-x-y)%3 for x,y in zip(p,q))
            secants[z].append((i,j))
    pool=sorted(p for p in secants if len(secants[p])<=max_secants)
    m=len(pool)
    if m<min_additions:
        raise ValueError("Not enough candidates to meet min_additions")
    pool_index={p:j for j,p in enumerate(pool)}
    constraints=[]
    rhs=[]
    def add(terms,limit):
        constraints.append(terms);rhs.append(limit)
    for j,p in enumerate(pool):
        for i,k in secants[p]:
            add([(236+j,1),(i,-1),(k,-1)],0)
    for i,p in enumerate(pool):
        for j in range(i+1,m):
            q=pool[j]
            z=tuple((-x-y)%3 for x,y in zip(p,q))
            if z in index:
                add([(236+i,1),(236+j,1),(index[z],-1)],1)
            elif z in pool_index and j<pool_index[z]:
                add([(236+i,1),(236+j,1),(236+pool_index[z],1)],2)
    add([(236+j,-1) for j in range(m)],-min_additions)
    row=[];col=[];data=[]
    for k,terms in enumerate(constraints):
        for pos,coeff in terms:
            row.append(k);col.append(pos);data.append(coeff)
    mat=coo_matrix((data,(row,col)),shape=(len(rhs),236+m)).tocsr()
    c=np.array([1.0]*236+[-1.0]*m)
    result=milp(c,integrality=np.ones(236+m),
        bounds=Bounds(np.zeros(236+m),np.ones(236+m)),
        constraints=LinearConstraint(mat,-np.inf,np.array(rhs)),
        options={"time_limit":time_limit,"mip_rel_gap":0})
    answer={"candidate_count":m,"max_secants":max_secants,
        "min_additions":min_additions,"status":str(result.message),
        "is_proven_optimal":bool(result.success),
        "mip_gap":None if getattr(result,"mip_gap",None) is None else float(result.mip_gap)}
    if result.x is not None:
        bits=np.rint(result.x).astype(int)
        removed={A[i] for i in range(236) if bits[i]}
        added={p for j,p in enumerate(pool) if bits[236+j]}
        new_cap=(original-removed)|added
        assert verify(new_cap)==len(new_cap)
        answer.update({"removed":len(removed),"added":len(added),
            "net_change":len(added)-len(removed),
            "valid_cap_size":len(new_cap),
            "verified_by_independent_checker":True})
        assert abs((len(removed)-len(added))-float(result.fun))<1e-5
    return answer

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-secants",type=int,default=10)
    parser.add_argument("--min-additions",type=int,default=1)
    parser.add_argument("--time-limit",type=int,default=25)
    args=parser.parse_args()
    outcome=solve(args.max_secants,args.min_additions,args.time_limit)
    print(json.dumps(outcome,indent=2,sort_keys=True))
    if args.max_secants==10 and args.min_additions==1 and outcome["is_proven_optimal"]:
        assert outcome["valid_cap_size"]==227
