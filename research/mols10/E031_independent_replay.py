#!/usr/bin/env python3
"""Independent direct checker: Latin/overlay, partial constraints, and CNF model replay."""
import json,sys,hashlib
sys.path.insert(0,'/mnt/data')
from E031_rowwise_5net import solve
from E031_direct_cnf import make,normalize,from_squares

def verify(S,n,complete=True):
    assert len(S)==3
    k=len(S[0]);assert all(len(A)==k for A in S)
    assert all(len(A[r])==n for A in S for r in range(k))
    pairs=[(0,1),(0,2),(1,2)]
    for A in S:
        for row in A:assert len(set(row))==n and set(row)==set(range(n))
        for c in range(n):assert len({A[r][c] for r in range(k)})==k
    ovs=[]
    for a,b in pairs:
        vals=[(S[a][r][c],S[b][r][c]) for r in range(k) for c in range(n)]
        assert len(set(vals))==len(vals)
        ovs.append(len(set(vals)))
    if complete:assert k==n and ovs==[n*n]*3
    assert all(S[s][0]==list(range(n)) for s in range(3))
    assert all(S[0][r][0]==r for r in range(k))
    return {'rows':k,'pair_counts':ovs}

out={'positive':[],'negative':[],'partial':[]}
for n in (2,3,4,5):
    d=solve(n,100000,4,hall=False)
    if d['status']=='SAT':
        verify(d['squares'],n)
        M=make(n)
        N=normalize(d['squares'])
        assert not from_squares(M,N)
        out['positive'].append({'n':n,'nodes':d['nodes'],'clauses':len(M['clauses']),
         'variables':M['vars'],'valid_cnf_witness':True,'overlays':[n*n]*3})
        # Deliberate corruption should be rejected both semantically and in CNF
        bad=[[r[:] for r in A] for A in N]
        bad[0][1][1]=bad[0][1][0]
        assert from_squares(M,bad)
        out['negative'].append({'n':n,'tampered_matrix':True})
    else:
        assert n in (2,3) and d['status']=='UNSAT_EXHAUSTIVE_NORMALIZED'
        out['negative'].append({'n':n,'status':d['status'],'nodes':d['nodes']})
# Separate LATIN-only negative case: duplicate the same order-10 Latin square
# from a complete public E027 fixed-Q mate listing; duplication destroys all
# pairwise orthogonality without violating a single Latin row or column.
q10=json.load(open('/mnt/data/E027_RESULTS.json'))['UW']['solutions'][0]['mate']
M=make(10); Z=normalize([q10,q10,q10])
fails=from_squares(M,Z)
assert len(fails)>0
out['negative'].append({'n':10,'duplicate_latin_squares':True,
                       'violated_cnf_clauses':len(fails),'type':'Latin-valid but overlay-invalid'})
# Independent order-ten partial row validity check: no assumptions of proximity to solution.
for seed in (0,1,2):
    for hall in (False,True):
        d=solve(10,50000,3,hall=hall,seed=seed)
        v=verify(d['partial_rows'],10,False) if d['partial_rows'] else None
        out['partial'].append({'seed':seed,'hall':hall,'status':d['status'],'nodes':d['nodes'],
          'deepest_completed_row':d['deepest_completed_row'],'verification':v,
          'hall_prunes':d['hall_prunes'],'seconds':d['seconds']})
open('/mnt/data/E031_REPLAY_RESULTS.json','w').write(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
