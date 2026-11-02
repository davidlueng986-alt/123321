#!/usr/bin/env python3
"""Independent exact mod-3 verifier for CAP-005F clique-cover witnesses.
Does not use generator's eligibility code, graph coloring, or networkx.
"""
import argparse
import itertools
import json
from pathlib import Path
from verify_capset import read_points, verify

def f(p): return 9*p[0]+3*p[1]+p[2]
def negsum(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))

def check(data,points):
    assert verify(points)==236
    B=set(points)
    outsider=sorted(set(itertools.product(range(3),repeat=7))-B)
    pairs={x:[] for x in outsider}
    for i,a in enumerate(points):
        for b in points[i+1:]:
            x=negsum(a,b)
            if x in pairs: pairs[x].append((f(a),f(b)))
    assert len(outsider)==1951 and all(pairs.values())
    certs=data['certificates']
    assert len(certs)==data['new_certificates']==680
    seen=set()
    for cert in certs:
        group=tuple(cert['fibers'])
        assert len(group)==6 and len(set(group))==6 and all(0<=i<27 for i in group)
        assert group not in seen
        seen.add(group)
        released=set(group)
        fixed={p for p in B if f(p) not in released}
        expected={x for x in outsider if f(x) in released and
                  all(u in released or v in released for u,v in pairs[x])}
        classes=cert['classes']
        assert 1<=len(classes)<=16
        covered=[]
        for cl in classes:
            assert cl
            pts=[tuple(map(int,s)) for s in cl]
            for a,b in itertools.combinations(pts,2):
                assert negsum(a,b) in fixed, (group,a,b)
            covered.extend(pts)
        assert len(covered)==len(set(covered))==len(expected)
        assert set(covered)==expected and len(expected)>=17
    assert data['previously_excluded']==294394
    assert data['total_excluded']==295074
    assert data['unresolved']==936
    return len(certs)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('certificate',type=Path)
    args=ap.parse_args()
    data=json.loads(args.certificate.read_text(encoding='utf-8'))
    points=read_points(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt')
    n=check(data,points)
    print(f'PASS independent arithmetic clique-cover checker: {n} certified six-fiber neighborhoods, 936 unresolved; restricted only')
if __name__=='__main__': main()
