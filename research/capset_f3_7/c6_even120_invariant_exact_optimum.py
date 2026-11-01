#!/usr/bin/env python3
"""Exact optimum 236 for F3^7 caps invariant under an index-two order-120
subgroup of the verified Paley magic-basis signed-permutation group.

The subgroup is the even-permutation kernel. This is a RESTRICTED theorem,
not an upper bound on the unrestricted r_3(7). Pure stdlib, no randomness.
"""
import itertools
import json
from paley_magic_basis_240_certificate import H, basis, dot, action
from verify_capset import verify

T = {tuple(dot(n, p) for n in basis) for p in H}
assert len(T) == 112 and verify(T, 6) == 112

def parity(perm):
    return sum(perm[i] > perm[j] for i in range(6)
               for j in range(i + 1, 6)) % 2

G = [(p, mask) for p in itertools.permutations(range(6))
     for mask in range(64) if all(action(x, (p, mask)) in T for x in T)]
assert len(G) == 240
# Sign-mask parity equals permutation parity throughout this group.
assert all(parity(p) == (mask.bit_count() % 2) for p, mask in G)
subgroup = [g for g in G if parity(g[0]) == 0]
assert len(subgroup) == 120
space = list(itertools.product(range(3), repeat=6))
remaining = set(space)
orbits = []
while remaining:
    seed = min(remaining)
    orbit = {action(seed, g) for g in subgroup}
    assert orbit <= remaining
    orbits.append(orbit)
    remaining -= orbit
assert len(orbits) == 21
sizes = [len(o) for o in orbits]
point_orbit = {p: i for i, o in enumerate(orbits) for p in o}
assert len(point_orbit) == 729

# Distinct points within a slice, but different slices automatically
# distinguish points, even when their 6D tails coincide.
internal, cross = set(), set()
for a in space:
    i = point_orbit[a]
    for b in space:
        j = point_orbit[b]
        c = tuple((-x - y) % 3 for x, y in zip(a, b))
        k = point_orbit[c]
        cross.add((i, j, k))
        if a != b:
            internal.add(tuple(sorted((i, j, k))))
assert len(internal) == 780 and len(cross) == 4089

forbidden = {sum(1 << i for i in set(t)) for t in internal}
by_bit = [set() for _ in range(21)]
for f in forbidden:
    for i in range(21):
        if (f >> i) & 1:
            by_bit[i].add(f)

valid = []
def enumerate_valid(i, mask, weight):
    if i == 21:
        valid.append((mask, weight))
        return
    enumerate_valid(i + 1, mask, weight)
    bit = 1 << i
    if not any((f & (mask | bit)) == f for f in by_bit[i]):
        enumerate_valid(i + 1, mask | bit, weight + sizes[i])
enumerate_valid(0, 0, 0)
assert len(valid) == 174 and max(w for _, w in valid) == 112

shadow = [[0] * 21 for _ in range(21)]
for i, j, k in cross:
    shadow[i][j] |= 1 << k

# Exact subset-max DP: best[m] is maximum size of a cap-valid
# union of orbits contained in mask m.
N = 1 << 21
best = [-1] * N
arg = [0] * N
for mask, weight in valid:
    best[mask], arg[mask] = weight, mask
for i in range(21):
    bit = 1 << i
    for base in range(0, N, 2 * bit):
        for m in range(base + bit, base + 2 * bit):
            if best[m - bit] > best[m]:
                best[m], arg[m] = best[m - bit], arg[m - bit]

valid.sort(key=lambda x: x[1], reverse=True)
optimum, witness, tested = -1, None, 0
for a, (m0, w0) in enumerate(valid):
    for m1, w1 in valid[a:]:
        # Every third slice has at most 112 points. This safe upper
        # bound prunes pairs that cannot improve the current optimum.
        if w0 + w1 + 112 <= optimum:
            break
        blocked = 0
        x = m0
        while x:
            bit = x & -x
            i = bit.bit_length() - 1
            x -= bit
            y = m1
            while y:
                bit2 = y & -y
                j = bit2.bit_length() - 1
                y -= bit2
                blocked |= shadow[i][j]
        allowed = (N - 1) ^ blocked
        score = w0 + w1 + best[allowed]
        tested += 1
        if score > optimum:
            optimum, witness = score, (m0, m1, arg[allowed])
assert optimum == 236 and tested == 7598
slice_sizes = [sum(sizes[i] for i in range(21) if (m >> i) & 1)
               for m in witness]
assert sorted(slice_sizes) == [12, 112, 112]

# Independent coordinate-level verifier, not orbit-level constraints.
candidate = [(k,) + p for k, mask in enumerate(witness)
             for i, o in enumerate(orbits) if (mask >> i) & 1 for p in o]
assert verify(candidate, 7) == 236
print(json.dumps({
    "status": "VERIFIED_RESTRICTED_THEOREM_NOT_GLOBAL_BOUND",
    "subgroup_order": len(subgroup), "orbit_count": len(orbits),
    "orbit_sizes": sizes, "internal_classes": len(internal),
    "cross_classes": len(cross), "valid_slice_masks": len(valid),
    "exhaustive_pairs": len(valid) * (len(valid) + 1) // 2,
    "pairs_evaluated_after_safe_pruning": tested,
    "exact_restricted_optimum": optimum, "witness_masks": witness,
    "witness_slice_sizes": slice_sizes,
    "independent_direct_verifier": "PASS"
}, indent=2, sort_keys=True))
