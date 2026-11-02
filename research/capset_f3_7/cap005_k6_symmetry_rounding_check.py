#!/usr/bin/env python3
"""CAP-005H independent exact checker. No SciPy or generator imports."""
import argparse,json
from pathlib import Path
from itertools import combinations,product
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

def check(dual_path,cap_path,certificate_path=None):
    B=read_cap(cap_path);maps=generate_group(B)
    duals=json.loads(dual_path.read_text())
    assert len(duals['certificates'])==2
    outsiders=set(product(range(3),repeat=7))-B
    assert len(outsiders)==1951
    sec={x:[] for x in outsiders}
    for a,b in combinations(sorted(B),2):
        x=third(a,b)
        if x in sec:sec[x].append((fiber(a),fiber(b)))
    checked=[]
    for cert in duals['certificates']:
        group=tuple(cert['fibers'])
        assert len(group)==6 and tuple(sorted(set(group)))==group
        T=set(group);fixed={p for p in B if fiber(p) not in T}
        V={p for p in B if fiber(p) in T}
        V|={x for x in outsiders if fiber(x) in T and all(a in T or b in T for a,b in sec[x])}
        baseline=len(B)-len(fixed)
        assert baseline==cert['baseline_occupancy']
        weights={p:Fraction(0) for p in V};objective=Fraction(0)
        for points,raw in cert['rows']:
            pts=tuple(map(decode,points))
            assert len(pts) in (2,3) and len(set(pts))==len(pts) and all(p in V for p in pts)
            if len(pts)==2:
                assert third(pts[0],pts[1]) in fixed
                rhs=1
            else:
                assert third(pts[0],pts[1])==pts[2]
                rhs=2
            y=frac(raw);assert y>0;objective+=rhs*y
            for p in pts:weights[p]+=y
        for s,raw in cert['upper']:
            p=decode(s);assert p in V
            z=frac(raw);assert z>0
            objective+=z;weights[p]+=z
        assert min(weights.values())>=1
        assert objective==frac(cert['dual_objective'])
        assert objective<baseline+1
        checked.append(group)
    assert set(checked)=={(1,2,3,4,8,18),(1,2,4,5,7,18)}
    covered=set()
    for rep in checked:
        orbit={image(rep,g) for g in maps}
        assert len(orbit)==16 and not (covered&orbit)
        covered|=orbit
    assert len(covered)==32
    if certificate_path:
        data=json.loads(certificate_path.read_text())
        U={tuple(g) for g in data['unresolved_groups']}
        assert data['unresolved']==88 and len(U)==88
        assert covered<=U and len(orbit_partition(U,maps))==7
        assert len(U-covered)==56
    return {'new_exact_exclusions':32,'cumulative_exact_exclusions':295954,
            'unresolved':56,'group_order':16,'global_status':'OPEN'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--duals',type=Path,required=True)
    p.add_argument('--certificate',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    a=p.parse_args()
    print(json.dumps(check(a.duals,a.cap,a.certificate),sort_keys=True))
