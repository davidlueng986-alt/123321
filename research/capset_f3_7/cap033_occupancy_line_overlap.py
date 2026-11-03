#!/usr/bin/env python3
"""CAP-033: exact quotient-line incidence audit of CAP027 formal 285 counts.
This checks only an occupancy relaxation, NEVER an actual cap.
CPU-only deterministic; Python standard library.
"""
from itertools import product
from collections import Counter

def audit():
    points=list(product(range(3),repeat=4))
    E={x for x in points if x[0]==x[1]==0}
    S={points[(7*i)%81] for i in range(11)}
    f={x:3+int(x in E)+3*int(x in S) for x in points}
    lines=set()
    for a in points:
        for b in points:
            if a==b: continue
            c=tuple((-u-v)%3 for u,v in zip(a,b))
            lines.add(tuple(sorted((a,b,c))))
    profiles=Counter(tuple(sorted((f[x] for x in line),reverse=True)) for line in lines)
    assert len(lines)==1080 and sum(f.values())==285
    assert Counter(f.values())=={3:63,4:7,6:9,7:2}
    assert profiles[(7,6,6)]==1 and profiles[(7,7,4)]==1
    special={}
    for line in lines:
        typ=tuple(sorted((f[x] for x in line),reverse=True))
        if typ in ((7,6,6),(7,7,4)):
            special[typ]=tuple(sorted((x,f[x]) for x in line))
    shared=set(x for x,n in special[(7,6,6)] if n==7) & set(x for x,n in special[(7,7,4)] if n==7)
    assert shared=={(0,0,0,0)}
    assert special[(7,6,6)]==(((0,0,0,0),7),((1,0,0,1),6),((2,0,0,2),6))
    assert special[(7,7,4)]==(((0,0,0,0),7),((0,0,1,2),4),((0,0,2,1),7))
    print('PASS 1080 lines; profiles',sorted(profiles.items()))
    print('PASS shared 7-fiber',sorted(shared))
    return special

if __name__=='__main__': audit()
