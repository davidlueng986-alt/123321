#!/usr/bin/env python3
"""CAP-010A: exact 112-cap secant-cover and 110/111 completion certificate.

Pure Python stdlib. Global 110/111 deductions require:
Potechin (2008) affine uniqueness of 112-caps, and
Thackeray (2022, arXiv:2206.09804) extension of every 110-cap to 112.
No claim of r3(7) exact value or literature novelty.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse,json
from cap007j_112_alignment import read_fixture,third,encode,V

def certificate(fixture=None,exhaustive=False):
    fixture=fixture or Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'
    S,_,_=read_fixture(fixture)
    assert len(S)==112 and len(set(S))==112
    ids={encode(p) for p in S}
    assert all(third(a,b) not in ids for a,b in []) # explicit full check below
    assert all(encode(third(a,b)) not in ids for a,b in combinations(S,2))
    edges={i:[] for i in range(729) if i not in ids}
    for i,j in combinations(range(112),2):
        z=encode(third(S[i],S[j]))
        assert z in edges
        edges[z].append((1<<i)|(1<<j))
    hist=Counter(len(x) for x in edges.values())
    assert hist==Counter({10:616,56:1}),hist
    assert sum(map(len,edges.values()))==6216
    # Independent graph-theoretic audit: each edge family is a matching.
    for z,E in edges.items():
        used=0
        for e in E:
            assert e.bit_count()==2 and not used&e
            used|=e
    count=0
    if exhaustive:
        # All 6216 pairs removed; for every external point test whether
        # at least one of three disjoint original secants survives.
        # Three edges suffice since deletion of two vertices hits <=2 edges.
        triples=[E[:3] for E in edges.values()]
        for i,j in combinations(range(112),2):
            removed=(1<<i)|(1<<j)
            assert all(any(e&removed==0 for e in E) for E in triples)
            count+=1
        assert count==6216
    return {'canonical_112_verified':True,
            'outside_secants_histogram':dict(sorted(hist.items())),
            'outside_points':len(edges),'total_secants':6216,
            'disjoint_secants_per_external_point_minimum':10,
            'removed_pair_completions_exhaustively_checked':count,
            'universal_corollary':'All 110-caps have exactly two one-point extensions and a unique 112-cap completion; all 111-caps extend uniquely to a 112-cap (conditional on published 110 classification and 112 affine uniqueness).',
            'unique_completion_for_subsets_of_maximal_112_when_removed_at_most':9,
            'novelty':'NOT ESTABLISHED',
            'r3_7_exact_status':'OPEN'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--exhaustive',action='store_true')
    a=p.parse_args()
    print(json.dumps(certificate(exhaustive=a.exhaustive),sort_keys=True))
