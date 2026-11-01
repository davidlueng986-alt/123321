#!/usr/bin/env python3
"""Exact dual-certificate replay for fixed-pair Latin-square near-orthogonality.

No SciPy, SAT solver, probabilistic assumptions, or floating point required.

Mathematical statement: Fix Latin squares A,D which are orthogonal. Let
X range over ALL Latin squares orthogonal to A. For each X-symbol v, its
ten positions form an A-transversal T_v. For a chosen cell subset R,
verify for EVERY A-transversal T that:
    |{D(i,j) : (i,j) in T}| <= |T minus R|.
The X-symbol classes partition all n^2 cells, so summing proves
    |{(X(i,j),D(i,j)) : all cells}| <= n^2 - |R|.
A claimed tight upper bound also needs an explicit attaining X.

A certificate for a fixed A,D does NOT resolve unrestricted MOLS(10).
"""
import argparse
import collections
import itertools
import json
from pathlib import Path


def is_latin(s):
    if not isinstance(s, list) or not s:
        return False
    n = len(s)
    target = set(range(n))
    return all(
        isinstance(row, list) and len(row) == n
        and all(type(x) is int for x in row)
        and set(row) == target
        for row in s
    ) and all({s[i][j] for i in range(n)} == target for j in range(n))


def pair_count(a, b):
    n = len(a)
    return len({(a[i][j], b[i][j]) for i in range(n) for j in range(n)})


def transversals_dfs(a):
    n = len(a)
    choices = []
    def rec(row, taken_cols, taken_symbols):
        if row == n:
            yield tuple(choices)
            return
        for col in range(n):
            cb = 1 << col
            sb = 1 << a[row][col]
            if taken_cols & cb or taken_symbols & sb:
                continue
            choices.append(col)
            yield from rec(row + 1, taken_cols | cb, taken_symbols | sb)
            choices.pop()
    yield from rec(0, 0, 0)


def validate(a, d, certificate, attaining=None, independent=False):
    assert is_latin(a) and is_latin(d), "input matrices must be Latin"
    n = len(a)
    assert len(d) == n and pair_count(a, d) == n * n, "A,D must be orthogonal"
    raw_cells = certificate["removed_cells_zero_based"]
    removed = [tuple(c) for c in raw_cells]
    r = set(removed)
    assert len(r) == len(raw_cells), "duplicate removed cells"
    assert all(len(c) == 2 and all(type(z) is int and 0 <= z < n for z in c)
               for c in r), "invalid removed cell"

    def slack(p):
        distinct = len({d[i][p[i]] for i in range(n)})
        outside = sum((i, p[i]) not in r for i in range(n))
        return outside - distinct

    count = 0
    counter = collections.Counter()
    reference = [] if independent else None
    for p in transversals_dfs(a):
        count += 1
        if reference is not None:
            reference.append(p)
        delta = slack(p)
        if delta < 0:
            raise AssertionError("dual certificate fails on transversal " + str(p))
        counter[delta] += 1

    brute_checked = None
    if independent:
        brute_checked = 0
        brute = []
        for p in itertools.permutations(range(n)):
            brute_checked += 1
            if len({a[i][p[i]] for i in range(n)}) == n:
                brute.append(p)
        assert brute == reference, "independent full permutation replay disagrees"
    upper = n * n - len(r)
    actual = None
    if attaining is not None:
        assert is_latin(attaining) and pair_count(a, attaining) == n*n
        actual = pair_count(d, attaining)
        assert actual <= upper
    info = {
        "certificate_valid": True, "order": n, "transversal_count": count,
        "permutations_checked_independently": brute_checked,
        "removed_cells": [list(c) for c in sorted(r)],
        "minimum_slack": min(counter),
        "tight_transversals": counter[0],
        "slack_histogram": {str(k): v for k,v in sorted(counter.items())},
        "upper_bound": upper,
        "attained": actual is not None and actual == upper,
        "attaining_score": actual,
        "scope": "fixed A,D only; NOT a general 3-MOLS(10) solution"
    }
    assert count == certificate["asserted_A_transversal_count"]
    assert upper == certificate["asserted_upper_bound"]
    if "asserted_constraint_min_slack" in certificate:
        assert min(counter) == certificate["asserted_constraint_min_slack"]
    if "asserted_min_slack" in certificate:
        assert min(counter) == certificate["asserted_min_slack"]
    if "asserted_tight_count" in certificate:
        assert counter[0] == certificate["asserted_tight_count"]
    if "asserted_slack_histogram" in certificate:
        assert info["slack_histogram"] == {
            str(k): v for k,v in certificate["asserted_slack_histogram"].items()
        }
    if "attaining_overlay" in certificate and certificate["attaining_overlay"] is not None:
        assert actual == certificate["attaining_overlay"]
    return info


def replay(certificate_file, independent=False):
    path = Path(certificate_file)
    cert = json.loads(path.read_text(encoding="utf8"))
    squares = json.loads((path.parent / Path(cert["source"]).name).read_text(encoding="utf8"))["squares"]
    i, j = cert["fixed_indices"]
    idx = cert.get("attaining_index")
    return validate(squares[i], squares[j], cert,
                    None if idx is None else squares[idx],
                    independent=independent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate_file", type=Path)
    parser.add_argument("--independent", action="store_true",
                        help="also enumerate all n! permutations as independent replay")
    args = parser.parse_args()
    print(json.dumps(replay(args.certificate_file, args.independent), indent=2))
