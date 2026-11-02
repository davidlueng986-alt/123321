#!/usr/bin/env python3
"""CAP-005L independent F3 arithmetic checker, no generator import/optimizer.
Requires CAP-005K's independently checked complete 1665-orbit certificate.
"""
import argparse
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def third(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))
def fiber(p): return 9*p[0]+3*p[1]+p[2]
def parse(s):
    assert isinstance(s,str) and len(s)==7 and set(s)<={'0','1','2'}
    return tuple(map(int,s))
def maps():
    def gens(i):
        a,b,c=i//9,(i//3)%3,i%3
        return ((1-a)%3*9+b*3+c,a*9+(-b)%3*3+c,
                a*9+b*3+(-c)%3,a*9+c*3+b)
    G={tuple(range(27))}
    pending=list(G)
    while pending:
        g=pending.pop()
        for k in range(4):
            h=tuple(gens(g[i])[k] for i in range(27))
            if h not in G: G.add(h);pending.append(h)
    assert len(G)==16
    return G

def check(cert_path,k7_path,cap_path):
    lines=cap_path.read_text().splitlines()
    assert lines[0].strip()=='n: 7'
    pts=[parse(s.strip()) for s in lines[1:] if s.strip()]
    B=set(pts)
    assert len(pts)==len(B)==236
    for a,b in itertools.combinations(sorted(B),2):
        assert third(a,b) not in B
    outs=set(itertools.product(range(3),repeat=7))-B
    assert len(outs)==1951
    required={x:set() for x in outs}
    for a,b in itertools.combinations(sorted(B),2):
        z=third(a,b)
        if fiber(a)!=fiber(b):
            required[z].add((fiber(a),fiber(b)))
    prior=json.loads(k7_path.read_text())
    assert prior['group_order']==16 and prior['survivor_orbits']==1665
    assert prior['original_survivors']==25124
    target={tuple(row['fibers']):row['orbit_size']
            for row in prior['representatives'] if row['N']==17}
    assert len(target)==37 and sum(target.values())==576
    data=json.loads(cert_path.read_text())
    assert len(data['certificates'])==37 and data['excluded_neighborhoods']==576
    assert data['excluded_orbits']==37 and data['remaining_neighborhoods']==24548
    assert data['remaining_orbits']==1628
    G=maps()
    seen=set()
    checked=set()
    kinds={}
    for row in data['certificates']:
        T=tuple(row['fibers'])
        assert T in target and T not in checked
        checked.add(T)
        assert row['N']==17 and row['orbit_size']==target[T]
        assert len(T)==7 and T==tuple(sorted(set(T)))
        release=set(T)
        E={x for x in outs if fiber(x) in release
           and all(a in release or b in release for a,b in required[x])}
        assert len(E)==17,(T,len(E))
        fixed={x for x in B if fiber(x) not in release}
        w=row['witness']
        kind=w['kind']
        if kind=='pair_fixed':
            a,b=map(parse,w['points'])
            z=parse(w['third'])
            assert a!=b and a in E and b in E
            assert third(a,b)==z and z in fixed
        elif kind=='triple_outsiders':
            a,b,c=map(parse,w['points'])
            assert len({a,b,c})==3 and {a,b,c}<=E
            assert third(a,b)==c
        else: raise AssertionError(('unknown witness',kind))
        kinds[kind]=kinds.get(kind,0)+1
        orbit={tuple(sorted(g[i] for i in T)) for g in G}
        assert len(orbit)==target[T] and not (orbit&seen)
        seen.update(orbit)
    assert checked==set(target) and len(seen)==576
    assert sum(kinds.values())==37
    return {'status':'PASS_INDEPENDENT_EXACT_F3','certificates':37,
            'excluded_seven_fiber_neighborhoods':576,
            'remaining_seven_fiber_neighborhoods':24548,
            'witness_types':kinds,'global_bound_improved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('certificate',type=Path)
    p.add_argument('prior',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    a=p.parse_args()
    print(json.dumps(check(a.certificate,a.prior,a.cap),sort_keys=True))
