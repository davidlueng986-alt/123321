#!/usr/bin/env python3
"""CAP039 independent constructive and UP audit of CAP035 Sinz counters."""
from itertools import product
from collections import Counter
import random, hashlib

def counter(xs,k,start):
    n=len(xs)
    if k==0:return [(-x,) for x in xs],start,{}
    assert 0<k<n
    s={(i,j):start+(i-1)*k+j-1 for i in range(1,n) for j in range(1,k+1)}
    out=[]
    for i in range(1,n):out.append((-xs[i-1],s[i,1]))
    for i in range(2,n):out.append((-s[i-1,1],s[i,1]))
    for j in range(2,k+1):
        for i in range(2,n):
            out.extend([(-xs[i-1],-s[i-1,j-1],s[i,j]),(-s[i-1,j],s[i,j])])
    for i in range(2,n+1):out.append((-xs[i-1],-s[i-1,k]))
    for i in range(1,n):
        for j in range(i+1,k+1):out.append((-s[i,j],))
    return out,start+(n-1)*k,s

def propagate(cs,values):
    values=dict(values)
    while True:
        changed=False
        for c in cs:
            if any(values.get(abs(l))==(l>0) for l in c):continue
            remaining=[l for l in c if abs(l) not in values]
            if not remaining:return True
            if len(remaining)==1:
                l=remaining[0];values[abs(l)]=(l>0);changed=True
        if not changed:return False

def main():
    Q=list(product(range(3),repeat=4))
    E={q for q in Q if q[0]==q[1]==0}
    S={Q[(7*i)%81] for i in range(11)}
    counts=[3+int(q in E)+3*int(q in S) for q in Q]
    assert Counter(counts)=={3:63,4:7,6:9,7:2} and sum(counts)==285
    rng=random.Random(390039)
    h=hashlib.sha256(); start=2188; nc=good=bad=0
    for fiber,k in enumerate(counts):
        xs0=list(range(27*fiber+1,27*(fiber+1)+1))
        for xs,t in ((xs0,k),([-x for x in xs0],27-k)):
            cs,end,aux=counter(xs,t,start)
            assert end-start==26*t
            for c in cs:h.update((' '.join(map(str,c))+' 0\n').encode())
            start=end;nc+=len(cs)
            cases=[(False,)*27,(True,)*27]
            for size in {0,1,t-1,t,t+1,27}:
                if 0<=size<=27:
                    for _ in range(12):
                        indices=set(rng.sample(range(27),size))
                        cases.append(tuple(i in indices for i in range(27)))
            for bits in cases:
                vals={abs(x):(bits[i] if x>0 else not bits[i]) for i,x in enumerate(xs)}
                if sum(bits)<=t:
                    vals.update({v:sum(bits[:i])>=j for (i,j),v in aux.items()})
                    assert all(any(vals[abs(l)]==(l>0) for l in c) for c in cs)
                    good+=1
                else:
                    assert propagate(cs,vals)
                    bad+=1
    assert start-1==59049 and nc==135561
    print('PASS counters=162 aux_end=59049 suffix_clauses=135561 valid=',good,
          'invalid_UP=',bad,'seed=390039 sha256=',h.hexdigest())

if __name__=='__main__':main()
