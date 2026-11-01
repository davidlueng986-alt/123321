#!/usr/bin/env python3
"""Independent affine-fiber saturation audit of the classical 236-point cap.

No SAT solver or floating-point. For each coordinate pair (i,j), each
fixed pair of values (a,b) determines a 5D coordinate fiber of 243
points. Keep all 236 original points outside this fiber frozen.
An exterior p inside can be selected only when EVERY original secant
passing through p has at least one endpoint in the released fiber.

Then study unions of k=2,3,4 of nine disjoint fibers fixing (x_1,x_2),
which correspond respectively to 6,9,12 of the 27 four-dimensional
blocks (prefix x0,x1,x2) described by Math Agent Campaign 001.

The number of 'unblocked' exterior candidates is only a NECESSARY
condition for an improved cap; actual candidates may conflict.
"""
import collections
import itertools
import json
from generate_calderbank_fishburn import construction

A=construction()
sec=collections.defaultdict(list)
for i,p in enumerate(A):
    for j in range(i+1,len(A)):
        q=A[j]
        z=tuple((-x-y)%3 for x,y in zip(p,q))
        sec[z].append((p,q))
assert len(sec)==1951

def external_unblocked(inside_fiber,points_to_check):
    return sum(all(p in inside_fiber or q in inside_fiber for p,q in sec[z]) for z in points_to_check)

def report():
    coordinate_fiber_counts=collections.Counter()
    special=[]
    for i,j in itertools.combinations(range(7),2):
        for a,b in itertools.product(range(3),repeat=2):
            old={p for p in A if (p[i],p[j])==(a,b)}
            outside=[p for p in sec if (p[i],p[j])==(a,b)]
            freed=external_unblocked(old,outside)
            coordinate_fiber_counts[freed]+=1
            if freed:special.append(((i,j),(a,b),len(old),freed))
    assert sum(coordinate_fiber_counts.values())==21*9
    assert dict(coordinate_fiber_counts)=={0:165,1:24}
    assert all(s[0][0]==0 and s[1][0] in (0,1) for s in special)
    families={}
    classes=list(itertools.product(range(3),repeat=2))
    for k in (1,2,3,4):
        counts=collections.Counter()
        max_freed=-1
        top=[]
        for combo in itertools.combinations(classes,k):
            combo_set=set(combo)
            old={p for p in A if p[1:3] in combo_set}
            outside=[p for p in sec if p[1:3] in combo_set]
            freed=external_unblocked(old,outside)
            counts[freed]+=1
            if freed>max_freed:
                max_freed=freed;top=[combo]
            elif freed==max_freed:
                top.append(combo)
        families[k]={"total_fiber_combinations":sum(counts.values()),
            "candidate_histogram":dict(sorted(counts.items())),
            "maximum_unblocked_new_candidates":max_freed,
            "maximizing_combinations_count":len(top),
            "sample_maximizer":top[0]}
    assert families[1]["maximum_unblocked_new_candidates"]==0
    assert families[2]["candidate_histogram"]=={0:20,1:8,2:8}
    assert families[3]["maximum_unblocked_new_candidates"]==21
    assert families[4]["maximum_unblocked_new_candidates"]==138
    return {"coordinate_codim2_fibers":189,
            "single_coordinate_fiber_unblocked_histogram":dict(sorted(coordinate_fiber_counts.items())),
            "nine_disjoint_3x4D_strip_families":families,
            "reason":"With at most one unblocked outsider in a single 5D coordinate fiber, rebuilding only that fiber cannot increase 236; if an outsider is selected at least one old point must be removed due to completeness."}

if __name__=="__main__":
    print(json.dumps(report(),sort_keys=True,indent=2))
