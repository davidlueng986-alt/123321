#!/usr/bin/env python3
"""Exact saturation/line-incidence analysis of any cap in F_3^7.

For external p and q in cap A, its unique paired cap endpoint is
r = -p-q mod 3. Therefore secants through p pair disjoint cap endpoints.
To add p, one must remove >= number_of_secants(p) members of A.
"""
import collections
import itertools
import json
from verify_capset import read_points, verify

def analyze(points, dimension=7):
    points = list(points)
    size = verify(points, dimension)
    inside = set(points)
    outside = set(itertools.product(range(3),repeat=dimension)) - inside
    incidences = collections.defaultdict(list)
    for i, x in enumerate(points):
        for j in range(i+1,size):
            y=points[j]
            p=tuple((-a-b)%3 for a,b in zip(x,y))
            assert p not in inside, "Construction must be cap"
            incidences[p].append((i,j))
    counts=[len(incidences[p]) for p in outside]
    assert sum(counts) == size*(size-1)//2
    for p in outside:
        edges=incidences[p]
        # Every secant through p has a disjoint pair of endpoints in A.
        ends=[idx for edge in edges for idx in edge]
        assert len(ends)==len(set(ends))
    histogram=dict(sorted(collections.Counter(counts).items()))
    slice_histograms={}
    for s in range(3):
        slice_histograms[s]=dict(sorted(collections.Counter(
            len(incidences[p]) for p in outside if p[0]==s).items()))
    return {
       "dimension": dimension,"cap_size": size,
       "outside_points": len(outside),"covered_outside_points": len(incidences),
       "is_complete": len(incidences)==len(outside),
       "total_secants": sum(counts),
       "minimum_secants_per_outside": min(counts) if counts else None,
       "maximum_secants_per_outside": max(counts) if counts else None,
       "secant_histogram": histogram,
       "slice_histograms": slice_histograms,
       "structural_implication": "Adding any outside point requires removing at least s_A(p) pairwise disjoint cap endpoints; the minimum over p is the minimum replacement barrier."
    }

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("candidate")
    args=ap.parse_args()
    print(json.dumps(analyze(read_points(args.candidate)),indent=2,sort_keys=True))
