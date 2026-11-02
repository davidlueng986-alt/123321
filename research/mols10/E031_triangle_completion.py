#!/usr/bin/env python3
"""Triple-wise residual triangle exact-cover necessary condition for partial 3-MOLS.
For each pair (AB,AC,BC), uncovered ordered symbol pairs must be covered
exactly once by hypothetical remaining cell triples (a,b,c).
This deliberately IGNORES rows and columns; FEASIBLE is only necessary.
Solver-complete INFEASIBLE excludes the fixed partial state, not n=10 globally.
"""
import numpy as np, scipy.optimize as opt, scipy.sparse as sp
P=((0,1),(0,2),(1,2))
def analyse(S,n,mode='milp',max_seconds=2):
    k=len(S[0]);assert len(S)==3 and all(len(A)==k for A in S)
    used=[set() for _ in range(3)]
    for p,(s,t) in enumerate(P):
        for r in range(k):
            for col in range(n):
                tup=(S[s][r][col],S[t][r][col]);assert tup not in used[p]
                used[p].add(tup)
    rem=[[(a,b) for a in range(n) for b in range(n) if (a,b) not in used[p]] for p in range(3)]
    f=[set(z) for z in rem]
    candidates=[(a,b,c) for a,b in rem[0] for c in range(n) if (a,c) in f[1] and (b,c) in f[2]]
    support=[set(),set(),set()]
    for a,b,c in candidates:
        support[0].add((a,b));support[1].add((a,c));support[2].add((b,c))
    deficits=[len(f[p]-support[p]) for p in range(3)]
    result={'n':n,'fixed_rows':k,'remaining_pair_counts':list(map(len,rem)),
        'candidate_triples':len(candidates),'unsupported_pairs':deficits}
    if not rem[0]:result['status']='COMPLETE_NO_REMAINING_PAIRS';return result
    if any(deficits):result['status']='INFEASIBLE_BY_SUPPORT';return result
    if mode=='support':result['status']='SUPPORT_ONLY';return result
    index={ (p,z):i for p in range(3) for i,z in [] }
    # separate index per pair block
    offsets=[0,len(rem[0]),len(rem[0])+len(rem[1])]
    for p in range(3):
        for i,z in enumerate(rem[p]):index[p,z]=offsets[p]+i
    I=[];J=[]
    for j,(a,b,c) in enumerate(candidates):
        for p,z in enumerate(((a,b),(a,c),(b,c))):I.append(index[p,z]);J.append(j)
    A=sp.coo_matrix((np.ones(len(I)),(I,J)),shape=(sum(map(len,rem)),len(candidates))).tocsr()
    bounds=opt.Bounds(0,1)
    res=opt.milp(np.zeros(len(candidates)),integrality=np.ones(len(candidates)),bounds=bounds,
          constraints=opt.LinearConstraint(A,1,1), options={'time_limit':max_seconds,'mip_rel_gap':0.0})
    result.update({'solver_status':int(res.status),'solver_message':str(res.message),
                   'status':'FEASIBLE_RELAXED' if res.status==0 and res.x is not None
                      else 'INFEASIBLE_SOLVER_COMPLETE_NO_EXTERNAL_CERT' if res.status==2 else 'UNKNOWN',
                   'constraint_count':A.shape[0],'variable_count':A.shape[1],
                   'node_count':getattr(res,'mip_node_count',None)})
    if result['status']=='FEASIBLE_RELAXED':
        chosen=[candidates[i] for i,z in enumerate(res.x) if z>0.5]
        assert len(chosen)==n*(n-k)
        assert all(len(set((v[x],v[y]) for v in chosen))==n*(n-k) for x,y in P)
        result['validated_assignment']=len(chosen)
    return result

if __name__=='__main__':
    import sys,json
    sys.path.insert(0,'/mnt/data')
    from E031_rowwise_5net import solve
    out=[]
    for n in (4,5,6,10):
        for seed in (0,1,2):
            x=solve(n,100000,2,seed=seed,hall=False)
            S=x['partial_rows']
            if S:
                out.append({'seed':seed,'search':{k:v for k,v in x.items() if k not in ('squares','partial_rows')},
                            'triangle':analyse(S,n,max_seconds=3)})
    print(json.dumps(out,indent=2))
