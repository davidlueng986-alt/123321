#!/usr/bin/env python3
"""CAP-007J2: exact partial-difference-set / SRG certificate for centered 112-caps.
Uses only integer arithmetic; no solver, randomness, or global r3(7) claim.
"""
from collections import Counter
from itertools import product
from pathlib import Path
from cap007j_112_alignment import read_fixture,encode,V
import json


def certify(S):
    S=set(S)
    assert len(S)==112 and (0,)*6 not in S
    assert S=={tuple((-x)%3 for x in p) for p in S}
    conv=Counter()
    for a in S:
        for b in S:
            conv[tuple((x+y)%3 for x,y in zip(a,b))]+=1
    cnt=Counter()
    for z in V:
        expected=112 if z==(0,)*6 else (1 if z in S else 20)
        assert conv[z]==expected,(z,conv[z],expected)
        cnt[expected]+=1
    assert cnt==Counter({20:616,1:112,112:1})
    fourier=Counter()
    for u in V:
        values=Counter(sum(x*y for x,y in zip(u,s))%3 for s in S)
        assert values[1]==values[2]
        real=values[0]-values[1]
        desired=112 if u==(0,)*6 else (-23 if u in S else 4)
        assert real==desired,(u,real,desired)
        fourier[real]+=1
    assert fourier==Counter({4:616,-23:112,112:1})
    return {'size':112,'conv_counts':dict(sorted(cnt.items())),'fourier_eigenvalues':dict(sorted(fourier.items())),
            'cayley_graph':{'v':729,'k':112,'lambda':1,'mu':20},
            'S_is_its_own_heavy_fourier_support':True}


def cross_energy_any_second_slice(S,T):
    """Exact spectral energy for fixed centered canonical 112-cap S and ANY T.

    Applies to arbitrary 112-cap S after affine centering and linear conjugacy;
    T need not be large or maximal. All quantities are integers.
    """
    S=set(S);T=list(T)
    assert len(S)==112 and len(set(T))==len(T)
    H={u for u in V if u!=(0,)*6 and u in S}  # checked self-dual spectrum
    n=len(T)
    heavy_power=0
    for u in H:
        c=Counter(sum(a*b for a,b in zip(u,p))%3 for p in T)
        heavy_power+=(3*sum(c[i]**2 for i in range(3))-n*n)//2
    numerator=(112**2-16)*n*n+16*729*n+513*heavy_power
    assert numerator%729==0
    return numerator//729

def run(path=None):
    path=path or str(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt')
    A0,A1,_=read_fixture(path)
    assert certify(A0)==certify(A1)
    return {'experiment':'CAP-007J2','canonical_representatives_checked':2,
            'result':certify(A0),'generalization':'Every 112-cap is affine equivalent by Potechin (2008); after unique centering, Cayley graph is isomorphic to this SRG.',
            'exact_global_r3_7_status':'OPEN'}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
