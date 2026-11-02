#!/usr/bin/env python3
"""E033 constructive proof witness for row1 cycle-type normalization.
For any VALID 3-MOLS, maps first row of each square to identity,
first column of A to identity, and A row1 to canonical cycle type.
Pure Python, no solver; n=4 GF(4) and prime-order controls.
"""
from collections import defaultdict
def cycles(f):
    seen=set();out=[]
    for x in range(len(f)):
        if x not in seen:
            c=[];y=x
            while y not in seen:
                seen.add(y);c.append(y);y=f[y]
            assert y==x;out.append(c)
    return out
def canonical(lengths):
    out=[];s=0
    for k in sorted(lengths,reverse=True):
        out.extend(s+(i+1)%k for i in range(k));s+=k
    return out
def validate(S):
    n=len(S[0]);assert len(S)==3
    target=set(range(n))
    for A in S:
        assert len(A)==n and all(set(row)==target for row in A)
        assert all({A[r][c] for r in range(n)}==target for c in range(n))
    for a,b in ((0,1),(0,2),(1,2)):
        assert len({(S[a][r][c],S[b][r][c]) for r in range(n) for c in range(n)})==n*n
    return True
def normalize(S):
    validate(S);n=len(S[0]);Z=[]
    for A in S:
        rename={A[0][c]:c for c in range(n)}
        Z.append([[rename[v] for v in row] for row in A])
    idx={Z[0][r][0]:r for r in range(n)}
    Z=[[A[idx[r]][:] for r in range(n)] for A in Z]
    f=Z[0][1];group=defaultdict(list)
    for cyc in cycles(f):group[len(cyc)].append(cyc)
    pi=[v for k in sorted(group,reverse=True) for cyc in group[k] for v in cyc]
    inv={v:i for i,v in enumerate(pi)}
    T=[[[inv[A[r][pi[c]]] for c in range(n)] for r in range(n)] for A in Z]
    idx={T[0][r][0]:r for r in range(n)}
    T=[[A[idx[r]][:] for r in range(n)] for A in T]
    target=canonical([len(c) for c in cycles(f)])
    assert T[0][1]==target and T[0][0]==list(range(n))
    assert all(T[0][r][0]==r for r in range(n))
    if T[1][1][0]>T[2][1][0]:T[1],T[2]=T[2],T[1]
    validate(T)
    return T,target
def gf4mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return z
def controls():
    S4=[[[r^gf4mul(a,c) for c in range(4)] for r in range(4)] for a in (1,2,3)]
    for n,S in [(4,S4)]+[(n,[[[(r+a*c)%n for c in range(n)] for r in range(n)] for a in (1,2,3)]) for n in (5,7,11)]:
        T,f=normalize(S);assert validate(T)
        print(n,f,[n*n]*3)
if __name__=='__main__':controls()
