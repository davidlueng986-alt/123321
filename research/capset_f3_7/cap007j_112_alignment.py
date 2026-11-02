#!/usr/bin/env python3
"""CAP-007J: exact finite audit of relative linear alignments of two maximal 112-caps.

No global upper bound is claimed. Test family: identity and products of up to two
of 81 elementary GL(6,3) matrices, all affine translations factored out.
Computations are integers over F3; sampling is separately labelled exploratory.
"""
import argparse
from collections import Counter,defaultdict
from itertools import combinations,product
import json
from pathlib import Path

n=6
W=(243,81,27,9,3,1)
V=list(product(range(3),repeat=6))

def encode(p): return sum(a*b for a,b in zip(p,W))
def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
def read_fixture(path):
    data=Path(path).read_text().splitlines()
    assert data[0].strip()=='n: 7'
    P=[tuple(int(x) for x in row.strip()) for row in data[1:] if row.strip()]
    assert len(P)==236 and len(set(P))==236
    S=set(P)
    for a,b in combinations(P,2):
        assert tuple((-x-y)%3 for x,y in zip(a,b)) not in S
    B0={p[1:] for p in P if p[0]==0}
    B1={p[1:] for p in P if p[0]==1}
    B2={p[1:] for p in P if p[0]==2}
    assert (len(B0),len(B1),len(B2))==(112,112,12)
    return sorted(B0),sorted(B1),sorted(B2)

def matmul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(6))%3 for j in range(6)) for i in range(6))

def transform(M,p):
    return tuple(sum(x*y for x,y in zip(row,p))%3 for row in M)

def unit_ops():
    I=tuple(tuple(int(i==j) for j in range(6)) for i in range(6))
    yield 'I',I
    for i in range(6):
        A=[list(row) for row in I]; A[i][i]=2
        yield f'sign{i}',tuple(map(tuple,A))
    for i in range(6):
        for j in range(i+1,6):
            A=[list(row) for row in I]; A[i],A[j]=A[j],A[i]
            yield f'swap{i}_{j}',tuple(map(tuple,A))
    for i in range(6):
        for j in range(6):
            if i==j:continue
            for t in (1,2):
                A=[list(row) for row in I]; A[i][j]=t
                yield f'shear{i}_{j}_{t}',tuple(map(tuple,A))

def matrix_family():
    gens=list(unit_ops())
    assert len(gens)==82
    mats={gens[0][1]:0}
    for _,m in gens[1:]: mats.setdefault(m,1)
    for _,a in gens[1:]:
        for _,b in gens[1:]: mats.setdefault(matmul(a,b),2)
    assert len(mats)==3812
    return mats

def make_third_table(B0):
    return {a:tuple(encode(third(a,b)) for b in V) for a in B0}

def holes(B1,M,table):
    used=bytearray(729)
    for p in B1:
        b=encode(transform(M,p))
        for a in table.values():used[a[b]]=1
    return tuple(i for i in range(729) if not used[i])

def has_line(points):
    S=set(points)
    return any(third(a,b) in S for a,b in combinations(points,2))

def power_mask(B):
    heavy=set()
    spectrum=Counter()
    for i,u in enumerate(V):
        c=[0,0,0]
        for p in B:
            c[sum(a*b for a,b in zip(p,u))%3]+=1
        x=(3*sum(z*z for z in c)-112*112)//2
        if i==0:assert x==112*112
        else:
            spectrum[x]+=1
            if x==529:heavy.add(i)
            else:assert x==16
    assert spectrum==Counter({16:616,529:112})
    return heavy

def additive_energy_formula(k):
    nom=112**4+728*16**2+2*112*16*513+k*513**2
    assert nom%729==0
    return nom//729

def calc(fixture):
    B0,B1,B2=read_fixture(fixture)
    table=make_third_table(B0)
    heavy0=power_mask(B0);heavy1=power_mask(B1)
    mats=matrix_family()
    histogram=Counter();overlap_to_holes=defaultdict(Counter)
    count12caps=0
    for M,depth in mats.items():
        H=holes(B1,M,table)
        q=len(H)
        histogram[q]+=1
        k=sum(encode(transform(tuple(tuple(M[j][i] for j in range(6)) for i in range(6)),V[u])) in heavy1 for u in heavy0)
        # Alternative direct algebra: <u, Mp>=<M^T u,p>.
        overlap_to_holes[k][q]+=1
        assert additive_energy_formula(k)>0
        if q==12:
            assert not has_line([V[i] for i in H])
            count12caps+=1
    identity=next(m for name,m in unit_ops() if name=='I')
    E=holes(B1,identity,table)
    assert {V[i] for i in E}==set(B2)
    assert histogram==Counter({0:3505,1:126,4:60,12:121})
    assert count12caps==121
    # Any affine translation t of B1 translates E by -t exactly, so does not
    # change size, cap property, or any invariant used in this enumeration.
    return {'problem':'CAP-007J','scope':'112+112 fixed first slice; relative linear maps length <=2',
            'matrices':len(mats),'elementary_generators':81,
            'holes_histogram':dict(sorted(histogram.items())),
            'max_eligible_third_slice':12,'num_12_hole_caps':count12caps,
            'baseline_holes':len(E),'spectra_two_level':{'power16':616,'power529':112},
            'spectral_overlap_holes':{str(k):dict(sorted(v.items())) for k,v in sorted(overlap_to_holes.items())},
            'translation_count_redundant':729,
            'statement':'restricted exact only: global target237 remains OPEN'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fixture',default=str(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'))
    ap.add_argument('--out')
    a=ap.parse_args();r=calc(a.fixture)
    s=json.dumps(r,sort_keys=True,indent=2)+'\n'
    if a.out:Path(a.out).write_text(s)
    print(s)
if __name__=='__main__':main()
