#!/usr/bin/env python3
"""CAP-005G: independent exact F3 arithmetic check of rational dual witnesses.
No SciPy, no generator imports, no trust in solver objective/status.
"""
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from verify_capset import read_points, verify

HERE=Path(__file__).resolve().parent

def fiber(p):return p[0]*9+p[1]*3+p[2]
def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
def decode(s):
    assert isinstance(s,str) and len(s)==7 and set(s)<={'0','1','2'}
    return tuple(map(int,s))
def frac(t):
    assert isinstance(t,list) and len(t)==2 and all(isinstance(x,int) for x in t)
    assert t[1]>0
    return Fraction(*t)

def check(d,previous=None):
    B=read_points(HERE/'candidates'/'calderbank_fishburn_236.txt')
    assert verify(B)==236
    B=set(B)
    outsiders=set(itertools.product(range(3),repeat=7))-B
    assert len(outsiders)==1951
    secants={x:[] for x in outsiders}
    for a,b in itertools.combinations(sorted(B),2):
        x=third(a,b)
        if x in secants:secants[x].append((fiber(a),fiber(b)))
    prev_groups=set()
    if previous is not None:
        old=json.loads(Path(previous).read_text())
        assert len(old['certificates'])==680
        prev_groups={tuple(c['fibers']) for c in old['certificates']}
        assert len(prev_groups)==680
    seen=set()
    for cert in d['certificates']:
        g=tuple(cert['fibers'])
        assert len(g)==6 and tuple(sorted(set(g)))==g and all(0<=i<27 for i in g)
        assert g not in seen and g not in prev_groups
        seen.add(g)
        released=set(g)
        fixed={p for p in B if fiber(p) not in released}
        variable={p for p in B if fiber(p) in released}
        variable.update(x for x in outsiders if fiber(x) in released and
                        all(a in released or b in released for a,b in secants[x]))
        assert len(variable)>=17
        weights={p:Fraction(0) for p in variable}
        objective=Fraction(0)
        for points,raw in cert['rows']:
            t=tuple(decode(s) for s in points)
            assert len(t) in (2,3) and len(set(t))==len(t) and all(p in variable for p in t)
            if len(t)==2:
                assert third(t[0],t[1]) in fixed
                rhs=1
            else:
                assert third(t[0],t[1])==t[2]
                rhs=2
            y=frac(raw);assert y>0
            objective+=rhs*y
            for p in t:weights[p]+=y
        for s,raw in cert['upper']:
            p=decode(s);assert p in variable
            z=frac(raw);assert z>0
            weights[p]+=z;objective+=z
        assert min(weights.values())>=1,(g,'dual coverage')
        assert objective<=len(B)-len(fixed),(g,'dual objective',objective)
    assert len(seen)==d['additional_certificates']==848
    assert d['previous_excluded']==295074
    assert d['total_excluded']==295922
    assert d['unresolved']==88
    unresolved={tuple(g) for g in d['unresolved_groups']}
    assert len(unresolved)==88 and not (unresolved&seen) and not (unresolved&prev_groups)
    return len(seen)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path)
    ap.add_argument('--previous',type=Path)
    args=ap.parse_args()
    print('PASS exact rational dual certificates',check(json.loads(args.certificate.read_text()),args.previous))
