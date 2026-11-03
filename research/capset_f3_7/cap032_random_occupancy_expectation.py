#!/usr/bin/env python3
"""CAP-032 exact expected 3AP count for CAP-027 occupancy; no randomness."""
from itertools import product
from fractions import Fraction
from collections import Counter
P=list(product(range(3),repeat=4))
chosen={P[(7*i)%81] for i in range(11)}
f={q:3+int(q[0]==q[1]==0)+3*int(q in chosen) for q in P}
assert sum(f.values())==285 and Counter(f.values())=={3:63,4:7,6:9,7:2}
lines=[]
for i,q in enumerate(P):
    for j in range(i+1,len(P)):
        r=P[j];s=tuple((-a-b)%3 for a,b in zip(q,r))
        if P.index(s)>j:lines.append((q,r,s))
assert len(lines)==1080
sumabc=sum(f[q]*f[r]*f[s] for q,r,s in lines)
assert sumabc==46863
cross=Fraction(sumabc,27)
internal=sum((Fraction(117*k*(k-1)*(k-2),27*26*25) for k in f.values()),Fraction())
assert internal==Fraction(341,25)
assert cross==Fraction(5207,3)
assert internal+cross==Fraction(131198,75)
# Independent ordered-pair computation (6 orientations per quotient line)
ordered=sum(f[q]*f[r]*f[tuple((-a-b)%3 for a,b in zip(q,r))]
            for q in P for r in P if q!=r)
assert ordered==6*sumabc
print('CAP032 PASS',len(lines),sumabc,internal,cross,internal+cross)
