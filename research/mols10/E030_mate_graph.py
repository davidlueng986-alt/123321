#!/usr/bin/env python3
"""E030: pairwise mate-compatibility graph for ten SPECIFIC fixed-Q matrices.
Recompute from repo: cd research/mols10 && python E030_mate_graph.py
Only fixed-Q exclusion, not unrestricted 3-MOLS(10).
"""
import json
from itertools import combinations
def overlay(A,B):
    return len({(A[r][c],B[r][c]) for r in range(10) for c in range(10)})
def latin(A):
    return len(A)==10 and all(sorted(row)==list(range(10)) for row in A) and all(sorted(A[r][c] for r in range(10))==list(range(10)) for c in range(10))
def analyze(mates):
    assert all(latin(a) for a in mates)
    edges=[{'i':i,'j':j,'overlay':overlay(mates[i],mates[j])} for i,j in combinations(range(len(mates)),2)]
    return {'mates':len(mates),'tested_pairs':len(edges),'max_overlay':max((x['overlay'] for x in edges),default=None),'orthogonal_mate_edges':sum(x['overlay']==100 for x in edges),'edges':edges}
def recompute():
    from E027_fixed_Q_exhaustive import RAW,solve,latin as source_latin
    from E023_SX_pair_replay import P as sx_p,Q as sx_q
    from E023_UU_pair_replay import P as uu_p,Q as uu_q
    cases={k:[x['mate'] for x in solve(k)['solutions']] for k in ['UW','UX','VX','WW','WX','XX']}
    raw=lambda M:' '.join(''.join(map(str,row)) for row in M)
    for k,p,q in [('SX',sx_p,sx_q),('UU',uu_p,uu_q)]:
        RAW[k]=[raw(p),raw(q)]
        cases[k]=[x['mate'] for x in solve(k)['solutions']]
    with open('near_triple.json',encoding='utf8') as f:
        a,b,c=json.load(f)['squares']
    for k,q in [('Egan_B',b),('Egan_C',c)]:
        assert source_latin(a) and source_latin(q) and overlay(a,q)==100
        p=[[-1]*10 for _ in range(10)]
        for r in range(10):
            for col in range(10):p[a[r][col]][col]=q[r][col]
        assert source_latin(p)
        RAW[k]=[raw(p),raw(q)]
        cases[k]=[x['mate'] for x in solve(k)['solutions']]
    return cases
def run():
    result={k:analyze(v) for k,v in recompute().items()}
    return {'scope':'ten specified fixed Q matrices only','cases':result,'total_mates':sum(x['mates'] for x in result.values()),'total_pair_tests':sum(x['tested_pairs'] for x in result.values()),'total_orthogonal_edges':sum(x['orthogonal_mate_edges'] for x in result.values())}
if __name__=='__main__':print(json.dumps(run(),indent=2))
