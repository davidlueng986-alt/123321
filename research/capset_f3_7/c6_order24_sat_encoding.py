#!/usr/bin/env python3
"""CAP-004F: exact CNF reduction for all order-24-invariant F3^7 caps.

This is an exact decision encoding, NOT an UNSAT proof and NOT a global
upper bound. 135 primary orbit variables (3 slices x 45 orbits).
Deterministic, stdlib only; no SAT solver or paid compute required.
"""
import argparse
import contextlib
import hashlib
import io
import itertools
import json

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
weights = [len(orbit) for orbit in orbits]
n = len(orbits)
primary_count = 3 * n

# A line in F3^7 either lies entirely within one 6D slice or has
# exactly one point in each of the three slices. These are ALL cases.
within = set()
cross = set()
for a in space:
    i = orbit_of[a]
    for b in space:
        j = orbit_of[b]
        c = tuple((-u-v) % 3 for u, v in zip(a, b))
        k = orbit_of[c]
        cross.add((i, j, k))
        if a != b:
            within.add(tuple(sorted({i, j, k})))
assert len(within) == 3556
assert len(cross) > 4089

class CNF:
    def __init__(self):
        self.nvar = primary_count
        self.clauses = []
        self.gates = []

    def new(self, op, *args):
        self.nvar += 1
        self.gates.append((self.nvar, op, args))
        return self.nvar

    def add(self, *lits):
        assert all(type(lit) is int and lit != 0 for lit in lits)
        self.clauses.append(tuple(lits))

    def recurrence(self, a, x, b):
        # y = a OR (x AND b), where a,b are constants or positive vars.
        if a is True or b is False:
            return a
        if a is False:
            if b is True:
                return x
            y = self.new("and", x, b)
            self.add(-y, x)
            self.add(-y, b)
            self.add(y, -x, -b)
            return y
        if b is True:
            y = self.new("or", a, x)
            self.add(-a, y)
            self.add(-x, y)
            self.add(-y, a, x)
            return y
        y = self.new("mix", a, x, b)
        self.add(-a, y)
        self.add(-x, -b, y)
        self.add(-y, a, x)
        self.add(-y, a, b)
        return y

    def eval_assignment(self, primaries):
        vals = [False] * (self.nvar + 1)
        for i, val in enumerate(primaries, 1):
            vals[i] = bool(val)
        for y, op, args in self.gates:
            u = [vals[z] if type(z) is int else z for z in args]
            if op == "and":
                vals[y] = u[0] and u[1]
            elif op == "or":
                vals[y] = u[0] or u[1]
            else:
                vals[y] = u[0] or (u[1] and u[2])
        return vals

def build(target):
    cnf = CNF()
    for s in range(3):
        for ids in sorted(within):
            cnf.add(*(-(1+s*n+i) for i in ids))
    for i, j, k in sorted(cross):
        cnf.add(-(1+i), -(1+n+j), -(1+2*n+k))
    structural_count = len(cnf.clauses)
    # Weighted threshold >= target via exact Tseitin dynamic programming.
    # prev[t] means selected weight among processed orbit variables >= t.
    prev = [True] + [False] * target
    cumulative = 0
    for s in range(3):
        for i, w in enumerate(weights):
            x = 1+s*n+i
            cumulative += w
            cur = [True]
            for t in range(1, target+1):
                if t > cumulative:
                    cur.append(False)
                else:
                    b = True if t <= w else prev[t-w]
                    cur.append(cnf.recurrence(prev[t], x, b))
            prev = cur
    assert type(prev[target]) is int
    cnf.add(prev[target])  # The only objective clause.
    return cnf, structural_count

# Independent 236 witness from the previously certified order-120 masks,
# refined to the 24-orbits without importing the order-120 optimizer.
masks120 = (462848, 344128, 1048576)
primary = []
candidate = []
for s in range(3):
    for orbit in orbits:
        ids = {orbit120_of[p] for p in orbit}
        assert len(ids) == 1
        selected = bool(masks120[s] & (1 << next(iter(ids))))
        primary.append(selected)
        if selected:
            candidate.extend((s,)+p for p in orbit)
assert sum(v*w for v, w in zip(primary, weights*3)) == 236
assert verify(candidate, 7) == 236  # Independent coordinate arithmetic.

def test_cnf(cnf, structural_count, target):
    vals = cnf.eval_assignment(primary)
    failures = [idx for idx, clause in enumerate(cnf.clauses)
                if not any(vals[abs(lit)] == (lit > 0) for lit in clause)]
    assert not any(i < structural_count for i in failures)
    if target == 236:
        assert failures == []
    else:
        assert target == 237 and failures == [len(cnf.clauses)-1]
    return len(failures)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, choices=(236, 237), default=237)
    parser.add_argument("--out", help="Optional DIMACS CNF output path")
    args = parser.parse_args()
    cnf, structural_count = build(args.target)
    witness_failures = test_cnf(cnf, structural_count, args.target)
    digest = None
    if args.out:
        h = hashlib.sha256()
        with open(args.out, "w", encoding="ascii", newline="\n") as f:
            def emit(line):
                data = line.encode("ascii")
                f.write(line)
                h.update(data)
            emit("p cnf %d %d\n" % (cnf.nvar, len(cnf.clauses)))
            for clause in cnf.clauses:
                emit(" ".join(map(str, clause)) + " 0\n")
        digest = h.hexdigest()
    print(json.dumps({
        "status": "EXACT_REDUCTION_NOT_SAT_SOLVED",
        "target": args.target,
        "subgroup_order": 24,
        "orbit_count": n,
        "primary_variables": primary_count,
        "auxiliary_variables": cnf.nvar-primary_count,
        "variables": cnf.nvar,
        "within_orbit_forbidden_sets": len(within),
        "cross_orbit_triples": len(cross),
        "structural_clauses": structural_count,
        "total_clauses": len(cnf.clauses),
        "independent_236_witness_verified": True,
        "witness_236_unsatisfied_clauses": witness_failures,
        "cnf_sha256": digest,
        "exact_24_invariant_237_decision_status": "UNKNOWN",
        "global_r3_7_status": "OPEN"
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
