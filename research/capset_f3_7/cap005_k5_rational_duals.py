#!/usr/bin/env python3
"""CAP-005C: rationally checked LP duals for all 5-fiber release sets.

SciPy/HiGHS proposes floating-point duals. Every claimed upper bound is
rechecked using exact fractions; numerical optimizer status alone proves nothing.
"""
import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from verify_capset import read_points, verify

HERE = Path(__file__).resolve().parent

def fiber(p):
    return 9*p[0] + 3*p[1] + p[2]

def certify():
    points = read_points(HERE/"candidates"/"calderbank_fishburn_236.txt")
    assert verify(points) == 236
    original = set(points)
    outsiders = set(itertools.product(range(3),repeat=7)) - original
    assert len(outsiders)==1951
    edges = {x:set() for x in outsiders}
    secants = Counter()
    for a,b in itertools.combinations(points,2):
        x=tuple((-a[i]-b[i])%3 for i in range(7))
        if x in edges:
            edges[x].add((1<<fiber(a))|(1<<fiber(b)))
            secants[x]+=1
    assert len(secants)==1951 and min(secants.values())==10
    by=[[] for _ in range(27)]
    for x,es in edges.items():
        by[fiber(x)].append((x,tuple(es)))
    histogram=Counter()
    certs=[]
    for group in itertools.combinations(range(27),5):
        mask=sum(1<<j for j in group)
        admissible=[x for j in group for x,es in by[j] if all(e&mask for e in es)]
        histogram[len(admissible)]+=1
        if len(admissible)<10:
            # Any outsider requires >=10 deletions; fewer than 10 additions
            # cannot improve 236. No LP necessary.
            continue
        released=set(group)
        frozen={x for x in points if fiber(x) not in released}
        candidates=sorted({x for x in points if fiber(x) in released}|set(admissible))
        variable={x:i for i,x in enumerate(candidates)}
        total=frozen|set(candidates)
        constraints=set()
        for a,b in itertools.combinations(sorted(total),2):
            c=tuple((-u-v)%3 for u,v in zip(a,b))
            if c not in total:
                continue
            triple={a,b,c}
            indices=tuple(sorted(variable[x] for x in triple if x in variable))
            rhs=2-sum(x in frozen for x in triple)
            assert rhs>=0  # the frozen portion is a cap
            if indices:
                constraints.add((indices,rhs))
        constraints=sorted(constraints)
        n=len(candidates)
        A=lil_matrix((len(constraints),n),dtype=float)
        rhs=np.empty(len(constraints))
        for i,(indices,b) in enumerate(constraints):
            for j in indices:
                A[i,j]=1
            rhs[i]=b
        # Maximize number of selected candidate points (minimize its negative).
        lp=linprog(-np.ones(n),A_ub=A.tocsr(),b_ub=rhs,
                   bounds=(0,1),method="highs")
        if lp.status!=0:
            raise AssertionError(("LP not optimal; inconclusive",group,lp.message))
        y=[Fraction(float(-v)).limit_denominator(1000)
           for v in lp.ineqlin.marginals]
        z=[Fraction(float(-v)).limit_denominator(1000)
           for v in lp.upper.marginals]
        # This exact rational certificate is independent of floating-point
        # optimality: y>=0, z>=0, A^T*y+z>=1, rhs^T*y+sum(z)<=
        # original points in the five released fibers.
        assert all(v>=0 for v in y) and all(v>=0 for v in z)
        coverage=list(z)
        for (indices,_),yi in zip(constraints,y):
            for j in indices:
                coverage[j]+=yi
        assert all(v>=1 for v in coverage),(group,min(coverage))
        original_released=236-len(frozen)
        dual_bound=sum(yi*b for yi,(_,b) in zip(y,constraints))+sum(z)
        assert dual_bound<=original_released,(group,dual_bound,original_released)
        def encode(q):
            return [q.numerator,q.denominator]
        certs.append({
            "released_fibers":list(group),
            "original_released":original_released,
            "admissible_outsiders":len(admissible),
            "dual_bound":encode(dual_bound),
            "constraints":len(constraints),
            "nonzero_row_duals":[[i,*encode(v)] for i,v in enumerate(y) if v],
            "nonzero_upper_duals":[[i,*encode(v)] for i,v in enumerate(z) if v],
        })
    expected={0:44392,1:25872,2:5384,3:344,4:1434,5:1576,
              6:1136,7:152,9:128,10:152,11:32,12:16,13:32,
              14:40,15:16,18:8,20:8,22:8}
    assert dict(histogram)==expected,(histogram,expected)
    assert len(certs)==312
    return {"status":"EXACT_RATIONAL_DUALS_CERTIFY_NO_FIVE_FIBER_IMPROVEMENT",
            "baseline_size":236,"release_sets":80730,
            "small_outsider_gate_sets":80730-312,
            "rational_dual_certificates":len(certs),
            "max_admissible_outsiders":22,
            "scope":"Only five first-three-coordinate F3^4 fibers; not global",
            "certificates":certs}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    result=certify()
    if args.out:
        args.out.write_text(json.dumps(result,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="certificates"},sort_keys=True))
