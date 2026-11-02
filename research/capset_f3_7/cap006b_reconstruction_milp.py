#!/usr/bin/env python3
"""CAP-006B exploratory exact 8-fiber 0/1 formulation (HiGHS CPU).
Optimizer 'optimal' status is NOT a self-contained independently checkable
proof certificate. Always direct-check any returned point set in F3.
"""
from itertools import combinations,product
import argparse,json
from cap006b_partition_pilot import baseline,third,fiber,MATS

DEFAULT_T=(0,1,5,6,8,11,18,19)

def run(T=DEFAULT_T,seconds=12.):
    import numpy as np
    from scipy.optimize import milp,linprog,Bounds,LinearConstraint
    from scipy.sparse import csr_matrix
    B=baseline();R=set(T);M=MATS['base_012']
    fixed={p for p in B if fiber(p,M) not in R}
    old=sorted(B-fixed)
    outsiders=[p for p in product(range(3),repeat=7) if p not in B and fiber(p,M) in R]
    E=[p for p in outsiders if all(third(a,b)!=p for a,b in combinations(sorted(fixed),2))]
    V=sorted(set(old)|set(E));index={p:i for i,p in enumerate(V)}
    constraints=[]
    for i,a in enumerate(V):
        for j in range(i+1,len(V)):
            z=third(a,V[j])
            if z in fixed:constraints.append(((i,j),1))
            elif z in index and index[z]>j:constraints.append(((i,j,index[z]),2))
    rows=[r for r,(t,rhs) in enumerate(constraints) for _ in t]
    cols=[i for t,rhs in constraints for i in t]
    mat=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(constraints),len(V)))
    rhs=np.array([r for t,r in constraints],dtype=float)
    lp=linprog(c=-np.ones(len(V)),A_ub=mat,b_ub=rhs,bounds=(0,1),method='highs')
    r=milp(c=-np.ones(len(V)),integrality=np.ones(len(V)),
           bounds=Bounds(np.zeros(len(V)),np.ones(len(V))),
           constraints=LinearConstraint(mat,-np.inf,rhs),
           options={'time_limit':seconds,'mip_rel_gap':0.})
    out={'T':list(T),'fixed':len(fixed),'old_release':len(old),'admissible':len(E),
         'variables':len(V),'line_constraints':len(constraints),
         'lp_upper_bound':(-lp.fun if lp.success else None),'solver_status':int(r.status),
         'solver_message':r.message,'solver_dual_bound':r.mip_dual_bound if hasattr(r,'mip_dual_bound') else None,
         'scope':'fixed eight-fiber region ONLY, no independent optimality certificate'}
    if r.x is not None:
        chosen={p for p,x in zip(V,r.x) if x>0.5}
        S=fixed|chosen
        out['candidate_total']=len(S)
        out['candidate_independently_checked']=all(third(a,b) not in S for a,b in combinations(sorted(S),2))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=12.)
    a=p.parse_args();print(json.dumps(run(seconds=a.seconds),sort_keys=True))
