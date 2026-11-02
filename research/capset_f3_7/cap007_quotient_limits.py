#!/usr/bin/env python3
"""Exact quotient occupancy relaxation audit. 333 is optimum of counts-only
subspace constraints from r3(4)=20, r3(5)=45, r3(6)=112.
This is NOT a 333-cap, nor a competitive global bound (published <=291).
"""
from itertools import combinations,product
import json
V=list(product(range(3),repeat=3))
index={u:i for i,u in enumerate(V)}
WITNESS333=[13,13,12,13,12,12,12,13,12,12,12,12,13,12,13,13,13,12,12,13,12,12,12,12,12,12,12]
def lines():
    return [(i,j,k) for i,j in combinations(range(27),2)
            for k in [index[tuple((-x-y)%3 for x,y in zip(V[i],V[j]))]] if j<k]
def planes():
    normals=[a for a in V if a!=(0,0,0) and next(x for x in a if x)!=2]
    assert len(normals)==13
    return [tuple(i for i,u in enumerate(V) if sum(x*y for x,y in zip(a,u))%3==v)
            for a in normals for v in range(3)]
def check(c):
    assert len(c)==27 and all(isinstance(x,int) and 0<=x<=20 for x in c)
    L=lines();P=planes()
    assert len(L)==117 and len(P)==39
    ls=[sum(c[i] for i in row) for row in L]
    ps=[sum(c[i] for i in row) for row in P]
    M=sum(c)
    assert sum(t*t for t in ps)==4*M*M+9*sum(x*x for x in c)
    return {'M':M,'Q':sum(x*x for x in c),'line_max':max(ls),'plane_max':max(ps),
            'all_quotas_hold':max(ls)<=45 and max(ps)<=112}
def mod9_exclusions():
    out=[]
    for M in (334,335,336):
        profiles={334:(111,111,112),335:(111,112,112),336:(112,112,112)}
        t=profiles[M]
        rem=(13*sum(x*x for x in t)-4*M*M)%9
        assert rem!=0
        out.append({'M':M,'all_directions_forced_plane_counts':t,'mod9_obstruction':rem})
    return out
def result():
    w=check(WITNESS333)
    assert w['M']==333 and w['all_quotas_hold']
    return {'quotient_occupancy_relaxation_optimum':333,
            'quotient_fiber_bound':20,'quotient_line_bound':45,
            'quotient_plane_bound':112,'witness_333':WITNESS333,
            'exact_check':w,'excluded_334_through_336':mod9_exclusions(),
            'scope':'only count constraints, does not construct 333-cap',
            'global_record_improved':False}
if __name__=='__main__':print(json.dumps(result(),sort_keys=True))
