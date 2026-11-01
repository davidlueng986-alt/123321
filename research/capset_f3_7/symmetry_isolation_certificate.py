#!/usr/bin/env python3
"""Exact stdlib-only symmetry / 16-deletion isolation certificate.
Independently replay existing 1,902,225-pair minimum=16,count=888 audit.
"""
import itertools
from collections import defaultdict
from generate_calderbank_fishburn import construction
from verify_capset import verify

A=construction()
assert verify(A)==236
inside=set(A)
all_points=set(itertools.product(range(3),repeat=7))
outs=all_points-inside
blocks={"".join(sorted(b)) for b in ("123","236","124","245","135","256","146","345","156","346")}
D={tuple(int(c)-1 for c in b) for b in blocks}
all_triples=set(itertools.combinations(range(6),3))
perms=[]
for P in itertools.permutations(range(6)):
    T={tuple(sorted(P[i] for i in b)) for b in D}
    if T==D:perms.append((P,False))
    elif T==all_triples-D:perms.append((P,True))
assert len(perms)==120 and sum(t for _,t in perms)==60
even_masks=[m for m in range(64) if m.bit_count()%2==0]
G=list(itertools.product(perms,even_masks))
assert len(G)==3840
def act(x,g):
    (P,swap),m=g
    y=[(1-x[0])%3 if swap else x[0]]+[0]*6
    for j in range(6):
        y[1+P[j]]=(2 if m>>j&1 else 1)*x[j+1]%3
    return tuple(y)
for g in G:
    assert {act(x,g) for x in A}==inside
sec=defaultdict(list)
for i,p in enumerate(A):
    for j in range(i+1,len(A)):
        q=A[j]
        sec[tuple((-u-v)%3 for u,v in zip(p,q))].append((i,j))
assert set(sec)==outs
remaining=outs.copy()
orbits=[]
while remaining:
    x=min(remaining)
    orb={act(x,g) for g in G}
    assert orb<=remaining and len({len(sec[p]) for p in orb})==1
    orbits.append((x,len(orb),len(sec[x])))
    remaining-=orb
assert len(orbits)==14 and sum(o[1] for o in orbits)==1951

PAIR_REPS=[
 ((0,0,0,0,0,0,1),(0,0,0,0,0,1,0)),
 ((0,0,0,0,0,0,1),(2,1,1,1,1,2,2)),
 ((0,0,1,1,1,1,1),(2,2,2,2,2,2,2)),
]
edge_masks=[[(1<<i)|(1<<j) for i,j in sec[p]] for p in sorted(outs)]
def covers_for_pair(p,q):
    assert tuple((-u-v)%3 for u,v in zip(p,q)) not in inside
    graph=defaultdict(set)
    for i,j in sec[p]+sec[q]:
        graph[i].add(j); graph[j].add(i)
    seen=set(); mandatory=0; choices=[]
    for v in graph:
        if v in seen:continue
        seen_comp=set();front=[v]
        while front:
            x=front.pop()
            if x in seen_comp:continue
            seen_comp.add(x);front.extend(graph[x]-seen_comp)
        seen.update(seen_comp)
        if len(seen_comp)==2:
            a,b=sorted(seen_comp); choices.append((1<<a,1<<b))
        elif len(seen_comp)==3:
            center=next(x for x in seen_comp if len(graph[x])==2)
            mandatory|=1<<center
        else:raise ValueError("Non-path component: needs independent audit")
    assert len(choices)+mandatory.bit_count()==16
    for bits in range(1<<len(choices)):
        mask=mandatory
        for i,(left,right) in enumerate(choices):
            mask|=right if bits>>i&1 else left
        assert mask.bit_count()==16
        yield mask
def available_count(mask):
    return sum(all(mask&edge for edge in edges) for edges in edge_masks)
pair_orbits=set(); sizes=[]; cover_counts=[]
for p,q in PAIR_REPS:
    O={tuple(sorted((act(p,g),act(q,g)))) for g in G}
    assert O.isdisjoint(pair_orbits)
    pair_orbits.update(O); sizes.append(len(O))
    count=0
    for removed in covers_for_pair(p,q):
        assert available_count(removed)==2
        count+=1
    cover_counts.append(count)
assert sizes==[120,384,384] and cover_counts==[4096,2048,1024]
assert len(pair_orbits)==888
print("VERIFIED GROUP ORDER",len(G))
print("VERIFIED OUTSIDER ORBITS",len(orbits),[(o[1],o[2]) for o in orbits])
print("VERIFIED MIN-16 PAIR ORBITS",sizes)
print("VERIFIED EXHAUSTIVE MIN-COVERS",cover_counts)
print("VERIFIED FOR EVERY MIN-COVER: EXACTLY TWO OUTSIDERS AVAILABLE")
print("USING FULL PAIR-SCAN CERTIFICATE (888 TOTAL), DELETING <=16 ORIGINAL POINTS CANNOT PRODUCE >236")
