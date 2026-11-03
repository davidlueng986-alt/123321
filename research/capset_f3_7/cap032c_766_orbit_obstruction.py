#!/usr/bin/env python3
"""CAP-032C: universal orbit-type obstruction for (7,6,6) AG(4,3) caps.
Conditional statement: a 7-point 3D fiber in (7,6,6) must be of the
7-cap affine orbit that is NOT extendable to any 9-cap in F3^3.
Exact finite enumeration, independent 3AP checks; not a global r3(7) bound.
"""
from itertools import combinations
from cap032b_universal_fiber_77 import caps7,reps,third,members
from collections import Counter
import json

def cap(tup):
    S=set(tup)
    return all(third[a][b] not in S for a,b in combinations(tup,2))
def all_sixcaps():
    out=[]
    for inds in combinations(range(27),6):
        if cap(inds):out.append(inds)
    assert len(out)==107406
    return out
def nine_completions(A):
    orig=set(members(A))
    open_sites=[p for p in range(27) if p not in orig and
                all(third[a][b]!=p for a,b in combinations(orig,2))]
    good=[(p,q) for p,q in combinations(open_sites,2) if cap(tuple(orig|{p,q}))]
    assert len(open_sites)==4
    return good
def audit():
    R,orbit_sizes=reps(caps7())
    assert orbit_sizes==[50544,75816]
    assert R==[5659,17947]
    second=all_sixcaps()
    counts=[];witness=None
    for A in R:
        first=list(members(A));pair_rows=[[1<<third[a][b] for b in range(27)] for a in first]
        h=Counter();compatible=0;ways=0
        for B in second:
            mask=0
            for row in pair_rows:
                for b in B:mask|=row[b]
            H=((1<<27)-1)^mask
            sites=list(members(H))
            h[len(sites)]+=1
            if len(sites)<6:continue
            local=0
            for C in combinations(sites,6):
                if cap(C):
                    local+=1
                    if witness is None:witness=[first,list(B),list(C)]
            if local:
                compatible+=1;ways+=local
        counts.append({'first_rep':A,'orbit_size':orbit_sizes[len(counts)],
                       'second_6caps_with_feasible_6cap_third':compatible,
                       'feasible_second_third_pairs':ways,
                       'nine_cap_completions':len(nine_completions(A)),
                       'raw_hole_histogram':dict(sorted(h.items()))})
    assert [x['second_6caps_with_feasible_6cap_third'] for x in counts]==[27,0]
    assert [x['feasible_second_third_pairs'] for x in counts]==[27,0]
    assert [x['nine_cap_completions'] for x in counts]==[0,1]
    assert witness is not None
    P={(i,)+tuple((p//(3**j))%3 for j in range(3)) for i,part in enumerate(witness) for p in part}
    assert len(P)==19
    assert all(tuple((-a-b)%3 for a,b in zip(x,y)) not in P
               for x,y in combinations(P,2))
    return {'first_7cap_types':counts,'sharp_7_6_6_19cap_verified':True,
            'example_witness_3_slices':witness,
            'universal_if_7_6_6_then_7cap_not_extendable_to9':True,
            'global_r3_7_bound_improved':False,'novelty_verified':False}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True))
