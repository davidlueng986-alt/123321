#!/usr/bin/env python3
"""Independent reproduction of Edel's known 496-cap in F3^8.

The six-dimensional 112/112/12 fibers from the verified 236-cap
are paired with these two-dimensional prefix sets:
 B1={(0,1),(0,2)}, B2={(1,0),(2,0)}, B0={1,2}^2.
Cardinality is 224+224+48=496, strictly BELOW known 512 record.

Source: Math Agent 2026-11-01 Campaign 001 v2.0; Edel's
2004 Property-(ER) lengthening construction. No novelty claim.
"""
from generate_calderbank_fishburn import construction
from verify_capset import verify

def construct():
    A=construction()
    H0=[p[1:] for p in A if p[0]==0]
    H1=[p[1:] for p in A if p[0]==1]
    U =[p[1:] for p in A if p[0]==2]
    B1=[(0,1),(0,2)]
    B2=[(1,0),(2,0)]
    B0=[(1,1),(1,2),(2,1),(2,2)]
    cap=([b+p for b in B1 for p in H0]+
         [b+p for b in B2 for p in H1]+
         [b+p for b in B0 for p in U])
    assert verify(cap,8)==496
    return cap

if __name__=="__main__":
    print("VERIFIED known Edel 496-cap in F3^8:",verify(construct(),8))
