#!/usr/bin/env python3
"""Exact signed-permutation search around Calderbank–Fishburn 236-cap.

Use C = transformed first 112-point six-dimensional slice, and H'
= transformed second 112-point six-dimensional slice. Enumerate all
6!*2^6 = 46,080 signed coordinate permutations of H', deduplicating
into 1,920 distinct images. Exactly ten images allow a third slice of
12 points, each a cap; all others leave zero free points. Thus this
restricted two-112-slice family cannot yield 237 or more.

This is an exact combinatorial FINITE-FAMILY exclusion, NOT a general
upper bound on r3(7); arbitrary GL(6,3) affine transformations remain.
"""
import collections
import itertools
import json
from generate_calderbank_fishburn import construction
from paley_magic_basis_240_certificate import basis,dot,action
from verify_capset import verify

def audit():
    old=construction()
    C={tuple(dot(n,p[1:]) for n in basis) for p in old if p[0]==0}
    D={tuple(dot(n,p[1:]) for n in basis) for p in old if p[0]==1}
    assert verify(C,6)==verify(D,6)==112
    unique={}
    for P in itertools.permutations(range(6)):
        for mask in range(64):
            g=(P,mask)
            B=frozenset(action(p,g) for p in D)
            unique.setdefault(B,g)
    assert len(unique)==1920

    space=list(itertools.product(range(3),repeat=6))
    index={p:i for i,p in enumerate(space)}
    thirds=[[index[tuple((-a-b)%3 for a,b in zip(x,y))]
             for y in space] for x in space]
    Cids=[index[p] for p in C]
    bins=collections.Counter()
    exemplar=None
    for B,g in unique.items():
        Dids=[index[p] for p in B]
        hit=bytearray(729)
        for a in Cids:
            row=thirds[a]
            for b in Dids:hit[row[b]]=1
        unblocked={space[i] for i in range(729) if hit[i]==0}
        bins[len(unblocked)]+=1
        assert len(unblocked) in (0,12)
        if unblocked:
            assert verify(unblocked,6)==12
            lifted={ (0,)+p for p in C }|{ (1,)+p for p in B }|{ (2,)+p for p in unblocked }
            assert verify(lifted,7)==236
            if exemplar is None:exemplar={"signed_permutation":[list(g[0]),g[1]],"third_slice":sorted(unblocked)}
    assert bins=={0:1910,12:10}
    return {
      "signed_coordinate_permutations_tested":46080,
      "distinct_second_slices":1920,
      "unblocked_third_slice_histogram":dict(sorted(bins.items())),
      "all_ten_recovered_12_point_third_slices_are_caps":True,
      "maximum_seven_dimensional_cap_in_restricted_family":236,
      "example_recovered_236":exemplar,
      "scope":"first 112-cap frozen, second is signed-permutation image of complementary 112-cap in the reconstructed magic basis; arbitrary GL6 maps NOT included"
    }

if __name__=="__main__":
    print(json.dumps(audit(),sort_keys=True,indent=2))
