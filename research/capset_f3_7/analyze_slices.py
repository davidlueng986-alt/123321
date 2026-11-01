#!/usr/bin/env python3
"""Exact cross-slice obstruction for the Calderbank–Fishburn 236-cap."""
import collections
import itertools
from generate_calderbank_fishburn import construction

def analyze_slices():
    cap=construction()
    a0=[x for x in cap if x[0]==0]
    a1=[x for x in cap if x[0]==1]
    a2={x for x in cap if x[0]==2}
    cross=collections.defaultdict(list)
    for x in a0:
        for y in a1:
            z=tuple((-u-v)%3 for u,v in zip(x,y))
            assert z[0]==2
            cross[z].append((x,y))
    slice2={v for v in itertools.product(range(3), repeat=7) if v[0]==2}
    permissible=slice2-set(cross)
    assert permissible==a2
    assert len(cross)==717
    assert len(permissible)==12
    # For any fixed z, each x uniquely determines its partner y; cross pairs
    # therefore have distinct endpoints and form a matching.
    for edges in cross.values():
        ends=[p for pair in edges for p in pair]
        assert len(set(ends))==len(ends)
    blockers=[len(edges) for edges in cross.values()]
    assert min(blockers)==11
    return {
        "fixed_slice_sizes":[len(a0),len(a1)],
        "cross_blocked_slice2":len(cross),
        "only_12_compatible_slice2_points":[ "".join(map(str,x)) for x in sorted(permissible) ],
        "minimum_cross_secants_for_nonmember_slice2":min(blockers),
        "max_cross_secants":max(blockers),
        "rigorous_implication":"Keeping the 112+112 points in slices 0 and 1 fixes ALL 12 compatible third-slice points. To introduce even one other third-slice point, at least 11 original points of slices 0 and 1 must be removed."
    }

if __name__=="__main__":
    import json
    print(json.dumps(analyze_slices(), indent=2))
