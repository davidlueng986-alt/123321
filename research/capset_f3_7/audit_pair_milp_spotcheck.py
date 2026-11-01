#!/usr/bin/env python3
"""Independent MILP spot-check of the pair-removal result (SciPy/HiGHS).

Checks a known min-16 example, plus 100 pseudorandom external point pairs.
All chosen sample pairs have an independently optimized integer vertex cover.
This does not alone prove the full 1,902,225-pair scan.
"""
import collections
import itertools
import random
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix
from generate_calderbank_fishburn import construction

def setup():
    points=construction()
    index={p:i for i,p in enumerate(points)}
    pairs=collections.defaultdict(list)
    for i,p in enumerate(points):
        for j in range(i+1,len(points)):
            q=points[j]
            r=tuple((-a-b)%3 for a,b in zip(p,q))
            pairs[r].append((i,j))
    return pairs,index

def optimize(p,q,pairs,index):
    required=index.get(tuple((-u-v)%3 for u,v in zip(p,q)))
    edges=pairs[p]+pairs[q]
    matrix=lil_matrix((len(edges),236),dtype=float)
    for k,(i,j) in enumerate(edges):
        matrix[k,i]=1
        matrix[k,j]=1
    low=np.zeros(236)
    if required is not None:
        low[required]=1
    result=milp(np.ones(236),integrality=np.ones(236),
                bounds=Bounds(low,np.ones(236)),
                constraints=LinearConstraint(matrix.tocsr(),np.ones(len(edges)),np.inf),
                options={"time_limit":10})
    if not result.success:
        raise RuntimeError(result.message)
    witness=np.rint(result.x).astype(int)
    assert np.all(witness>=low)
    assert all(witness[i]+witness[j]>=1 for i,j in edges)
    return int(sum(witness))

def main():
    pairs,index=setup()
    outsiders=sorted(pairs)
    a=(0,0,0,0,0,0,1)
    b=(0,0,0,0,0,1,0)
    assert optimize(a,b,pairs,index)==16
    rng=random.Random(20261102)
    samples=[tuple(rng.sample(outsiders,2)) for _ in range(100)]
    scores=[optimize(p,q,pairs,index) for p,q in samples]
    assert min(scores)>=16
    print("INDEPENDENT MILP CHECK PASSED: min-case=16, 100 seeded pairs, min(sample)=",min(scores),"max(sample)=",max(scores))

if __name__=="__main__":
    main()
