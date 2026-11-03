#!/usr/bin/env python3
"""CAP042 independent ten-leaf incidence census; CPU only, no SAT solving."""
from itertools import combinations
from collections import defaultdict

N=3**7
def digits(x):
    a=[0]*7
    for i in range(6,-1,-1):
        a[i],x=x%3,x//3
    return tuple(a)
def enc(a):
    v=0
    for x in a:v=3*v+x
    return v
def third(a,b):
    return enc(tuple((-x-y)%3 for x,y in zip(digits(a),digits(b))))
frame=[0]+[enc(tuple(int(j==i) for j in range(7))) for i in range(7)]
zero8={third(a,b) for a,b in combinations(frame,2)}
classes=defaultdict(list)
for p in range(N):
    if p%3:continue
    v=digits(p)
    lam=((1-sum(v))%3,)+v
    tag=(lam[7],)+tuple(lam[:7].count(x) for x in (0,1,2))
    if p not in frame and p not in zero8:classes[tag].append(p)
assert len(classes)==10 and sum(map(len,classes.values()))==701

def counter(n,k):
    a=sum(min(i,k) for i in range(1,n+1))
    return a,2*a-n+1

def census():
    out=[]
    for branch,(tag,points) in enumerate(sorted(classes.items())):
        S=set(frame+[points[0]])
        Z={third(a,b) for a,b in combinations(sorted(S),2)}
        assert len(S)==9 and not S&Z
        U=set(range(N))-S-Z
        dropped=set()
        for z in Z:
            for x in range(N):
                if x!=z:dropped.add(tuple(sorted((z,x,third(z,x)))))
        binary=set()
        for s in S:
            for x in U:
                y=third(s,x)
                if y in U:binary.add(tuple(sorted((s,x,y))))
        assert not binary&dropped
        ternary=796797-len(dropped)-len(binary)
        n=len(U);h=sum(p%3==0 for p in U)
        ag,cg=counter(n,228);ah,ch=counter(h,81)
        out.append(dict(branch=branch,tag=tag,ninth=points[0],zeros=len(Z),
            free=n,free_H=h,dropped=len(dropped),binary=len(binary),
            ternary=ternary,variables=n+ag+ah,
            clauses=len(binary)+ternary+cg+ch))
    assert [x['dropped'] for x in out]==[38718]*5+[38733,38718,38724,38724,37662]
    assert [x['binary'] for x in out]==[9513]*7+[9516,9516,9526]
    assert [x['clauses'] for x in out]==[1786028]*5+[1786013,1786028,1786022,1786022,1787700]
    return out
if __name__=='__main__':
    import json
    print(json.dumps(census(),indent=2))
