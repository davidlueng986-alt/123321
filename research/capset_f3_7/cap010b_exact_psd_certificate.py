#!/usr/bin/env python3
"""CAP-010B: exact integer spectral certificate for the classical 112+112 slices.
Pure Python integers, no floating point/solver/GPU/seed. Scope: fixed known
Calderbank--Fishburn 236 construction; not arbitrary 112-cap pairs.
Run: python research/capset_f3_7/cap010b_exact_psd_certificate.py
"""
from collections import Counter
from itertools import product
from math import lcm
from pathlib import Path
import json
from verify_capset import read_points, verify

LAMBDA_SCALED = 185130000
EXPECTED_DEGREES = {11:32,15:192,16:160,18:240,24:60,30:32,32:1}

def encode(v):
    s=0
    for t in v:
        s=3*s+t
    return s

def negsum(a,b):
    return tuple((-x-y)%3 for x,y in zip(a,b))

def make_gram(witness=None):
    if witness is None:
        witness=Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'
    points=read_points(witness,dimension=7)
    assert verify(points,7)==236
    slices=[[p[1:] for p in points if p[0]==t] for t in range(3)]
    assert list(map(len,slices))==[112,112,12]
    H,Hp=slices[:2]
    Hset=set(H)
    blocked={negsum(x,y) for x in H for y in Hp}
    assert len(blocked)==717
    assert len(set(product(range(3),repeat=6))-blocked)==12
    histogram=Counter()
    supports=[]
    for z in sorted(blocked):
        js=[j for j,y in enumerate(Hp) if negsum(z,y) in Hset]
        histogram[len(js)]+=1
        supports.append(js)
    assert dict(histogram)==EXPECTED_DEGREES
    scale=lcm(*histogram)
    assert scale==15840
    n=len(Hp)
    G=[[0]*n for _ in range(n)]
    for js in supports:
        t=(scale//len(js))**2
        for i in js:
            for j in js:
                G[i][j]+=t
    assert all(G[i][j]==G[j][i] for i in range(n) for j in range(n))
    assert sum(G[i][i] for i in range(n))==sum(scale**2//len(js) for js in supports)
    return G,histogram,scale

def difference_psd_matrix(G,lam=LAMBDA_SCALED):
    # D maps a to sum_i a_i(e_(i+1)-e_0) in 1^perp.
    # K = D^T(lam I-G)D, a symmetric 111x111 integer matrix.
    n=len(G)
    return [[lam*(1+int(i==j))-G[i+1][j+1]+G[i+1][0]+G[0][j+1]-G[0][0]
             for j in range(n-1)] for i in range(n-1)]

def bareiss_psd_rank(matrix):
    """Exact symmetric fraction-free Schur pivots with divisibility checks.
    Each trailing Bareiss block is a positive multiple of the true Schur
    complement. Symmetric swaps preserve inertia. Zero diagonal maximum
    requires entire trailing block zero. No numerical eigenvalue is used.
    """
    A=[list(row) for row in matrix]
    n=len(A)
    assert all(len(row)==n for row in A)
    assert all(A[i][j]==A[j][i] for i in range(n) for j in range(i+1,n))
    prev=1
    swaps=0
    first=[]
    for k in range(n):
        idx=max(range(k,n),key=lambda i:A[i][i])
        if A[idx][idx]==0:
            assert all(A[i][j]==0 for i in range(k,n) for j in range(k,n))
            return {'psd':True,'rank':k,'nullity':n-k,'symmetric_swaps':swaps,'first_pivots':first}
        assert A[idx][idx]>0, f'negative Schur pivot at {k}'
        if idx!=k:
            A[k],A[idx]=A[idx],A[k]
            for row in A:
                row[k],row[idx]=row[idx],row[k]
            swaps+=1
        pivot=A[k][k]
        if len(first)<3:
            first.append(pivot)
        if k==n-1:
            return {'psd':True,'rank':n,'nullity':0,'symmetric_swaps':swaps,'first_pivots':first}
        for i in range(k+1,n):
            aik=A[i][k]
            for j in range(i,n):
                numerator=pivot*A[i][j]-aik*A[k][j]
                q,rem=divmod(numerator,prev)
                assert rem==0, f'nonexact Bareiss division at {k,i,j}'
                A[i][j]=q
                A[j][i]=q
        for i in range(k+1,n):
            A[i][k]=A[k][i]=0
        prev=pivot
    raise AssertionError('unreachable')

def min_deletions(m):
    assert m>=1
    return (64512*m+576*m+47600-1)//(576*m+47600)

def independent_base3_cap_check(points):
    """Independent base-3 integer pair checker, distinct from verify()."""
    values={encode(p) for p in points}
    assert len(values)==len(points)
    powers=[3**k for k in range(7)]
    for i,a in enumerate(points):
        for b in points[i+1:]:
            u,v=encode(a),encode(b)
            third=sum((-(u//power%3)-(v//power%3))%3*power for power in powers)
            assert third not in values
    return True

def modular_rank(matrix,prime=1000000007):
    """Independent modular rank lower-bound check."""
    A=[[v%prime for v in row] for row in matrix]
    rows,cols=len(A),len(A[0])
    rank=0
    for col in range(cols):
        pivot=next((i for i in range(rank,rows) if A[i][col]),None)
        if pivot is None:
            continue
        A[rank],A[pivot]=A[pivot],A[rank]
        inv=pow(A[rank][col],-1,prime)
        for i in range(rank+1,rows):
            factor=A[i][col]*inv%prime
            if factor:
                for j in range(col+1,cols):
                    A[i][j]=(A[i][j]-factor*A[rank][j])%prime
                A[i][col]=0
        rank+=1
    return rank

def certificate(witness=None):
    fixture=(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt') if witness is None else witness
    assert independent_base3_cap_check(read_points(fixture,dimension=7))
    G,histogram,L=make_gram(fixture)
    K=difference_psd_matrix(G)
    result=bareiss_psd_rank(K)
    assert result['psd'] and result['rank']==107 and result['nullity']==4
    assert modular_rank(K)==107
    assert 576*LAMBDA_SCALED==425*L*L
    assert all(min_deletions(m)>=m+1 for m in range(1,30))
    assert all(min_deletions(m)>=m for m in range(1,33))
    result.update({'scope':'fixed classical 112+112 slices only',
                   'blocked_third_slice_points':717,
                   'row_degree_histogram':dict(sorted(histogram.items())),
                   'scale':L,'scaled_lambda':LAMBDA_SCALED,
                   'independent_base3_checker':True,'independent_mod_prime_rank':107,
                   'lambda_perp_fraction':'425/576',
                   'm_1_to_29_requires_at_least_m_plus_1_deletions':True,
                   'm_1_to_32_requires_at_least_m_deletions':True,
                   'sample_m_to_min_d':{str(m):min_deletions(m) for m in (1,10,20,29,30,32,35)},
                   'new_global_upper_bound':False})
    return result

if __name__=='__main__':
    print(json.dumps(certificate(),sort_keys=True))
