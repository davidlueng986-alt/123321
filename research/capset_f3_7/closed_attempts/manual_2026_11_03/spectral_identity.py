#!/usr/bin/env python3
"""Independent exact Fourier-dual convolution identity, F3^6 maximal caps.

All calculations are rational/integer; no numerical Fourier tolerances.
A,B are symmetric 112-point Hill caps. A=S, B=M*T, Q=M^-T*T.
For z!=0, r(z)=16+4*(1_A(z)+1_B(z))+(3*n0(z)-|A∩Q|)/2.
For z=0, r(0)=|A∩Q|. Both sides count -(A+B).
This identity is NOT a proof that max third-slice holes is 12.
"""
from collections import Counter
from itertools import product
from pathlib import Path
from random import Random
import os
HERE=Path(__file__).resolve()
CANDIDATES=[Path(os.environ["CAPSET_WITNESS"])] if os.environ.get("CAPSET_WITNESS") else [
    HERE.parent/"witness236.txt",
    HERE.parents[1]/"candidates"/"calderbank_fishburn_236.txt",
    Path("research/capset_f3_7/candidates/calderbank_fishburn_236.txt"),
    Path("/mnt/data/capset_closed/witness236.txt")]
BASE=next((p for p in CANDIDATES if p.is_file()),None)
if BASE is None:raise FileNotFoundError("Set CAPSET_WITNESS to the 236-point fixture")
V=list(product(range(3),repeat=6))
ZERO=(0,)*6

def load():
    a=[];b=[]
    for raw in BASE.read_text().splitlines():
        x=raw.strip()
        if len(x)==7 and set(x)<={'0','1','2'}:
            if x[0]=='0':a.append(tuple(map(int,x[1:])))
            if x[0]=='1':b.append(tuple(map(int,x[1:])))
    assert len(a)==len(b)==112
    return frozenset(a),frozenset(b)

def matvec(m,v):
    return tuple(sum(m[i][j]*v[j] for j in range(6))%3 for i in range(6))

def invert_transpose(M):
    a=[[M[i][j] for j in range(6)]+[int(i==j) for j in range(6)] for i in range(6)]
    for c in range(6):
        p=next(r for r in range(c,6) if a[r][c]!=0)
        a[c],a[p]=a[p],a[c]
        if a[c][c]==2:a[c]=[2*x%3 for x in a[c]]
        for r in range(6):
            if r==c:continue
            v=a[r][c]
            a[r]=[(x-v*y)%3 for x,y in zip(a[r],a[c])]
    return [[a[j][i+6] for j in range(6)] for i in range(6)]

def direct(A,B):
    C=Counter(tuple((-a[i]-b[i])%3 for i in range(6)) for a in A for b in B)
    return C

def spectral(A,B,Q):
    K=A & Q
    t=len(K)
    out={}
    for z in V:
        if z==ZERO: out[z]=t;continue
        n0=sum(sum(a*b for a,b in zip(k,z))%3==0 for k in K)
        assert (3*n0-t)%2==0
        out[z]=16+4*(int(z in A)+int(z in B))+(3*n0-t)//2
    assert sum(out.values())==112*112
    return out,t

def self_dual_check(A):
    assert A==frozenset(tuple(-z%3 for z in x) for x in A)
    for k in V:
        c=Counter(sum(a*b for a,b in zip(k,p))%3 for p in A)
        assert c[1]==c[2]
        F=c[0]-c[1]
        assert F==(112 if k==ZERO else (-23 if k in A else 4)), (k,F)

def run(trials=40,seed=2026110306):
    S,T=load()
    self_dual_check(S);self_dual_check(T)
    M=[[int(i==j) for j in range(6)] for i in range(6)]
    rng=Random(seed)
    cases=[]
    for i in range(trials):
        if i:
            for _ in range(2+rng.randrange(8)):
                a=rng.randrange(6);b=rng.randrange(5)
                if b>=a:b+=1
                u=rng.choice((1,2))
                M[a]=[(x+u*y)%3 for x,y in zip(M[a],M[b])]
        B=frozenset(matvec(M,x) for x in T)
        Q=frozenset(matvec(invert_transpose(M),x) for x in T)
        r,t=spectral(S,B,Q)
        original=direct(S,B)
        assert all(original[z]==r[z] for z in V)
        H=[z for z in V if not r[z]]
        if t<32:
            assert len(H)==(t==0)
        cases.append({'i':i,'intersection':t,'holes':len(H),'zero_origin':not t,'positive_min':min(v for v in r.values() if v>0)})
    print({'trials':trials,'seed':seed,'self_dual_exact':True,'all_729_convolutions_match':True,
           'intersections':dict(Counter(x['intersection'] for x in cases)),
           'holes':dict(Counter(x['holes'] for x in cases)),
           'max_holes':max(x['holes'] for x in cases),
           't_below32_no_nonzero_holes':True,'all_cases':cases[:8]})
if __name__=='__main__':run()
