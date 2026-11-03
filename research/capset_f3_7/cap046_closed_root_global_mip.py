#!/usr/bin/env python3
"""CAP046: direct ROOT-complete n=7 target237 MILP feasibility attempt.

Sound WLOG: standard eight affine-frame vertices, their 28 forbidden
secants, and one 6D hyperplane (coordinate 7 = 0) containing >=89 points,
by CAP007J moments and r3(5)=45. These hypotheses are GLOBAL for any
hypothetical 237 cap, unlike fixed-285 occupancy experiments.
SciPy HiGHS is NOT an independently proof-logging UNSAT solver.
TIMEOUT/interrupt -> UNKNOWN. No GPU/paid compute.
"""
import json,time,argparse,os
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,vstack

def check(points,third):
    chosen=set(points)
    return len(chosen)==len(points) and all(int(third[x,y]) not in chosen
             for i,x in enumerate(points) for y in points[i+1:])

def run(seconds=17):
    start=time.perf_counter()
    n=2187
    pow3=np.array([729,243,81,27,9,3,1],dtype=np.int16)
    v=np.array([[(i//int(k))%3 for k in pow3] for i in range(n)],dtype=np.int16)
    t=((-(v[:,None,:]+v[None,:,:]))%3@pow3).astype(np.int16)
    edges=np.empty((796797,3),dtype=np.int32)
    end=0
    for a in range(n):
        ys=np.arange(a+1,n,dtype=np.int32)
        zs=t[a,ys];mask=ys<zs;count=int(mask.sum())
        edges[end:end+count,0]=a;edges[end:end+count,1]=ys[mask]
        edges[end:end+count,2]=zs[mask];end+=count
    assert end==796797
    row=np.repeat(np.arange(end,dtype=np.int32),3)
    col=edges.ravel()
    line_matrix=csr_matrix((np.ones(len(col)),(row,col)),shape=(end,n))
    H=[i for i in range(n) if i%3==0]
    low=np.zeros(n);up=np.ones(n)
    frame=[0,729,243,81,27,9,3,1]
    banned={int(t[a,b]) for i,a in enumerate(frame) for b in frame[i+1:]}
    assert len(banned)==28 and not(banned&set(frame))
    for i in frame:low[i]=up[i]=1
    for i in banned:low[i]=up[i]=0
    hrow=csr_matrix((np.ones(len(H)),(np.zeros(len(H),dtype=int),H)),shape=(1,n))
    M=vstack([line_matrix,csr_matrix(np.ones((1,n))),hrow],format='csr')
    lower=np.full(end+2,-np.inf);upper=np.full(end+2,2.)
    lower[-2:]=[237.,89.];upper[-2:]=np.inf
    print(json.dumps({'phase':'prepared','n':n,'line_clauses':end,
       'MIP_rows':M.shape[0],'nonzeros':M.nnz,'frame_selected':8,
       'frame_secant_zeros':len(banned),
       'build_seconds':round(time.perf_counter()-start,3)}),flush=True)
    st=time.perf_counter()
    sol=milp(c=np.zeros(n),integrality=np.ones(n),bounds=Bounds(low,up),
        constraints=LinearConstraint(M,lower,upper),
        options={'time_limit':seconds,'presolve':True})
    out={'phase':'returned','status':int(sol.status),
         'message':sol.message,'solve_seconds':round(time.perf_counter()-st,3),
         'ROOT':True,'conclusion':'UNKNOWN'}
    if sol.x is not None:
        picked=[i for i,x in enumerate(sol.x) if x>0.5]
        valid=check(picked,t)
        out['candidate_size']=len(picked)
        out['candidate_independently_checked']=valid
        out['dense_H_count']=sum(i in H for i in picked)
        if valid and len(picked)>=237 and out['dense_H_count']>=89:
            out['conclusion']='SAT_WITNESS_INDEPENDENTLY_CHECKED'
            out['points']=[''.join(str(x) for x in v[i]) for i in picked]
    # Important: even a solver INFEASIBLE status is NOT an independently
    # checked UNSAT proof. This script intentionally does not promote it.
    print(json.dumps(out,sort_keys=True),flush=True)
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=17.)
    args=ap.parse_args();run(args.seconds)
