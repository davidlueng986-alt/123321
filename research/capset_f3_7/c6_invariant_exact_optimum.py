#!/usr/bin/env python3
"""Exact restricted theorem: max size of a 240-signed-permutation-invariant
cap in F_3^7, with group acting on the last six coordinates, is 225.

Pure Python integer enumeration; no MILP, numerical optimizer, or randomness.
The group is the exact subgroup preserving the known 112-point 6D cap
in the independently verified Paley magic-basis coordinates.
This is NOT a global upper bound for r_3(7).
"""
from itertools import permutations, product
from paley_magic_basis_240_certificate import H, basis, dot, action
from verify_capset import verify

T={tuple(dot(n,p) for n in basis) for p in H}
assert len(T)==112 and verify(T,6)==112
G=[(perm,mask) for perm in permutations(range(6)) for mask in range(64)
   if all(action(x,(perm,mask)) in T for x in T)]
assert len(G)==240
remaining=set(product(range(3),repeat=6))
orbits=[]
while remaining:
    seed=min(remaining)
    orb={action(seed,g) for g in G}
    assert orb<=remaining
    orbits.append(orb)
    remaining-=orb
assert len(orbits)==13
sizes=[len(o) for o in orbits]
point_orbit={p:i for i,o in enumerate(orbits) for p in o}
assert len(point_orbit)==729

# An internal line has three DISTINCT 6D points; a cross-slice line
# has three distinct 7D points even if their six-coordinate tails agree.
internal=set()
cross=set()
points=list(product(range(3),repeat=6))
for a in points:
    ia=point_orbit[a]
    for b in points:
        c=tuple((-x-y)%3 for x,y in zip(a,b))
        ib,ic=point_orbit[b],point_orbit[c]
        cross.add((ia,ib,ic))
        if a!=b:
            internal.add(tuple(sorted((ia,ib,ic))))
assert len(internal)==247 and len(cross)==1195

# Exact classification of all possible orbit-union caps in ONE slice.
valid=[]
for mask in range(1<<13):
    if all(not all(mask>>i&1 for i in set(t)) for t in internal):
        valid.append(mask)
assert len(valid)==22
weight=lambda m:sum(sizes[i] for i in range(13) if m>>i&1)
assert max(map(weight,valid))==112

# The 6D cross-sum shadow of two orbit-union slices is an orbit union.
shadow=[[0]*13 for _ in range(13)]
for i,j,k in cross:
    shadow[i][j]|=1<<k
def forbidden(m0,m1):
    bits=0
    for i in range(13):
        if m0>>i&1:
            for j in range(13):
                if m1>>j&1:
                    bits|=shadow[i][j]
    return bits

# Subset-max dynamic programming: for any allowed-orbit mask, return
# the largest internally cap-valid submask. Exhaust all 22*23/2=253
# unordered first-two-slice pairs; every 3-slice cap can permute slices
# so its first two masks are one such pair.
N=1<<13
best=[-1]*N
arg=[0]*N
for m in valid:
    best[m]=weight(m)
    arg[m]=m
for i in range(13):
    for m in range(N):
        if m>>i&1 and best[m^(1<<i)]>best[m]:
            best[m]=best[m^(1<<i)]
            arg[m]=arg[m^(1<<i)]
opt=-1
witness=None
tested=0
for a,m0 in enumerate(valid):
    for m1 in valid[a:]:
        tested+=1
        allowed=(N-1)^forbidden(m0,m1)
        score=weight(m0)+weight(m1)+best[allowed]
        if score>opt:
            opt=score
            witness=(m0,m1,arg[allowed])
assert tested==253 and opt==225
assert sorted(map(weight,witness))==[1,112,112]

# Independent direct exact 7D triple verification of the optimum witness.
candidate=[(k,)+p for k,m in enumerate(witness)
           for i,o in enumerate(orbits) if m>>i&1 for p in o]
assert verify(candidate,7)==225
print("VERIFIED RESTRICTED THEOREM: 240-invariant F3^7 cap optimum=225")
print("group=240; orbit_sizes=",sizes)
print("internal_orbit_triples=247; cross_orbit_triples=1195")
print("valid_single_slice_orbit_unions=22; exhaustive_pairs=253")
print("witness_masks=",witness,"slice_sizes=",list(map(weight,witness)))
print("independent_direct_triple_checker=PASS; no global r3(7) claim")
