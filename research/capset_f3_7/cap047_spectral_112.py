#!/usr/bin/env python3
"""CAP-047: exact Fourier/difference-set theorem for two maximal AG(6,3) caps.

The theorem targets the CONSTRUCTION disproof path: 112+112+13 -> 237 points.
No claim that all 237 caps have this slice profile. NO solver UNSAT proof.
All arithmetic exact mod3 or integers (no floating point DFT).
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from random import Random
import json

V = tuple(product(range(3), repeat=6))
ZERO = (0,)*6
FIXTURE=Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'
if not FIXTURE.exists():
    FIXTURE=Path(__file__).resolve().parents[1]/'capset_closed'/'witness236.txt'

def load(path=FIXTURE):
    lines=[x.strip() for x in path.read_text().splitlines() if len(x.strip())==7 and set(x.strip())<={'0','1','2'}]
    assert len(lines)==236
    first={tuple(map(int,x[1:])) for x in lines if x[0]=='0'}
    second={tuple(map(int,x[1:])) for x in lines if x[0]=='1'}
    assert len(first)==len(second)==112
    return first,second

def dot(p,q):return sum(a*b for a,b in zip(p,q))%3

def neg(p):return tuple(-x%3 for x in p)

def selfdual_fingerprint(S):
    assert len(S)==112 and ZERO not in S and all(neg(x) in S for x in S)
    R=Counter(tuple((a[i]-b[i])%3 for i in range(6)) for a in S for b in S)
    assert len(R)==729 and R[ZERO]==112
    assert all(R[x]==(1 if x in S else 20) for x in V if x!=ZERO)
    z0={x:sum(dot(x,p)==0 for p in S) for x in V}
    assert all(z0[x]==(112 if x==ZERO else (22 if x in S else 40)) for x in V)
    assert all(neg(p) in S for p in S)
    return {'difference_counts': {'zero':112,'inside_S':1,'outside_S_nonzero':20},
            'orthogonality_counts':{'zero':112,'inside_S':22,'outside_S_nonzero':40},
            'fourier':{'zero':112,'inside_S':-23,'outside_S_nonzero':4}}

def matvec(M,v):return tuple(sum(M[i][j]*v[j] for j in range(6))%3 for i in range(6))

def inverse_transpose(M):
    a=[[M[i][j] for j in range(6)]+[int(i==j) for j in range(6)] for i in range(6)]
    for k in range(6):
        t=next(i for i in range(k,6) if a[i][k]!=0)
        a[k],a[t]=a[t],a[k]
        if a[k][k]==2:a[k]=[2*x%3 for x in a[k]]
        for i in range(6):
            if i==k:continue
            c=a[i][k]
            a[i]=[(x-c*y)%3 for x,y in zip(a[i],a[k])]
    inv=[row[6:] for row in a]
    return [list(row) for row in zip(*inv)]

def convolution_direct(S,T):
    return Counter(tuple((-a[i]-b[i])%3 for i in range(6)) for a in S for b in T)

def spectral_predict(S,T,low_dual_T):
    C=S&low_dual_T
    n=len(C)
    assert n%2==0
    out={}
    for z in V:
        if z==ZERO:
            out[z]=n
        else:
            n0=sum(dot(z,c)==0 for c in C)
            assert (3*n0-n)%2==0
            out[z]=16+4*int(z in S)+4*int(z in T)+(3*n0-n)//2
            assert out[z]>=0
    assert sum(out.values())==112**2
    return out,n

def verify_sample(trials=60,seed=2026110405):
    S,T0=load()
    Fs=selfdual_fingerprint(S)
    assert selfdual_fingerprint(T0)==Fs
    R=Random(seed)
    M=[[int(i==j) for j in range(6)] for i in range(6)]
    obs=[]
    for k in range(trials):
        if k%7==0:M=[[int(i==j) for j in range(6)] for i in range(6)]
        else:
            for _ in range(1+R.randrange(10)):
                i=R.randrange(6);j=R.randrange(5)
                if j>=i:j+=1
                a=1+R.randrange(2)
                M[i]=[(u+a*v)%3 for u,v in zip(M[i],M[j])]
        T={matvec(M,x) for x in T0}
        assert len(T)==112
        Q={matvec(inverse_transpose(M),x) for x in T0}
        P,n=spectral_predict(S,T,Q)
        D=convolution_direct(S,T)
        assert all(D[z]==P[z] for z in V)
        holes=sum(D[z]==0 for z in V)
        if n<32:assert holes==(n==0)
        obs.append((n,holes))
    return {'sample_matrices':trials,'seed':seed,'all_729_correlations_exact':True,
            'fingerprint':Fs,'intersection_histogram':dict(sorted(Counter(t for t,h in obs).items())),
            'hole_histogram':dict(sorted(Counter(h for t,h in obs).items())),
            'logical_consequence':'If t=|S intersect dual(T)| is 1..30, S+T covers all F3^6. If t=0, its complement contains exactly the origin. This is exact for ALL centrally normalized maximal 112-cap pairs, using published uniqueness of 112 cap and established canonical self-duality.',
            'max_empirical_holes':max(h for t,h in obs),
            'claim_all_112_112_holes_at_most_12_proven':False,
            'exact_r3_7_closed':False}

def counterexample_to_naive_C_subset():
    """Shows the t=32 intersection must be more than just an arbitrary 32-subset of S."""
    S,_=load()
    # Input order and antipodal canonical representatives are part of this artifact.
    src=[tuple(map(int,x.strip()[1:])) for x in FIXTURE.read_text().splitlines()
         if len(x.strip())==7 and x.strip()[0]=='0']
    rays=[];seen=set()
    for p in src:
        k=min(p,neg(p))
        if k not in seen:seen.add(k);rays.append(k)
    assert len(rays)==56
    inds=[2,6,11,12,13,17,23,27,29,32,33,35,38,40,47,50]
    C={p for i in inds for p in (rays[i],neg(rays[i]))}
    assert len(C)==32 and C<=S
    assert all(tuple((-a[i]-b[i])%3 for i in range(6)) not in C for a,b in combinations(C,2))
    avoiding=[z for z in V if z!=ZERO and all(dot(z,x)!=0 for x in C)]
    assert len(avoiding)==14
    return {'C_32_points_as_16_antipodal_representatives':[''.join(map(str,rays[i])) for i in inds],
            'avoiding_nonzero_normals':[''.join(map(str,x)) for x in avoiding],
            'avoiding_normal_count':14,
            'conclusion':'False: arbitrary centrally symmetric 32-cap subset of S cannot have more than 12 missing central-hyperplane normals. Actual intersection S intersect dual(T) has additional structure.'}

if __name__=='__main__':
    print(json.dumps({'spectral':verify_sample(),'adversarial_C32':counterexample_to_naive_C_subset()},indent=2,sort_keys=True))