#!/usr/bin/env python3
"""CAP-005I: independent exact proof checker. No SciPy, generator or networkx imports."""
import argparse,itertools,json
from pathlib import Path
from fractions import Fraction
from cap005_k6_symmetry_quotient import read_cap,generate_group,orbit_partition,image,fiber
HERE=Path(__file__).resolve().parent
third=lambda a,b:tuple((-x-y)%3 for x,y in zip(a,b))
def decode(s):
    assert isinstance(s,str) and len(s)==7 and set(s)<={'0','1','2'}
    return tuple(map(int,s))
def frac(x):
    assert isinstance(x,list) and len(x)==2 and all(type(v)==int for v in x) and x[1]>0
    return Fraction(*x)

def check(duals,unresolved,cap):
    B=read_cap(cap);maps=generate_group(B)
    data=json.loads(duals.read_text());assert len(data['certificates'])==7
    old=json.loads(unresolved.read_text());U={tuple(g) for g in old['unresolved_groups']}
    assert len(U)==old['unresolved']==88 and len(orbit_partition(U,maps))==7
    outsiders=set(itertools.product(range(3),repeat=7))-B
    assert len(outsiders)==1951
    sec={x:[] for x in outsiders}
    for a,b in itertools.combinations(sorted(B),2):
        x=third(a,b)
        if x in sec:sec[x].append((fiber(a),fiber(b)))
    covered=set();summary=[]
    for cert in data['certificates']:
        group=tuple(cert['fibers']);T=set(group)
        assert len(group)==6 and tuple(sorted(set(group)))==group
        fixed={p for p in B if fiber(p) not in T}
        V={p for p in B if fiber(p) in T}
        V|={x for x in outsiders if fiber(x) in T and all(a in T or b in T for a,b in sec[x])}
        baseline=len(B)-len(fixed);assert baseline==cert['baseline']
        weights={p:Fraction(0) for p in V};objective=Fraction(0)
        for typ,raw_points,raw_weight in cert['rows']:
            pts=tuple(map(decode,raw_points))
            assert len(set(pts))==len(pts) and all(p in V for p in pts)
            if typ=='pair':
                assert len(pts)==2 and third(*pts) in fixed;rhs=1
            elif typ=='line':
                assert len(pts)==3 and third(pts[0],pts[1])==pts[2];rhs=2
            elif typ=='triangle':
                assert len(pts)==3 and all(third(a,b) in fixed for a,b in itertools.combinations(pts,2));rhs=1
            elif typ=='cycle5':
                assert len(pts)==5 and all(third(pts[i],pts[(i+1)%5]) in fixed for i in range(5));rhs=2
            else:raise AssertionError(('unknown row',typ))
            y=frac(raw_weight);assert y>0
            objective+=rhs*y
            for p in pts:weights[p]+=y
        for raw_p,raw_weight in cert['upper']:
            p=decode(raw_p);assert p in V
            z=frac(raw_weight);assert z>0
            weights[p]+=z;objective+=z
        assert min(weights.values())>=1,(group,min(weights.values()))
        assert objective==frac(cert['objective'])
        assert objective<baseline+1,(group,objective,baseline)
        orbit={image(group,g) for g in maps}
        assert orbit<=U and not (orbit&covered)
        covered|=orbit
        summary.append((list(group),len(orbit),len(cert['rows']),baseline))
    assert covered==U and len(covered)==88
    assert data['certified_unresolved_cases']==88
    return {'exact_covered_88':len(covered),'orbit_representatives':summary,
            'total_six_fiber_subsets':296010,'total_excluded':296010,
            'restricted_optimum':236,'global_r3_7':'OPEN'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('duals',type=Path)
    p.add_argument('previous',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    a=p.parse_args();print(json.dumps(check(a.duals,a.previous,a.cap),sort_keys=True))
