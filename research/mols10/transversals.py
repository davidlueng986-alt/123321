#!/usr/bin/env python3
"""Exhaustive common-transversal/packing test for a FIXED orthogonal Latin pair.

A third orthogonal mate exists iff the n*n cells partition into n disjoint
common transversals. For n<=10 enumerate ALL n! row-column permutations.
No result for one fixed pair settles the unrestricted 3-MOLS(10) problem.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from verify import analyze


def transversals_by_permutations(a, b):
    n = len(a)
    if not 2 <= n <= 10:
        raise ValueError("exact permutation enumeration limited to orders 2..10")
    if not analyze([a, b], n)[0]["orthogonal"]:
        raise ValueError("invalid orthogonal Latin pair")
    return [p for p in itertools.permutations(range(n))
            if len({a[i][p[i]] for i in range(n)}) == n
            and len({b[i][p[i]] for i in range(n)}) == n]


def transversals_by_dfs(a, b):
    """Independent complete enumerator, using disjoint bit masks."""
    n = len(a)
    if not 2 <= n <= 10 or not analyze([a, b], n)[0]["orthogonal"]:
        raise ValueError("invalid order or pair")
    out, chosen = [], [-1] * n
    def dfs(row, cols, aa, bb):
        if row == n:
            out.append(tuple(chosen))
            return
        for col in range(n):
            c, av, bv = 1 << col, 1 << a[row][col], 1 << b[row][col]
            if cols & c or aa & av or bb & bv:
                continue
            chosen[row] = col
            dfs(row + 1, cols | c, aa | av, bb | bv)
            chosen[row] = -1
    dfs(0, 0, 0, 0)
    return out


def exact_packing(transversals, n, candidate_limit=20):
    """Exhaustive subset branch-and-bound. Explicitly decline huge cases."""
    if len(transversals) > candidate_limit:
        return {"status": "UNKNOWN_TOO_MANY_CANDIDATES", "candidate_limit": candidate_limit}
    masks = [sum(1 << (n*r+c) for r, c in enumerate(p)) for p in transversals]
    best, nodes = [], 0
    def dfs(start, occupied, chosen):
        nonlocal best, nodes
        nodes += 1
        if len(chosen) > len(best):
            best = chosen[:]
        if len(chosen) + len(masks) - start <= len(best):
            return
        for i in range(start, len(masks)):
            if occupied & masks[i] == 0:
                chosen.append(i)
                dfs(i + 1, occupied | masks[i], chosen)
                chosen.pop()
    dfs(0, 0, [])
    return {"status": "EXACT", "max_disjoint": len(best),
            "packing_indices": best, "subset_search_nodes": nodes}


def analyze_fixed_pair(a, b):
    n = len(a)
    permutations = transversals_by_permutations(a, b)
    independent = transversals_by_dfs(a, b)
    if permutations != independent:
        raise AssertionError("independent enumeration algorithms disagree")
    support = [[0]*n for _ in range(n)]
    for p in permutations:
        for i, j in enumerate(p):
            support[i][j] += 1
    unsupported = [[i, j] for i in range(n) for j in range(n)
                   if support[i][j] == 0]
    packing = exact_packing(permutations, n)
    third = None
    if packing["status"] == "EXACT" and packing["max_disjoint"] == n:
        third = [[-1]*n for _ in range(n)]
        for symbol, idx in enumerate(packing["packing_indices"]):
            for row, col in enumerate(permutations[idx]):
                third[row][col] = symbol
        if not all(x["orthogonal"] for x in analyze([a, b, third], n)):
            raise AssertionError("candidate failed independent verifier")
    ruled_out = len(permutations) < n or bool(unsupported) or (
        packing["status"] == "EXACT" and packing["max_disjoint"] < n)
    return {
        "order": n,
        "pair_sha256": hashlib.sha256(json.dumps([a,b], separators=(",",":")).encode()).hexdigest(),
        "enumeration": "EXACT: n! permutations, cross-checked by independent DFS",
        "common_transversal_count": len(permutations),
        "transversal_permutations": [list(p) for p in permutations],
        "unsupported_cells_zero_based": unsupported,
        "packing": packing,
        "extension_status": ("SAT_VERIFIED" if third is not None else
                             "UNSAT_FIXED_PAIR_CERTIFIED" if ruled_out else "UNKNOWN"),
        "third_square_witness": third,
        "scope": "FIXED PAIR ONLY; unrestricted 3-MOLS(10) remains open",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("json_file", type=Path)
    ap.add_argument("--pair", type=int, nargs=2, default=[0,1])
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    squares = json.loads(args.json_file.read_text(encoding="utf-8"))["squares"]
    result = analyze_fixed_pair(squares[args.pair[0]], squares[args.pair[1]])
    result["pair_indices"] = args.pair
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
