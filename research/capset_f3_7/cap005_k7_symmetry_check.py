#!/usr/bin/env python3
"""CAP-005K independent exact checker. Does NOT import CAP-005J's incidence
enumerator, rank/unrank, or CAP-005K generator. Checks 1665 representative
N(T) values by fresh F3 arithmetic, the complete orbit partition, and
the independently established total of 25,124 seven-fiber survivors.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from cap005_k6_symmetry_quotient import read_cap, generate_group, image

HERE = Path(__file__).resolve().parent
def fiber(p): return 9*p[0]+3*p[1]+p[2]
def third(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))

def check(cert_path,cap_path):
    B=read_cap(cap_path)
    maps=generate_group(B)
    outsiders=set(itertools.product(range(3),repeat=7))-B
    assert len(outsiders)==1951
    requirements={p:set() for p in outsiders}
    for a,b in itertools.combinations(sorted(B),2):
        z=third(a,b)
        assert z not in B
        fa,fb=fiber(a),fiber(b)
        if fa!=fb:requirements[z].add((min(fa,fb),max(fa,fb)))
    for x, pairs in requirements.items():
        used={fiber(x)}
        for a,b in pairs:
            assert a!=b and a not in used and b not in used
            used.update((a,b))
    data=json.loads(cert_path.read_text())
    assert data['group_order']==16 and data['original_survivors']==25124
    assert data['survivor_orbits']==1665 and len(data['representatives'])==1665
    covered=set()
    size_hist=Counter()
    N_hist=Counter()
    by_fiber=Counter(fiber(p) for p in B)
    for row in data['representatives']:
        T=tuple(row['fibers'])
        assert len(T)==7 and T==tuple(sorted(set(T))) and 0<=T[0]<T[-1]<27
        released=set(T)
        N=sum(1 for x,pairs in requirements.items()
              if fiber(x) in released and all(a in released or b in released for a,b in pairs))
        assert N>=17 and N==row['N'],(T,N,row['N'])
        assert row['baseline_occupancy']==sum(by_fiber[i] for i in T)
        orbit={image(T,g) for g in maps}
        assert len(orbit)==row['orbit_size']
        assert not covered.intersection(orbit),('overlapping orbit',T)
        covered.update(orbit)
        size_hist[len(orbit)]+=1
        N_hist[N]+=1
    assert len(covered)==25124
    assert dict(size_hist)=={4:3,8:185,16:1477}
    assert N_hist[198]==1 and N_hist[17]==37
    assert dict(data['orbit_size_histogram'])=={str(k):v for k,v in size_hist.items()}
    assert dict(data['N_orbit_histogram'])=={str(k):v for k,v in N_hist.items()}
    assert max(N_hist)==198 and sum(N_hist.values())==1665
    assert 862906+len(covered)==888030
    return {'status':'PASS_INDEPENDENT_EXACT_F3_REPRESENTATIVES',
            'survivor_orbits':1665,'covered_survivors':25124,
            'orbit_size_histogram':dict(size_hist),
            'max_N':198,'global_bound_improved':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    a=ap.parse_args()
    print(json.dumps(check(a.certificate,a.cap),sort_keys=True))
