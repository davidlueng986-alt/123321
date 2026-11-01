#!/usr/bin/env python3
"""Independent exact reconstruction of the C6 Paley magic basis & 240-group.

Starting only from the verified 112-point 6D cap H of the classical
236 construction, prove the main concrete claims in Math Agent Campaign
001 v2.0 using integer arithmetic:
- 56 special normals, every one with slices (22,45,45)
- an invertible six-normal magic basis, Hamming weights (4:60,5:12,6:40)
- ± rows of a symmetric conference W6 with W^2=-I (mod 3)
- precisely 240 signed permutations preserving the transformed 112-cap
- 13 orbits in F3^6, exactly TWO 112-cap orbit unions, disjoint
- their cross-sum shadow is all F3^6 except the origin, lifting to a 225-cap

No claims of novel cap records. Source reference:
https://docs.google.com/document/d/1_TWv6RzjYtBHJCawC6aT-q4ulBBdKuFaR7_nUaWp7lY/edit
"""
import collections
import itertools
import json
from generate_calderbank_fishburn import construction
from verify_capset import verify

H=sorted(p[1:] for p in construction() if p[0]==0)
assert verify(H,6)==112
basis=(
 (0,0,1,1,0,1),
 (0,0,1,1,0,2),
 (0,1,0,0,1,1),
 (0,1,0,0,2,2),
 (1,2,0,1,0,0),
 (1,2,0,2,0,0),
)

def dot(x,y):
    return sum(a*b for a,b in zip(x,y))%3

def rank_mod3(matrix):
    m=[list(row) for row in matrix]
    n=len(m);rank=0
    for col in range(n):
        pivot=next((i for i in range(rank,n) if m[i][col]%3),None)
        if pivot is None:continue
        m[rank],m[pivot]=m[pivot],m[rank]
        inv=1 if m[rank][col]==1 else 2
        m[rank]=[(inv*x)%3 for x in m[rank]]
        for i in range(n):
            if i==rank:continue
            coeff=m[i][col]
            m[i]=[(u-coeff*v)%3 for u,v in zip(m[i],m[rank])]
        rank+=1
    return rank

def action(x,g):
    perm,mask=g
    y=[0]*6
    for i,j in enumerate(perm):
        y[j]=(2 if (mask>>i)&1 else 1)*x[i]%3
    return tuple(y)

def audit():
    normals=[]
    for n in itertools.product(range(3),repeat=6):
        if not any(n) or next(v for v in n if v)!=1:
            continue
        bins=collections.Counter(dot(n,p) for p in H)
        if tuple(sorted(bins.values()))==(22,45,45):
            assert bins[0]==22
            normals.append(n)
    assert len(normals)==56
    zeros=[{i for i,p in enumerate(H) if dot(n,p)==0} for n in normals]
    assert all(len(a&b)==4 for a,b in itertools.combinations(zeros,2))
    assert rank_mod3(basis)==6
    for n in basis:
        assert n in normals
    chosen_zero=[{i for i,p in enumerate(H) if dot(n,p)==0} for n in basis]
    assert all(not a&b&c for a,b,c in itertools.combinations(chosen_zero,3))

    transformed={tuple(dot(n,p) for n in basis) for p in H}
    assert len(transformed)==112 and verify(transformed,6)==112
    weights=collections.Counter(sum(c!=0 for c in p) for p in transformed)
    assert weights=={4:60,5:12,6:40}
    weight5=[p for p in transformed if sum(v!=0 for v in p)==5]
    row_pairs=[]
    for i in range(6):
        pp=[p for p in weight5 if p[i]==0]
        assert len(pp)==2 and all((a+b)%3==0 for a,b in zip(*pp))
        row_pairs.append(pp)
    possible=[]
    for choices in itertools.product((0,1),repeat=6):
        W=[row_pairs[i][choices[i]] for i in range(6)]
        if all(W[i][j]==W[j][i] for i in range(6) for j in range(6)):
            possible.append(W)
    assert possible
    W=possible[0]
    assert all(W[i][i]==0 for i in range(6))
    assert all(W[i][j] in (1,2) for i in range(6) for j in range(6) if i!=j)
    assert all(sum(W[i][k]*W[k][j] for k in range(6))%3==(2 if i==j else 0)
               for i in range(6) for j in range(6))

    group=[]
    for P in itertools.permutations(range(6)):
        for mask in range(64):
            g=(P,mask)
            if all(action(x,g) in transformed for x in transformed):
                group.append(g)
    assert len(group)==240
    remaining=set(itertools.product(range(3),repeat=6))
    orbits=[]
    while remaining:
        x=min(remaining)
        orb={action(x,g) for g in group}
        assert orb<=remaining
        orbits.append(orb)
        remaining-=orb
    assert len(orbits)==13
    assert sorted(map(len,orbits))==sorted([1,12,60,120,40,60,120,60,120,60,12,40,24])

    caps=[]
    for mask in range(1<<len(orbits)):
        if sum(len(o) for i,o in enumerate(orbits) if mask>>i&1)!=112:
            continue
        S={x for i,o in enumerate(orbits) if mask>>i&1 for x in o}
        try:verify(S,6)
        except ValueError:continue
        caps.append((mask,S))
    assert len(caps)==2
    C,D=caps[0][1],caps[1][1]
    assert len(C)==len(D)==112 and C.isdisjoint(D)
    shadow={tuple((-a-b)%3 for a,b in zip(x,y)) for x in C for y in D}
    zero=(0,)*6
    assert shadow==set(itertools.product(range(3),repeat=6))-{zero}
    lifted={ (0,)+p for p in C }|{ (1,)+p for p in D }|{(2,)+zero}
    assert verify(lifted,7)==225
    return {
      "special_45_45_22_normals":56,
      "basis_rank_mod3":6,
      "basis":[list(x) for x in basis],
      "weight_histogram":dict(sorted(weights.items())),
      "paley_symmetric_W":[list(x) for x in W],
      "W_squared_mod3":"2*Identity6",
      "signed_permutation_group_order":240,
      "full_space_orbits":len(orbits),
      "orbit_sizes":[len(o) for o in orbits],
      "size_112_cap_orbit_unions":2,
      "disjoint_cap_orbit_indices":[[i for i in range(13) if mask>>i&1] for mask,_ in caps],
      "cross_sum_shadow_size":len(shadow),
      "missing_from_cross_sum":[0,0,0,0,0,0],
      "lifted_seven_dimensional_cap":225,
      "status":"independently verified known C6 structure, not new open-problem result"
    }

if __name__=="__main__":
    print(json.dumps(audit(),indent=2,sort_keys=True))
