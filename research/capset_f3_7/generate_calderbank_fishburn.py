#!/usr/bin/env python3
"""Reproduce the classical 236-point Calderbank–Fishburn cap in F_3^7.

Source: J. Bierbrauer, Y. Edel, 'Large caps in small spaces',
Table 1, Table 2, Theorem 5:
https://citeseerx.ist.psu.edu/document?doi=3b304b262b61d017935dd3a586d8ec892d4a9b88&repid=rep1&type=pdf
No reliance on random choices. Coordinates are written as 7 ternary digits.
This is a KNOWN construction, not a new record.
"""
import argparse
import itertools
from pathlib import Path
from verify_capset import verify

DESIGN_BLOCKS = (
    "123", "236", "124", "245", "135",
    "256", "146", "345", "156", "346",
)

def expand_support(support):
    """All vectors with coordinates 1 or 2 exactly on the 3-element support."""
    for signs in itertools.product((1, 2), repeat=3):
        out = [0] * 6
        for idx, sign in zip(support, signs):
            out[idx] = sign
        yield tuple(out)

def construction():
    D = {tuple(int(c) - 1 for c in block) for block in DESIGN_BLOCKS}
    D = {tuple(sorted(x)) for x in D}
    all_triples = set(itertools.combinations(range(6), 3))
    Dbar = all_triples - D
    assert len(D) == len(Dbar) == 10
    R = [v for v in itertools.product((1, 2), repeat=6)
         if sum(c == 2 for c in v) % 2 == 0]
    DD = [v for support in sorted(D) for v in expand_support(support)]
    Dc = [v for support in sorted(Dbar) for v in expand_support(support)]
    U = [tuple(s if i == pos else 0 for i in range(6))
         for pos in range(6) for s in (1, 2)]
    assert (len(R), len(DD), len(Dc), len(U)) == (32, 80, 80, 12)
    points = ([(0,) + v for v in R + DD] +
              [(1,) + v for v in R + Dc] +
              [(2,) + v for v in U])
    assert verify(points) == 236
    return points

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="research/capset_f3_7/candidates/calderbank_fishburn_236.txt")
    args = parser.parse_args()
    points = construction()
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("n: 7\n" + "\n".join("".join(map(str, p)) for p in points) + "\n",
                      encoding="utf-8")
    print(f"VERIFIED known Calderbank–Fishburn cap: {len(points)} points, file={target}")
