#!/usr/bin/env python3
"""CAP-004G: deterministic exact orbit-mask and cross-shadow data for C++ checker.

Every orbit-union cap in each of the three slices is enumerated; the C++
checker exhausts every size-ordered slice pair that could reach 237.
Only the specific order-24 invariant family is covered.
"""
import argparse
import contextlib
import hashlib
import io
import itertools
import json
from pathlib import Path

with contextlib.redirect_stdout(io.StringIO()):
    import c6_subgroup_lattice_certificate as subgroup
from verify_capset import verify

orbits = subgroup.orbits24
orbits120 = subgroup.orbits120
assert len(orbits) == 45 and len(orbits120) == 21
space = list(itertools.product(range(3), repeat=6))
orbit_of = {p: i for i, orbit in enumerate(orbits) for p in orbit}
orbit120_of = {p: i for i, orbit in enumerate(orbits120) for p in orbit}
assert len(orbit_of) == len(orbit120_of) == 729
weights = [len(o) for o in orbits]
n = len(orbits)

forbidden = set()
for a in space:
    i = orbit_of[a]
    for b in space:
        if a == b:
            continue
        c = tuple((-u-v) % 3 for u, v in zip(a, b))
        forbidden.add(sum(1 << j for j in {i, orbit_of[b], orbit_of[c]}))
assert len(forbidden) == 3556
forced_out = {i for f in forbidden if f.bit_count() == 1
              for i in range(n) if (f >> i) & 1}
assert len(forced_out) == 12
free = [i for i in range(n) if i not in forced_out]
free.sort(key=lambda i: sum((f >> i) & 1 for f in forbidden), reverse=True)
by_bit = {i: [f for f in forbidden if (f >> i) & 1] for i in free}
valid = []
nodes = 0

def enumerate_valid(pos, mask, weight):
    global nodes
    nodes += 1
    if pos == len(free):
        valid.append((mask, weight))
        return
    enumerate_valid(pos + 1, mask, weight)
    i = free[pos]
    nxt = mask | (1 << i)
    if all((f & nxt) != f for f in by_bit[i]):
        enumerate_valid(pos + 1, nxt, weight + weights[i])

enumerate_valid(0, 0, 0)
assert nodes == 87862 and len(valid) == 11434
assert max(w for _, w in valid) == 112
valid.sort(key=lambda item: (-item[1], item[0]))

shadow = [[0] * n for _ in range(n)]
for a in space:
    i = orbit_of[a]
    for b in space:
        j = orbit_of[b]
        c = tuple((-u-v) % 3 for u, v in zip(a, b))
        shadow[i][j] |= 1 << orbit_of[c]

# Independently replay a 236-point order-120-invariant witness.
masks120 = (462848, 344128, 1048576)
candidate = []
for s in range(3):
    for orbit in orbits:
        ids = {orbit120_of[p] for p in orbit}
        assert len(ids) == 1
        if masks120[s] & (1 << next(iter(ids))):
            candidate.extend((s,) + p for p in orbit)
assert verify(candidate, 7) == 236
assert sorted(sum(1 for p in candidate if p[0] == s) for s in range(3)) == [12, 112, 112]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="ascii", newline="\n") as f:
        f.write(f"{len(valid)}\n")
        for mask, weight in valid:
            f.write(f"{mask} {weight}\n")
        for row in shadow:
            f.write(" ".join(map(str, row)) + "\n")
    print(json.dumps({
        "status": "EXACT_ORDER24_INPUT_GENERATED",
        "valid_slice_masks": len(valid),
        "enumeration_nodes": nodes,
        "orbit_count": n,
        "within_forbidden_masks": len(forbidden),
        "max_slice": 112,
        "known_236_direct_arithmetic": "PASS",
        "data_sha256": hashlib.sha256(output.read_bytes()).hexdigest()
    }, sort_keys=True))

if __name__ == "__main__":
    main()
