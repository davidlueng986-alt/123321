#!/usr/bin/env python3
"""E029: complete fixed-Q mate enumeration for Egan-Wanless B and C.
Run from research/mols10: python E029_Egan_BC_fixed_Q.py
Depends on the two independent exact-cover engines E027 and independent
10! permutation replay E028. Scope: TWO SPECIFIC Q matrices only.
"""
import json, hashlib, time
import E027_fixed_Q_exhaustive as primary
import E027_dlx_independent as independent
from E028_SX_UU_fixed_Q import permutation_common

def canon(a):
    ren = {a[0][c]:c for c in range(10)}
    return [[ren[a[r][c]] for c in range(10)] for r in range(10)]

def construct_p(a,q):
    # derive(P,Q)[r,c] = inverse(P[:,c])[Q[r,c]] = A[r,c].
    # P is Latin because A and Q are orthogonal.
    p = [[-1]*10 for _ in range(10)]
    for r in range(10):
        for c in range(10):
            p[a[r][c]][c] = q[r][c]
    assert primary.latin(p) and primary.derive(p,q)==a
    return p

def run(label,a,q):
    assert primary.latin(a) and primary.latin(q)
    assert len({(a[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
    p=construct_p(a,q)
    raw=lambda m:' '.join(''.join(map(str,row)) for row in m)
    primary.RAW[label]=[raw(p),raw(q)]
    independent.RAW[label]=[raw(p),raw(q)]
    first=primary.solve(label)
    second=independent.solve(label)
    encode=lambda m:json.dumps(m,separators=(',',':'))
    assert first['complete'] and second['complete']
    assert first['q_transversals']==second['q_transversals']
    assert sorted(encode(x['mate']) for x in first['solutions'])==sorted(map(encode,second['mates']))
    assert sum(x['mate']==canon(a) for x in first['solutions'])==1
    witnesses=[]
    for x in first['solutions']:
        m=x['mate']
        assert primary.latin(m)
        assert len({(m[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
        cnt,support=permutation_common(m,q)  # independent full 10! enumeration
        assert (cnt,support)==(x['common_transversals'],x['common_cell_support'])
        witnesses.append({'mate':m,'common_transversals':cnt,'support':support})
    return {'fixed_Q':label,'q_sha256':hashlib.sha256(encode(q).encode()).hexdigest(),
      'q_transversals':first['q_transversals'],'normalized_mates':len(witnesses),
      'bitset_nodes':first['dfs_nodes'],'independent_nodes':second['nodes'],
      'full_permutation_tests':len(witnesses)*3628800,
      'all_mates':witnesses,'complete':True,'global_solution':False}

if __name__=='__main__':
    with open('near_triple.json',encoding='utf8') as f: a,b,c=json.load(f)['squares']
    start=time.monotonic()
    results={name:run(name,a,q) for name,q in [('B',b),('C',c)]}
    results['elapsed_s']=round(time.monotonic()-start,3)
    print(json.dumps(results,indent=2))
