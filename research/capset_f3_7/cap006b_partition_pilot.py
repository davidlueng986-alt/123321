#!/usr/bin/env python3
"""CAP-006B: matched, bounded 8-fiber outsider NECESSARY-gate pilot.
Different affine partitions, same 320 random 8-subsets, fixed seed 20261102.
N(T) is NOT mutually compatible outsiders and is NOT a cap witness.
"""
from itertools import combinations,product
from collections import Counter
from random import Random
import json
from cap006_projection_audit import read_cap

def baseline():
    B=set(read_cap())
    assert len(B)==236
    return B

def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
def project(p,M):return tuple(sum(x*y for x,y in zip(r,p))%3 for r in M)
def fiber(p,M):
    a,b,c=project(p,M)
    return 9*a+3*b+c

MATS={
 'base_012':[[1,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,1,0,0,0,0]],
 'low_Q2096':[[0,0,0,2,1,1,2],[2,0,1,2,1,1,1],[1,1,0,1,0,0,0]],
 'high_Q3186':[[1,2,2,1,2,1,2],[1,0,0,1,1,1,0],[0,0,0,2,2,2,0]]}

def build(B,M):
    f={p:fiber(p,M) for p in product(range(3),repeat=7)}
    occ=Counter(f[p] for p in B)
    O=sorted(set(f)-B)
    needs={p:[] for p in O}
    for a,b in combinations(sorted(B),2):
        z=third(a,b)
        assert z not in B
        needs[z].append((1<<f[a])|(1<<f[b]))
    bits={p:1<<f[p] for p in O}
    return occ,O,needs,bits

def eligible(T,occ,O,needs,bits):
    mask=sum(1<<i for i in T)
    count=sum(bool(mask&bits[p]) and all(mask&z for z in needs[p]) for p in O)
    old=sum(occ[i] for i in T)
    return {'T':list(T),'N_admissible':count,'released_old':old,
            'naive_gain_ceiling':count-old}

def result():
    B=baseline()
    assert all(third(a,b) not in B for a,b in combinations(sorted(B),2))
    rng=Random(20261102)
    sets=set()
    while len(sets)<320:
        sets.add(tuple(sorted(rng.sample(range(27),8))))
    samples=sorted(sets)
    out={}
    for name,M in MATS.items():
        occ,O,needs,bits=build(B,M)
        values=[eligible(T,occ,O,needs,bits) for T in samples]
        values.sort(key=lambda t:(-t['naive_gain_ceiling'],-t['N_admissible'],t['T']))
        out[name]={
            'Q':sum(occ[i]**2 for i in range(27)),
            'seed':20261102,'samples':320,
            'N_at_least17':sum(v['N_admissible']>=17 for v in values),
            'naive_margin_positive':sum(v['naive_gain_ceiling']>0 for v in values),
            'max_N':max(v['N_admissible'] for v in values),
            'max_naive_margin':max(v['naive_gain_ceiling'] for v in values),
            'mean_N':sum(v['N_admissible'] for v in values)/len(values),
            'top3_by_naive_margin':values[:3]
        }
    assert [out[k]['max_N'] for k in ('base_012','low_Q2096','high_Q3186')]==[124,2,45]
    assert [out[k]['N_at_least17'] for k in ('base_012','low_Q2096','high_Q3186')]==[37,0,19]
    return {'experiment':'CAP-006B','scope':'320 matched 8-fiber necessary tests only',
            'fixed_seed':20261102,'results':out,'global_bound_improved':False,
            'new_cap_witness_found':False}

if __name__=='__main__':
    print(json.dumps(result(),sort_keys=True))
