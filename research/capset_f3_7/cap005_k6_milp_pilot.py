#!/usr/bin/env python3
"""Exploratory six-fiber MILP. INFEASIBLE is NOT an independently checked proof."""
import argparse, itertools, json, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix, vstack
from pathlib import Path
from verify_capset import read_points, verify
from cap005_k6_secant_matching_gate import fiber

GROUPS=((0,1,3,5,8,18),(0,1,3,7,8,18),(9,10,12,14,17,18))

def pilot(group, limit):
    P=read_points(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt')
    assert verify(P)==236
    Pset=set(P); mask=sum(1<<f for f in group)
    frozen={x for x in P if not (mask & (1<<fiber(x)))}
    outsiders=set(itertools.product(range(3),repeat=7))-Pset
    edges={x:[] for x in outsiders}
    for a,b in itertools.combinations(P,2):
        x=tuple((-u-v)%3 for u,v in zip(a,b))
        if x in edges:edges[x].append((1<<fiber(a))|(1<<fiber(b)))
    admissible=sorted(x for x in outsiders if (mask & (1<<fiber(x))) and all(mask&e for e in edges[x]))
    candidates=sorted((Pset-frozen)|set(admissible))
    var={x:i for i,x in enumerate(candidates)}
    total=Pset|set(admissible)
    constraints=set()
    for a,b in itertools.combinations(sorted(total),2):
        c=tuple((-u-v)%3 for u,v in zip(a,b))
        if c not in total:continue
        triple={a,b,c}
        inds=tuple(sorted(var[x] for x in triple if x in var))
        if inds:constraints.add((inds,2-sum(x in frozen for x in triple)))
    constraints=sorted(constraints)
    rr=[];cc=[]
    for i,(inds,_) in enumerate(constraints):
        for j in inds:rr.append(i);cc.append(j)
    A=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(constraints),len(candidates))).tocsr()
    A=vstack([A,coo_matrix(np.ones((1,len(candidates))))]).tocsr()
    lo=[-np.inf]*len(constraints)+[237-len(frozen)]
    hi=[b for _,b in constraints]+[np.inf]
    start=time.monotonic()
    res=milp(np.zeros(len(candidates)),integrality=np.ones(len(candidates)),bounds=Bounds(0,1),
             constraints=LinearConstraint(A,lo,hi),options={'time_limit':limit,'mip_rel_gap':0})
    result={'group':group,'frozen':len(frozen),'admissible_outsiders':len(admissible),
            'variables':len(candidates),'constraints':len(constraints),'solver_status':int(res.status),
            'solver_message':res.message,'elapsed_seconds':round(time.monotonic()-start,4),
            'proof_certificate':False}
    if res.x is not None:
        selected=frozen|{x for x,v in zip(candidates,res.x) if v>0.5}
        assert len(selected)>=237 and verify(sorted(selected))==len(selected)
        result['verified_witness']=[''.join(map(str,x)) for x in sorted(selected)]
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--time-limit',type=float,default=5.0);a=p.parse_args()
    print(json.dumps([pilot(g,a.time_limit) for g in GROUPS],sort_keys=True))
