#!/usr/bin/env python3
"""Independent exact audit of all hyperplane slice spectra of the 236-point cap.
Inspired by an independent Math Agent Campaign 001 v2.0 Google Drive report.
No imported results, no floating-point, no external dependencies.

For nonzero linear normals d in F3^n modulo +/-1, compute a_(d,0..2).
One each dimension the count is (3^n-1)/2 normals.

General identity (holds for ANY finite set, not merely caps):
sum_d sum_c a_(d,c)^2 =
    M^2 * (3^(n-1)-1)/2 + M*3^(n-1).
Reason: use double counting of ordered point-pairs in each affine
hyperplane, where nonzero differences have (3^(n-1)-1)/2 orthogonal
projective directions, and diagonal pairs have (3^n-1)/2.
"""
import collections
import itertools
import json
from generate_calderbank_fishburn import construction
from verify_capset import verify

def normal_directions(n):
    for normal in itertools.product(range(3),repeat=n):
        if not any(normal):
            continue
        first=next(x for x in normal if x)
        if first==1:
            yield normal

def spectrum(points):
    points=[tuple(x) for x in points]
    n=len(points[0]);M=len(points)
    assert all(len(x)==n for x in points)
    histogram=collections.Counter()
    mins=[];maximum=0
    all_slices=[]
    for d in normal_directions(n):
        counts=[0]*3
        for x in points:
            counts[sum(a*b for a,b in zip(d,x))%3]+=1
        assert sum(counts)==M
        pattern=tuple(sorted(counts,reverse=True))
        histogram[pattern]+=1
        maximum=max(maximum,max(counts))
        mins.append(min(counts))
        all_slices.append(counts)
    count_directions=(3**n-1)//2
    assert sum(histogram.values())==count_directions
    lhs=sum(sum(k*k for k in a) for a in all_slices)
    rhs=M*M*((3**(n-1)-1)//2)+M*(3**(n-1))
    assert lhs==rhs
    return {"n":n,"size":M,"projective_directions":count_directions,
      "affine_hyperplanes":3*count_directions,
      "parseval_lhs":lhs,"parseval_rhs":rhs,
      "slice_types":len(histogram),
      "histogram":{"-".join(str(k) for k in p):c for p,c in sorted(histogram.items(),reverse=True)},
      "smallest_slice":min(mins),"largest_slice":maximum,
      "num_directions_with_smallest_slice":sum(v==min(mins) for v in mins)}

def audit():
    A=construction()
    assert verify(A)==236
    s=spectrum(A)
    assert s["n"]==7 and s["size"]==236
    assert s["projective_directions"]==1093
    assert s["affine_hyperplanes"]==3279
    assert s["parseval_lhs"]==20445388
    assert s["slice_types"]==12
    assert s["histogram"]["112-112-12"]==1
    assert s["histogram"]["96-96-44"]==16
    assert s["smallest_slice"]==12
    assert s["largest_slice"]==112
    return s

def audit_8d():
    from edel496_reproduction import construct
    A=construct()
    s=spectrum(A)
    assert s["n"]==8 and s["size"]==496
    assert s["projective_directions"]==3280
    assert s["parseval_lhs"]==269980240
    assert s["slice_types"]==17
    assert s["histogram"]["236-236-24"]==2
    return s

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--include-8d",action="store_true")
    args=p.parse_args()
    print("DIMENSION 7",json.dumps(audit(),indent=2,sort_keys=True))
    if args.include_8d:
        print("DIMENSION 8",json.dumps(audit_8d(),indent=2,sort_keys=True))
