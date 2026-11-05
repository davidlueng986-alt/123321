#!/usr/bin/env python3
"""CAP052 pure F3 structural checker. This does NOT solve r3(7).
Theorem A: a hypothetical 237-cap admits a dense-six-flat centre normal
form with 11 mandatory selected points and 7 antipodal pairs in H.
Theorem B: a 237-cap admits an ambient centre with >=15 secant pairs
and 12 mandatory points. Both give ONE root-complete decision instance.
"""
from itertools import combinations, product
from math import comb
import json

N=7
def basis(n):
    return [tuple(int(i==j) for i in range(n)) for j in range(n)]
def pack(p):
    x=0
    for a in p:x=3*x+a
    return x
def third(a,b):
    return tuple((-x-y)%3 for x,y in zip(a,b))
def canonical(v):
    v=tuple(v)
    if not any(v):return None
    return tuple(2*x%3 for x in v) if next(x for x in v if x)==2 else v
def pg2_arc_max4_check():
    pg=sorted({canonical(v) for v in product(range(3),repeat=3)}-{None})
    assert len(pg)==13
    lines=set()
    for a,b in combinations(pg,2):
        line=frozenset([a,b,canonical((x+y)%3 for x,y in zip(a,b)),
                       canonical((x-y)%3 for x,y in zip(a,b))])
        assert len(line)==4
        lines.add(line)
    assert len(lines)==13
    for p in combinations(pg,5):
        assert any(len(set(p)&line)>=3 for line in lines)
    return True
def fixed_summary(pair_rank,dense):
    E=basis(N)
    ones=E+[tuple(2*a%3 for a in E[i]) for i in range(pair_rank)]
    on={pack(x) for x in ones}
    zeros={pack(third(a,b)) for a,b in combinations(ones,2)}
    assert len(on)==7+pair_rank and on.isdisjoint(zeros) and 0 in zeros
    Hones=sum(p%3==0 for p in on)
    Hzeros=sum(p%3==0 for p in zeros)
    out={'mandatory_selected':len(on),'forced_zero':len(zeros),
         'free_points':3**7-len(on)-len(zeros),
         'selected_point_codes':sorted(on),'selected_H':Hones,
         'forced_zero_H':Hzeros,'free_H':729-Hones-Hzeros}
    return out
def verify():
    assert comb(89,2)>6*(729-89)
    assert comb(237,2)>14*(2187-237)
    assert pg2_arc_max4_check()
    assert 15*13>40*4  # 15 projective points cannot be a cap in PG(3,3)
    dense=fixed_summary(4,True)
    ambient=fixed_summary(5,False)
    assert (dense['mandatory_selected'],dense['forced_zero'],
            dense['free_points'],dense['selected_H'],
            dense['forced_zero_H'],dense['free_H'])==(11,52,2124,10,42,677)
    assert (ambient['mandatory_selected'],ambient['forced_zero'],
            ambient['free_points'])==(12,62,2113)
    return {'status':'ONLY_NORMAL_FORM_PROOFS_NOT_ROOT_CLOSURE',
            'dense_89_secant_center_min_pairs':7,
            'global_237_secant_center_min_pairs':15,
            'dense_single_case':dense,
            'global_single_case':ambient,
            'sat_status':'UNKNOWN'}
if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True))
