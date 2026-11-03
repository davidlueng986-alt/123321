#!/usr/bin/env python3
"""CAP-034: exact five-fiber 30-point witness for the CAP027 two intersecting high-density quotient lines.
Deterministic stdlib; NOT a 285-point cap or a global bound.
"""
from itertools import combinations
W766 = [
(0,0,0,1),(0,0,2,2),(0,1,0,1),(0,1,2,0),(0,1,2,1),(0,2,0,0),(0,2,2,2),
(1,1,1,0),(1,1,1,2),(1,2,0,2),(1,2,1,0),(1,2,1,2),
(2,1,1,0),(2,1,1,1),(2,2,0,0),(2,2,1,0),(2,2,1,1),(1,1,2,0),(2,1,2,1)]
Q0=(0,0,0,0); Q1=(1,0,0,1); Q2=(2,0,0,2)
Q3=(0,0,2,1); Q4=(0,0,1,2)
A={p[1:] for p in W766 if p[0]==0}
B={p[1:] for p in W766 if p[0]==1}
C={p[1:] for p in W766 if p[0]==2}
D=A.copy()
E={(1,0,0),(2,0,2),(0,0,0),(0,1,1)}
def third(x,y): return tuple((-a-b)%3 for a,b in zip(x,y))
def check(P):
    assert len(P)==len(set(P))
    return all(third(x,y) not in P for x,y in combinations(P,2))
def audit():
    assert [len(x) for x in (A,B,C,D,E)]==[7,6,6,7,4]
    assert check(A) and check(B) and check(C) and check(D) and check(E)
    assert all(third(a,d) not in E for a in A for d in D)
    pieces=[{q+p for p in part} for q,part in zip((Q0,Q1,Q2,Q3,Q4),(A,B,C,D,E))]
    P=set().union(*pieces)
    assert len(P)==30 and check(P)
    # Independent check: all 30 choose 3 triples, sum-coordinate-wise zero.
    assert sum(all((x[i]+y[i]+z[i])%3==0 for i in range(7))
               for x,y,z in combinations(P,3))==0
    # Every quotient line among occupied fibers has either <=2 occupied fibers
    # or is one of the two designated lines.
    qs=(Q0,Q1,Q2,Q3,Q4)
    assert [(i,j,k) for i,j,k in combinations(range(5),3)
            if third(qs[i],qs[j])==qs[k]]==[(0,1,2),(0,3,4)]
    print('PASS: 30 distinct points, 0 collinear triples, profiles 7/6/6/7/4')
    return sorted(P)
if __name__=='__main__':audit()
