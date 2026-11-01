#!/usr/bin/env python3
"""Exhaustive signed-permutation cross-shadow restriction for C6 templates.

We fix C, the magic-basis 112-cap reconstructed from published 236-cap,
and take C' to be any signed coordinate permutation of either:
  (a) C itself, or
  (b) the only other 112-cap union of the verified order-240 orbits.
Each search reduces 46,080 signed permutations to 192 DISTINCT C'
sets (stabilizer order 240).

For (a), -(C+C') covers all 729 points in F3^6 for every C'.
For (b), 146/192 cover all 729, 46/192 leave exactly ONE point.
Consequently a 7D cap with first two 6D slices drawn from this
restricted family has size <=225 (112+112+1).
This DOES NOT exclude 236/237 from other GL6/affine transformations.
"""
import collections
import itertools
import json
from paley_magic_basis_240_certificate import basis,H,action,dot
from verify_capset import verify

def audit():
    C={tuple(dot(n,p) for n in basis) for p in H}
    assert verify(C,6)==112
    group=[]
    for P in itertools.permutations(range(6)):
        for mask in range(64):
            g=(P,mask)
            if all(action(x,g) in C for x in C):group.append(g)
    assert len(group)==240
    remaining=set(itertools.product(range(3),repeat=6))
    orbits=[]
    while remaining:
        x=min(remaining)
        O={action(x,g) for g in group}
        orbits.append(O);remaining-=O
    assert len(orbits)==13
    C_from_orbits=set().union(*[orbits[i] for i in (7,10,11)])
    assert C_from_orbits==C
    D=set().union(*[orbits[i] for i in (1,4,9)])
    assert verify(D,6)==112 and C.isdisjoint(D)
    space=set(itertools.product(range(3),repeat=6))
    results={}
    for name,base in (("same_C",C),("other_orbit_C",D)):
        transformed={}
        for P in itertools.permutations(range(6)):
            for mask in range(64):
                g=(P,mask)
                E=frozenset(action(x,g) for x in base)
                transformed.setdefault(E,g)
        assert len(transformed)==192
        freq=collections.Counter()
        for E,g in transformed.items():
            shadow={tuple((-u-v)%3 for u,v in zip(x,y)) for x in C for y in E}
            free=space-shadow
            freq[len(free)]+=1
            assert len(free)<=1
        results[name]=dict(sorted(freq.items()))
    assert results["same_C"]=={0:192}
    assert results["other_orbit_C"]=={0:146,1:46}
    return {
      "signed_permutation_group_size":46080,
      "stabilizer_order":240,
      "distinct_transformed_caps_per_template":192,
      "missing_third_slice_points_by_template":results,
      "maximum_lifted_seven_dimensional_size_in_family":225,
      "restriction":"fixed C and signed permutations of two orbit-invariant 112-cap templates; does not cover arbitrary GL(6,3) or affine twists"
    }

if __name__=="__main__":
    print(json.dumps(audit(),indent=2,sort_keys=True))
