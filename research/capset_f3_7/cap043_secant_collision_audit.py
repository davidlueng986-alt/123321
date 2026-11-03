#!/usr/bin/env python3
"""CAP043: independent affine-frame secant collision census (CPU only)."""
from collections import defaultdict
from itertools import combinations
N=3**7
def digits(n):
    out=[]
    for _ in range(7):
        out.append(n%3); n//=3
    return out
def encode(v): return sum(x*3**i for i,x in enumerate(v))
def third(a,b):
    return encode([(-x-y)%3 for x,y in zip(digits(a),digits(b))])
def run():
    frame=[0]+[3**i for i in range(7)]
    excluded=set(frame)|{third(a,b) for a,b in combinations(frame,2)}
    groups=defaultdict(list)
    for p in range(N):
        if digits(p)[6] or p in excluded: continue
        d=digits(p)
        lam=[(1-sum(d))%3]+d
        key=(lam[7],lam[:7].count(0),lam[:7].count(1),lam[:7].count(2))
        groups[key].append(p)
    assert len(groups)==10 and sum(map(len,groups.values()))==701
    counts=[]; anomalies=[]
    for branch,(tag,pts) in enumerate(sorted(groups.items())):
        chosen=frame+[pts[0]]
        fibers=defaultdict(list)
        for a,b in combinations(chosen,2):
            fibers[third(a,b)].append((a,b))
        duplicates={z:pairs for z,pairs in fibers.items() if len(pairs)>1}
        counts.append(len(fibers))
        if duplicates: anomalies.append((branch,pts[0],duplicates))
    assert counts==[36]*9+[35],counts
    assert anomalies==[(9,4,{8:[(0,4),(1,3)]})],anomalies
    print({'orbits':len(groups),'eligible_ninth':701,'forced_zero_counts':counts,
           'unique_collision':anomalies[0], 'seed':None})
if __name__=='__main__': run()
