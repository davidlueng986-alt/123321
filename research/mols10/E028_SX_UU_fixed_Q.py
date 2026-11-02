#!/usr/bin/env python3
"""E028 complete fixed-Q orthogonal-mate audit for BKS Appendix SX/UU.
Run from research/mols10: python E028_SX_UU_fixed_Q.py
Uses two independently implemented exact-cover backends from E027 and
an independent exhaustive 10! common-transversal checker.
Scope: these two published Q matrices only, NOT their whole families.
"""
import hashlib,itertools,json,time
import E027_fixed_Q_exhaustive as primary
import E027_dlx_independent as independent
from E023_SX_pair_replay import P as SX_P,Q as SX_Q
from E023_UU_pair_replay import P as UU_P,Q as UU_Q

def canon(z):
    relabel={z[0][c]:c for c in range(10)}
    return [[relabel[z[r][c]] for c in range(10)] for r in range(10)]

def permutation_common(a,q):
    count=0;support=0;tested=0
    for t in itertools.permutations(range(10)):
        tested+=1;ma=mq=0
        for r,c in enumerate(t):
            ba=1<<a[r][c];bq=1<<q[r][c]
            if ma&ba or mq&bq:break
            ma|=ba;mq|=bq
        else:
            count+=1
            for r,c in enumerate(t):support|=1<<(10*r+c)
    assert tested==3628800
    return count,support.bit_count()

def run(label,p,q):
    assert primary.latin(p) and primary.latin(q)
    original=primary.derive(p,q)
    assert primary.latin(original)
    assert len({(original[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
    rows=lambda m:' '.join(''.join(str(x) for x in row) for row in m)
    primary.RAW[label]=[rows(p),rows(q)]
    independent.RAW[label]=[rows(p),rows(q)]
    start=time.monotonic()
    a=primary.solve(label)
    b=independent.solve(label)
    key=lambda m:json.dumps(m,separators=(',',':'))
    assert a['q_transversals']==b['q_transversals']
    assert sorted(map(key,(x['mate'] for x in a['solutions'])))==sorted(map(key,b['mates']))
    assert sum(x['mate']==canon(original) for x in a['solutions'])==1
    replay=[]
    for x in a['solutions']:
        mate=x['mate']
        assert primary.latin(mate)
        assert len({(mate[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
        n,support=permutation_common(mate,q)
        assert (n,support)==(x['common_transversals'],x['common_cell_support'])
        replay.append({'mate':mate,'common_transversals':n,'support':support})
    return {'q_sha256':hashlib.sha256(key(q).encode()).hexdigest(),
            'q_transversals':a['q_transversals'],'partitions':len(replay),
            'bitset_nodes':a['dfs_nodes'],'independent_nodes':b['nodes'],
            'published_mate_recovered':True,'independent_mates_identical':True,
            'all_mates':replay,'permutation_tests':len(replay)*3628800,
            'complete_fixed_Q':True,'elapsed_s':round(time.monotonic()-start,3)}

if __name__=='__main__':
    print(json.dumps({'SX':run('SX',SX_P,SX_Q),'UU':run('UU',UU_P,UU_Q)},indent=2))
