#!/usr/bin/env python3
"""CAP-006A: deterministic audit of 3D projections of the verified 236-cap.

Scope: occupancy distributions under full-rank linear maps F3^7 -> F3^3.
This is NOT an improved cap construction or an upper bound for r3(7).
CPU-only, standard library, seed 20261102 for the pseudorandom pilot.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "candidates" / "calderbank_fishburn_236.txt"
MASK32 = (1 << 32) - 1

def read_cap(path=FIXTURE):
    rows = path.read_text().splitlines()
    assert rows[0].strip() == "n: 7"
    cap = [tuple(int(c) for c in line.strip()) for line in rows[1:] if line.strip()]
    assert len(cap) == 236 and len(set(cap)) == 236
    assert all(len(p) == 7 and all(0 <= c <= 2 for c in p) for p in cap)
    return cap

def assert_cap(cap):
    # Independent direct arithmetic, no reuse of projective mapping code.
    S = set(cap)
    for a, b in itertools.combinations(cap, 2):
        z = tuple((-x-y) % 3 for x, y in zip(a, b))
        assert z not in S, (a, b, z)

def rank3(matrix):
    a = [list(row) for row in matrix]
    rank = 0
    for j in range(7):
        pivot = next((i for i in range(rank, 3) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        if a[rank][j] == 2:
            a[rank] = [(2 * x) % 3 for x in a[rank]]
        for i in range(3):
            if i != rank and a[i][j]:
                k = a[i][j]
                a[i] = [(x - k * y) % 3 for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == 3:
            break
    return rank

def project_count(cap, matrix):
    assert rank3(matrix) == 3
    count = [0] * 27
    for p in cap:
        a, b, c = [sum(x*y for x, y in zip(row, p)) % 3 for row in matrix]
        count[9*a + 3*b + c] += 1
    assert sum(count) == len(cap)
    return count

def concentration(count):
    return sum(c*c for c in count)

def coordinate_audit(cap):
    profiles = {}
    groups = {"contains_coordinate_zero": [], "excludes_coordinate_zero": []}
    for inds in itertools.combinations(range(7), 3):
        matrix = [[int(i == j) for j in range(7)] for i in inds]
        counts = project_count(cap, matrix)
        profile = tuple(sorted(counts))
        profiles.setdefault(profile, []).append("".join(map(str, inds)))
        groups["contains_coordinate_zero" if 0 in inds else "excludes_coordinate_zero"].append(
            {"triple": "".join(map(str, inds)), "Q": concentration(counts),
             "zero_fibers": counts.count(0)})
    assert sorted(len(v) for v in profiles.values()) == [15, 20]
    assert len(groups["contains_coordinate_zero"]) == 15
    assert len(groups["excludes_coordinate_zero"]) == 20
    assert {r["Q"] for r in groups["contains_coordinate_zero"]} == {2884}
    assert {r["Q"] for r in groups["excludes_coordinate_zero"]} == {2290}
    assert {r["zero_fibers"] for r in groups["contains_coordinate_zero"]} == {4}
    assert {r["zero_fibers"] for r in groups["excludes_coordinate_zero"]} == {0}
    return {"number_coordinate_projections": 35, "profiles": [
        {"count": len(triples), "triples": triples, "occupancy_sorted": list(prof),
         "Q": sum(v*v for v in prof), "zero_fibers": prof.count(0)}
        for prof, triples in sorted(profiles.items(), key=lambda x: len(x[1]))]}

def random_audit(cap, seed=20261102, samples=512):
    state = seed
    def next32():
        nonlocal state
        state ^= (state << 13) & MASK32
        state ^= state >> 17
        state ^= (state << 5) & MASK32
        state &= MASK32
        return state
    seen = set()
    results = []
    while len(results) < samples:
        mat = tuple(tuple(next32() % 3 for _ in range(7)) for _ in range(3))
        if mat in seen or rank3(mat) != 3:
            continue
        seen.add(mat)
        count = project_count(cap, mat)
        results.append({"matrix": "/".join("".join(map(str, row)) for row in mat),
                        "Q": concentration(count), "zero_fibers": count.count(0),
                        "minimum_fiber": min(count), "maximum_fiber": max(count)})
    q = sorted(r["Q"] for r in results)
    return {"samples": samples, "seed": seed, "Q_min": q[0],
            "Q_median_lower": q[(samples-1)//2], "Q_max": q[-1],
            "empty_fiber_min": min(r["zero_fibers"] for r in results),
            "empty_fiber_max": max(r["zero_fibers"] for r in results),
            "count_Q_at_least_2884": sum(r["Q"] >= 2884 for r in results),
            "min_Q_examples": [r for r in results if r["Q"] == q[0]][:3],
            "max_Q_examples": [r for r in results if r["Q"] == q[-1]][:3]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=Path, default=FIXTURE)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    cap = read_cap(args.cap)
    assert_cap(cap)
    result = {"experiment": "CAP-006A", "cap_size": len(cap),
              "cap_arithmetic_check": "PASS", "scope": "projection distribution only",
              "coordinate": coordinate_audit(cap),
              "deterministic_sample": random_audit(cap)}
    assert result["deterministic_sample"]["Q_min"] == 2096
    assert result["deterministic_sample"]["Q_median_lower"] == 2234
    assert result["deterministic_sample"]["Q_max"] == 3186
    assert result["deterministic_sample"]["count_Q_at_least_2884"] == 2
    text = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.out:
        args.out.write_text(text)
    print(text, end="")

if __name__ == "__main__":
    main()
