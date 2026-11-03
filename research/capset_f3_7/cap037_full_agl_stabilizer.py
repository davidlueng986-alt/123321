#!/usr/bin/env python3
"""CAP037: exact full AGL(4,3) stabilizer of CAP027 occupancy, stdlib."""
from itertools import product
Q=list(product(range(3),repeat=4))
E={q for q in Q if q[0]==q[1]==0}
S={Q[(7*i)%81] for i in range(11)}
f={q:3+int(q in E)+3*int(q in S) for q in Q}
assert sorted([f[q] for q in Q]).count(7)==2
assert {q for q in Q if f[q] in (4,7)}==E
V=list(product(range(3),repeat=2))
def mv(M,v):
    return ((M[0]*v[0]+M[1]*v[1])%3,(M[2]*v[0]+M[3]*v[1])%3)
GL=[m for m in product(range(3),repeat=4) if (m[0]*m[3]-m[1]*m[2])%3]
assert len(GL)==48
h=(2,1)
pairs=[(D,t) for D in GL for t in V
       if {t,tuple((mv(D,h)[j]+t[j])%3 for j in range(2))}=={(0,0),h}]
assert len(pairs)==12
high6={q for q in Q if f[q]==6}
found=[];tested=0
for A in GL:
    for C in product(range(3),repeat=4):
        for D,t in pairs:
            tested+=1
            mapped=set()
            for q in high6:
                x,y=q[:2],q[2:]
                ax=mv(A,x);cx=mv(C,x);dy=mv(D,y)
                mapped.add(ax+tuple((cx[j]+dy[j]+t[j])%3 for j in range(2)))
            if mapped==high6:
                found.append((A,C,D,t))
assert tested==46656
assert found==[((1,0,0,1),(0,0,0,0),(1,0,0,1),(0,0))]
print('PASS full AGL4 stabilizer = identity; tested',tested,'candidates; no seed')
