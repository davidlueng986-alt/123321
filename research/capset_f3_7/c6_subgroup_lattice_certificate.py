#!/usr/bin/env python3
"""CAP-004D: exact subgroup structure of the Paley signed-permutation stabilizer.

This proves that the derived order-60 subgroup has exactly the same point
orbits on F3^6 as the previously certified order-120 subgroup. Thus its
restricted 7D cap optimum is ALSO 236. It additionally rules out order-40
subgroups of this particular 120-group, and constructs an order-24 subgroup.
Pure stdlib, deterministic; NOT a global r3(7) bound.
"""
import itertools
import json
from collections import Counter
from paley_magic_basis_240_certificate import H, basis, dot, action
from verify_capset import verify

T = {tuple(dot(n, p) for n in basis) for p in H}
assert len(T) == 112 and verify(T, 6) == 112

def parity(p):
    return sum(p[i] > p[j] for i in range(6) for j in range(i+1, 6)) % 2

G = [(p, m) for p in itertools.permutations(range(6))
     for m in range(64) if all(action(x, (p, m)) in T for x in T)]
assert len(G) == 240
assert all(parity(p) == m.bit_count() % 2 for p, m in G)
E = [g for g in G if parity(g[0]) == 0]
assert len(E) == 120

def compose(a, b):  # Apply a first, then b.
    p, m = a
    q, n = b
    return (tuple(q[p[i]] for i in range(6)),
            sum(((m >> i & 1) ^ (n >> p[i] & 1)) << i for i in range(6)))

index = {g: i for i, g in enumerate(E)}
identity = index[(tuple(range(6)), 0)]
mul = [[index[compose(a, b)] for b in E] for a in E]
inv = [next(j for j in range(120)
            if mul[i][j] == identity and mul[j][i] == identity)
       for i in range(120)]
assert all(action(action(x, a), b) == action(x, compose(a, b))
           for x in itertools.product(range(3), repeat=6)
           for a, b in ((E[3], E[7]), (E[17], E[53]), (E[71], E[119])))

def closure(generators, cutoff=120):
    seen = {identity}
    todo = [identity]
    while todo:
        x = todo.pop()
        for g in generators:
            y = mul[x][g]
            if y not in seen:
                seen.add(y)
                if len(seen) > cutoff:
                    return seen
                todo.append(y)
    return seen

def commutators(subset):
    return {mul[mul[mul[i][j]][inv[i]]][inv[j]]
            for i in subset for j in subset}

D = closure(commutators(range(120)))
assert len(D) == 60
assert closure(commutators(D)) == D  # D is perfect.
center = {i for i in range(120)
          if all(mul[i][j] == mul[j][i] for j in range(120))}
assert len(center) == 2 and len(center & D) == 1

def order(i):
    x = identity
    for k in range(1, 121):
        x = mul[x][i]
        if x == identity:
            return k
    raise AssertionError("element order exceeds group order")

assert Counter(order(i) for i in range(120)) == {
    1: 1, 2: 31, 3: 20, 5: 24, 6: 20, 10: 24}

space = set(itertools.product(range(3), repeat=6))
def orbit_partition(subgroup):
    remaining = set(space)
    result = []
    while remaining:
        seed = min(remaining)
        orbit = {action(seed, E[i]) for i in subgroup}
        assert orbit <= remaining
        result.append(orbit)
        remaining -= orbit
    return result

orbits60 = orbit_partition(D)
orbits120 = orbit_partition(range(120))
assert len(orbits60) == len(orbits120) == 21
assert {frozenset(o) for o in orbits60} == {
    frozenset(o) for o in orbits120}
# Invariant subsets of each of the three 6D slices therefore coincide,
# so the already CI-certified order-120 restricted optimum 236 transfers
# verbatim to the order-60 derived subgroup. No new 7D search is needed.

# An order-40 subgroup would have index three in E. Its coset action gives
# a transitive homomorphism E -> S3. But D=[E,E] is perfect, so its image
# in S3 must be trivial; E/D has order 2 and cannot act transitively on 3
# cosets. Therefore E has no order-40 subgroup.

# Explicitly construct an order-24 subgroup: first find order-12 in D,
# then adjoin the central involution not in D.
z = next(i for i in center if i != identity)
found = None
for a in sorted(i for i in D if order(i) == 3):
    for b in sorted(i for i in D if order(i) == 2):
        if len(closure((a, b), cutoff=12)) == 12:
            found = (a, b, closure((a, b, z)))
            break
    if found is not None:
        break
assert found is not None and len(found[2]) == 24
orbits24 = orbit_partition(found[2])
assert len(orbits24) == 45
assert Counter(map(len, orbits24)) == {1: 1, 6: 4, 8: 4, 12: 16, 24: 20}

# Direct coordinate-level 6D cap-validity audit of individual 24-orbits.
def orbit_is_cap(o):
    for a, b in itertools.combinations(o, 2):
        if tuple((-x-y) % 3 for x, y in zip(a, b)) in o:
            return False
    return True
assert sum(map(orbit_is_cap, orbits24)) == 33

print(json.dumps({
    "status": "VERIFIED_FINITE_GROUP_COMPUTATION_RESTRICTED_ONLY",
    "even_subgroup_order": 120, "derived_subgroup_order": 60,
    "derived_is_perfect": True, "center_order": 2,
    "order_60_and_120_orbit_partitions_identical": True,
    "order_60_orbit_count": len(orbits60),
    "order_60_restricted_optimum_inherited_from_CAP_004C": 236,
    "order_40_subgroup_possible": False,
    "order_24_subgroup_exists": True,
    "order_24_generators": [E[found[0]], E[found[1]]],
    "order_24_orbit_count": len(orbits24),
    "order_24_orbit_size_distribution": dict(Counter(map(len, orbits24))),
    "order_24_individually_cap_valid_orbits": 33,
    "no_global_bound_claim": True
}, indent=2, sort_keys=True))
