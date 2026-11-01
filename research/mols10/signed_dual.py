#!/usr/bin/env python3
"""Replay a SIGNED rational (integer-scaled) transversal-dual certificate.

For fixed orthogonal Latin pair (A,D), choose integer cell weights z_ij
and denominator q > 0. If for every A-transversal T:
    sum_(i,j) in T z_ij <= q*(n - number distinct D-symbols on T)
then any Latin B' orthogonal to A satisfies:
    overlay_unique(D,B') <= floor(n*n - sum_all z_ij / q).
Negative cell weights are valid because every B' symbol class partitions the
whole n*n grid, and every such class is an A-transversal.

All calculations use exact integer arithmetic. No numerical solver dependency.
"""
import argparse
import collections
import json
from pathlib import Path
from dual_certificates import is_latin, pair_count, transversals_dfs


def validate_signed(a, d, certificate):
    if not is_latin(a) or not is_latin(d) or len(a) != len(d):
        raise ValueError("fixed squares must be Latin")
    n = len(a)
    if pair_count(a,d) != n*n:
        raise ValueError("fixed pair is not orthogonal")
    q = certificate["denominator"]
    matrix = certificate["weight_numerators"]
    if type(q) is not int or q <= 0 or len(matrix) != n or any(
        not isinstance(row,list) or len(row) != n
        or any(type(z) is not int for z in row)
        for row in matrix
    ):
        raise ValueError("invalid signed rational certificate")

    weight_sum = sum(map(sum,matrix))
    if weight_sum != certificate["asserted_weight_sum"]:
        raise AssertionError("weight sum mismatch")

    tight = 0
    n_trans = 0
    min_slack = None
    histogram = collections.Counter()
    for p in transversals_dfs(a):
        n_trans += 1
        distinct = len({d[i][p[i]] for i in range(n)})
        weight = sum(matrix[i][p[i]] for i in range(n))
        slack = q*(n-distinct)-weight
        if slack < 0:
            raise AssertionError("violating A-transversal: " + str(p))
        histogram[slack] += 1
        min_slack = slack if min_slack is None else min(min_slack, slack)
        if slack == 0:
            tight += 1
    upper = (q*n*n - weight_sum)//q
    assert n_trans == certificate["asserted_A_transversal_count"]
    assert min_slack == certificate["asserted_min_constraint_slack"]
    assert tight == certificate["asserted_tight_transversal_count"]
    assert upper == certificate["asserted_upper_bound"]
    if "attaining_index" in certificate:
        # The replay wrapper separately validates the attaining square's
        # Latin property, A-orthogonality, and actual D-overlay.
        assert certificate["attaining_overlay"] == upper

    return {"verified":True,"order":n,"denominator":q,
            "weight_sum_numerators":weight_sum,
            "A_transversals_checked":n_trans,
            "minimum_constraint_slack":min_slack,
            "tight_transversals":tight,
            "global_integer_upper_bound_for_fixed_pair":upper,
            "scope":"conditional fixed pair only; open MOLS10 unchanged"}


def replay(path):
    path = Path(path)
    cert = json.loads(path.read_text())
    squares = json.loads((path.parent / Path(cert["source"]).name).read_text())["squares"]
    a,d = [squares[k] for k in cert["fixed_indices"]]
    output = validate_signed(a,d,cert)
    if "attaining_index" in cert:
        candidate = squares[cert["attaining_index"]]
        n = len(a)
        if not is_latin(candidate) or pair_count(a,candidate) != n*n:
            raise AssertionError("claimed attainer is not Latin and orthogonal to A")
        actual = pair_count(d,candidate)
        if actual != output["global_integer_upper_bound_for_fixed_pair"]:
            raise AssertionError("claimed attainer does not reach the dual bound")
        output["attaining_score"] = actual
        output["optimality_proven"] = True
    return output


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate_file")
    args=parser.parse_args()
    print(json.dumps(replay(args.certificate_file),indent=2))
