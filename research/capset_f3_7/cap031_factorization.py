"""CAP031 exact affine-line decomposition, stdlib CPU-only; no randomness."""
from itertools import product
from math import comb
Q=list(product(range(3),repeat=4))
lines=set()
for a in Q:
    for b in Q:
        if a==b: continue
        c=tuple((-x-y)%3 for x,y in zip(a,b))
        lines.add(tuple(sorted((a,b,c))))
assert len(lines)==1080
assert all(len(set(L))==3 for L in lines)
same=81*(27*26//6)
cross=len(lines)*27*27
assert (same,cross,same+cross)==(9477,787320,796797)
assert same+cross==2187*2186//6
# Every quotient line has 729 distinct lifts indexed by two internal coordinates.
# For fibers i,j,k, lifted triple (i,u),(j,v),(k,-u-v) for u,v in F3^3.
U=list(product(range(3),repeat=3))
assert len({(u,v,tuple((-a-b)%3 for a,b in zip(u,v))) for u in U for v in U})==729
print("PASS",len(lines),same,cross,same+cross)
