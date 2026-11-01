#!/usr/bin/env python3
"""E014: exact minimum-symbol local obstruction for a FIXED orthogonal pair.

An A-transversal T is one cell in every row/column/A-symbol. For a third
Latin C orthogonal to A and B, each C-symbol class is an A-transversal
and contains every B-symbol exactly once. Given S subset of B symbols,
a cell x is BLOCKED if no A-transversal through x uses each s in S at
most once. A blocked cell proves that the fixed pair A,B has no mate.

Enumerating all subsets of B symbols of size < k and all A-transversals
proves the minimum k for this particular local-obstruction criterion.
It does NOT prove any statement about arbitrary order-10 Latin pairs.
"""
import collections
import itertools
import json
import math
from pathlib import Path
from sample_mates import transversals_single
from verify import analyze

ROOT = Path(__file__).resolve().parent


def minimal_obstruction(a, b):
    n = len(a)
    assert all(p["orthogonal"] for p in analyze([a, b], n))
    t = transversals_single(a)
    full = (1 << (n*n)) - 1
    entries = []
    for p in t:
        counts = collections.Counter(b[i][p[i]] for i in range(n))
        collision = sum(1 << s for s, ct in counts.items() if ct > 1)
        cellmask = sum(1 << (n*i+p[i]) for i in range(n))
        entries.append((collision, cellmask))
    details = {}
    for k in range(n+1):
        blocked_subsets = 0
        first = None
        for subset in itertools.combinations(range(n), k):
            selected = sum(1 << s for s in subset)
            cover = 0
            compatible = 0
            for collision, cells in entries:
                if collision & selected == 0:
                    cover |= cells
                    compatible += 1
            missing = full & ~cover
            if missing:
                blocked_subsets += 1
                if first is None:
                    idx = (missing & -missing).bit_length()-1
                    first = {"B_symbols": list(subset),
                             "blocked_cell": [idx//n, idx%n],
                             "uncovered_cells": missing.bit_count(),
                             "compatible_A_transversals": compatible}
        details[str(k)] = {"tested": math.comb(n,k),
                           "blocking_subsets": blocked_subsets}
        if blocked_subsets:
            return {"order":n,"A_transversals":len(t),
                    "minimum_B_symbol_subset":k,
                    "smaller_subsets_all_nonblocking":True,
                    "first_certificate":first,
                    "subset_count_by_size":details}
    raise AssertionError("full B symbol set should block a cell for these pairs")


def independent_permutation_replay(a,b,certificate):
    """Independent n! permutation loop for the claimed blocked cell."""
    n=len(a)
    row,col=certificate["blocked_cell"]
    subset=set(certificate["B_symbols"])
    a_transversals=0
    eligible_through_cell=0
    for p in itertools.permutations(range(n)):
        if len({a[i][p[i]] for i in range(n)}) != n:
            continue
        a_transversals += 1
        if p[row] != col:
            continue
        counts=collections.Counter(b[i][p[i]] for i in range(n))
        if all(counts[s] <= 1 for s in subset):
            eligible_through_cell += 1
    assert eligible_through_cell == 0
    return {"permutations_checked":math.factorial(n),
            "A_transversals":a_transversals,
            "eligible_through_blocked_cell":eligible_through_cell}


def load_pairs():
    near=json.loads((ROOT/"near_triple.json").read_text())["squares"]
    parker=json.loads((ROOT/"parker_pair.json").read_text())["squares"]
    w=json.loads((ROOT/"E012_WITNESSES.json").read_text())
    cases={"Egan_AB":(near[0],near[1]),
           "Egan_AC":(near[0],near[2]),
           "Parker_AB":(parker[0],parker[1])}
    for name,entry in w["fixed_pairs"].items():
        cases[name]=(entry["A"],entry["B"])
    return cases


if __name__ == "__main__":
    output={}
    for name,(a,b) in load_pairs().items():
        result=minimal_obstruction(a,b)
        result["independent"]=independent_permutation_replay(
            a,b,result["first_certificate"])
        output[name]=result
        print(name, "min B symbols",result["minimum_B_symbol_subset"],
              "certificate",result["first_certificate"],flush=True)
    print(json.dumps(output,indent=2))
