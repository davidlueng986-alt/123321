#!/usr/bin/env python3
"""CAP038 independent base-3 arithmetic audit of CAP035 triple clauses."""
from hashlib import sha256
N=3**7
def third(a,b):
    z=0; place=1
    for _ in range(7):
        z+=((-a%3-b%3)%3)*place
        a//=3;b//=3;place*=3
    return z
def audit():
    h=sha256(); n=inside=outside=0
    for a in range(N):
        for b in range(a+1,N):
            c=third(a,b)
            if c<=b:continue
            n+=1
            if a//27==b//27==c//27:inside+=1
            else:
                assert len({a//27,b//27,c//27})==3
                outside+=1
            h.update(f"{-a-1} {-b-1} {-c-1} 0\n".encode())
    assert (n,inside,outside)==(796797,9477,787320)
    digest=h.hexdigest()
    assert digest=="d9be134e726c3d84cbb8ac7ca6ef23c37fd6571d45953c9c742927ab5491c3a8"
    print("CAP038 PASS",n,inside,outside,digest)
if __name__=="__main__":audit()
