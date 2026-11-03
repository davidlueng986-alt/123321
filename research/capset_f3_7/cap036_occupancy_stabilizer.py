#!/usr/bin/env python3
"""CAP036: exact affine quotient occupancy stabilizer audit (stdlib, deterministic)."""
from itertools import product, permutations
from collections import Counter
Q=list(product(range(3),repeat=4))
E={q for q in Q if q[0]==q[1]==0}
S={Q[(7*i)%81] for i in range(11)}
C={q:3+int(q in E)+3*int(q in S) for q in Q}
assert Counter(C.values())=={3:63,4:7,6:9,7:2}
def shift(q,t):return tuple((q[i]+t[i])%3 for i in range(4))
def monomial(q,p,s):return tuple(s[i]*q[p[i]]%3 for i in range(4))
translations=[t for t in Q if all(C[q]==C[shift(q,t)] for q in Q)]
linear=[(p,s) for p in permutations(range(4)) for s in product((1,2),repeat=4)
        if all(C[q]==C[monomial(q,p,s)] for q in Q)]
# Also test all affine monomial maps (31,104 candidates); no assumption that
# separate linear and translation stabilizers imply the full affine result.
affine=[(p,s,t) for p in permutations(range(4)) for s in product((1,2),repeat=4)
        for t in Q if all(C[q]==C[shift(monomial(q,p,s),t)] for q in Q)]
assert translations==[(0,0,0,0)]
assert linear==[((0,1,2,3),(1,1,1,1))]
assert affine==[((0,1,2,3),(1,1,1,1),(0,0,0,0))]
print("PASS: 81 translations, 384 monomial maps, 31104 affine monomial maps; stabilizer identity only")
