#!/usr/bin/env python3
"""CAP-004E bounded exact order-24-invariant high-slice search.

Exhausts all 24-invariant 7D caps whose first TWO slices each have >=104
points, up to slice permutation. Proves restricted optimum 236, NOT global.
Pure stdlib, deterministic, CPU only. Uses separately certified subgroup.
"""
import contextlib
import io
import itertools
import json
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    import c6_subgroup_lattice_certificate as subgroup
from verify_capset import verify

orbits = subgroup.orbits24
space = list(itertools.product(range(3), repeat=6))
N = len(orbits)
assert N == 45
point_orbit = {p:i for i,o in enumerate(orbits) for p in o}
assert len(point_orbit) == 729
weights = [len(o) for o in orbits]

# Within-slice forbidden orbit masks. For distinct a,b the third point
# c=-a-b is also distinct. One forbidden bit mask means that every union
# containing those orbits violates the cap condition.
forbidden = set()
for a in space:
    i = point_orbit[a]
    for b in space:
        if a == b:
            continue
        j = point_orbit[b]
        c = tuple((-x-y)%3 for x,y in zip(a,b))
        forbidden.add(sum(1<<k for k in {i,j,point_orbit[c]}))
assert len(forbidden) == 3556
forced_out = {i for f in forbidden if f.bit_count() == 1
              for i in range(N) if (f>>i)&1}
assert len(forced_out) == 12
free = [i for i in range(N) if i not in forced_out]
free.sort(key=lambda i:sum((f>>i)&1 for f in forbidden),reverse=True)
by_bit = {i:[f for f in forbidden if (f>>i)&1] for i in free}
valid = []
nodes = 0

def enumerate_valid(pos, mask, weight):
    global nodes
    nodes += 1
    if pos == len(free):
        valid.append((mask,weight))
        return
    enumerate_valid(pos+1,mask,weight)
    i = free[pos]
    nxt = mask | (1<<i)
    if all((f & nxt) != f for f in by_bit[i]):
        enumerate_valid(pos+1,nxt,weight+weights[i])

enumerate_valid(0,0,0)
assert nodes == 87862 and len(valid) == 11434
assert max(w for _,w in valid) == 112
valid.sort(key=lambda item:item[1],reverse=True)
high = [(mask,w) for mask,w in valid if w >= 104]
assert len(high) == 144
assert Counter(w for _,w in high) == {112:48,104:96}

# Cross-slice shadow: choosing orbit i in slice 0 and orbit j in slice 1
# excludes every orbit k in slice 2 for which a+b+c=0 for some a,b,c.
shadow = [[0]*N for _ in range(N)]
for a in space:
    i = point_orbit[a]
    for b in space:
        j = point_orbit[b]
        c = tuple((-x-y)%3 for x,y in zip(a,b))
        shadow[i][j] |= 1<<point_orbit[c]

best = -1
witness = None
pairs = 0
max_third = -1
for ia,(ma,wa) in enumerate(high):
    for mb,wb in high[ia:]:
        pairs += 1
        blocked = 0
        x = ma
        while x:
            bit = x & -x
            i = bit.bit_length()-1
            x -= bit
            y = mb
            while y:
                bit2 = y & -y
                j = bit2.bit_length()-1
                y -= bit2
                blocked |= shadow[i][j]
        allowed = ((1<<N)-1)^blocked
        for mc,wc in valid:  # descending: first feasible is optimal third
            if (mc & ~allowed) == 0:
                max_third = max(max_third,wc)
                score = wa+wb+wc
                if score > best:
                    best = score
                    witness = (ma,mb,mc)
                break

assert pairs == 144*145//2 == 10440
assert best == 236 and max_third == 16
candidate = [(s,)+p for s,mask in enumerate(witness)
             for i,o in enumerate(orbits) if (mask>>i)&1 for p in o]
assert verify(candidate,7) == 236  # separate direct arithmetic checker
slice_sizes = [sum(weights[i] for i in range(N) if (m>>i)&1)
               for m in witness]
assert slice_sizes == [112,112,12]
print(json.dumps({
    "status":"VERIFIED_RESTRICTED_HIGH_SLICE_THEOREM_NOT_GLOBAL",
    "subgroup_order":24,"orbit_count":45,
    "internal_forbidden_orbit_masks":len(forbidden),
    "forced_out_orbits":len(forced_out),
    "valid_single_slice_masks":len(valid),
    "search_nodes":nodes,
    "high_slice_threshold":104,
    "high_slice_masks":len(high),
    "unordered_high_slice_pairs_exhausted":pairs,
    "exact_optimum_when_two_slices_ge_104":best,
    "maximum_third_slice_over_tested_pairs":max_third,
    "witness_slice_sizes":slice_sizes,
    "witness_masks":witness,
    "independent_direct_7d_verifier":"PASS",
    "global_bound_improved":False
},indent=2,sort_keys=True))
