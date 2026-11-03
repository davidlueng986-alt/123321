#!/usr/bin/env python3
"""CAP035 full exact 3AP CNF and conditional 285 fiber occupancy; stdlib only."""
from itertools import product
from collections import Counter
from hashlib import sha256
Q=list(product(range(3),repeat=4)); U=list(product(range(3),repeat=3))
P=[q+u for q in Q for u in U]; IDX={p:i+1 for i,p in enumerate(P)}
def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
def triples():
    for i,a in enumerate(P):
        for j in range(i+1,len(P)):
            k=IDX[third(a,P[j])]-1
            if j<k:yield (-i-1,-j-1,-k-1)
def counts():
    E={q for q in Q if q[0]==q[1]==0}
    S={Q[(7*i)%81] for i in range(11)}
    return {q:3+int(q in E)+3*int(q in S) for q in Q}
def at_most(xs,k,start):
    n=len(xs)
    if k>=n:return [],start
    if k==0:return [(-x,) for x in xs],start
    s={(i,j):start+(i-1)*k+j-1 for i in range(1,n) for j in range(1,k+1)}
    nxt=start+(n-1)*k; out=[]
    for i in range(1,n):out.append((-xs[i-1],s[i,1]))
    for i in range(2,n):out.append((-s[i-1,1],s[i,1]))
    for j in range(2,k+1):
        for i in range(2,n):
            out.append((-xs[i-1],-s[i-1,j-1],s[i,j]))
            out.append((-s[i-1,j],s[i,j]))
    for i in range(2,n+1):out.append((-xs[i-1],-s[i-1,k]))
    for i in range(1,n):
        for j in range(i+1,k+1):out.append((-s[i,j],))
    return out,nxt
def encode(path):
    nvars=len(P); nclauses=0
    # Stream to temporary body; DIMACS header needs counts.
    import tempfile,os
    with tempfile.NamedTemporaryFile(mode='w',delete=False) as f:
        tmp=f.name
        def emit(c):
            nonlocal nclauses
            f.write(' '.join(map(str,c))+' 0\n');nclauses+=1
        for c in triples():emit(c)
        v=nvars+1
        for q in Q:
            xs=[IDX[q+u] for u in U]; k=counts()[q]
            for lits,t in ((xs,k),([-x for x in xs],27-k)):
                cs,v=at_most(lits,t,v)
                for c in cs:emit(c)
        nvars=v-1
    with open(path,'w') as out,open(tmp) as src:
        out.write(f'p cnf {nvars} {nclauses}\n')
        for line in src:out.write(line)
    os.unlink(tmp)
    return nvars,nclauses
def audit():
    assert len(P)==2187 and sum(counts().values())==285
    assert Counter(counts().values())=={3:63,4:7,6:9,7:2}
    h=sha256(); n=0
    for c in triples():
        assert len(set(c))==3 and all(-2187<=x<0 for x in c)
        h.update((' '.join(map(str,c))+' 0\n').encode());n+=1
    assert n==796797
    for size,k in ((3,1),(4,2),(4,3)):
        cc,v=at_most(list(range(1,size+1)),k,size+1)
        for bits in product((False,True),repeat=size):
            valid=False
            for aux in product((False,True),repeat=v-size-1):
                vals=(False,)+bits+aux
                if all(any(vals[abs(l)] if l>0 else not vals[-l] for l in c) for c in cc):
                    valid=True;break
            assert valid==(sum(bits)<=k)
    print('PASS',n,h.hexdigest(),'small cardinality exhaustive PASS; SAT UNKNOWN')
if __name__=='__main__':
    import sys
    audit()
    if len(sys.argv)>1:print('DIMACS',encode(sys.argv[1]))
