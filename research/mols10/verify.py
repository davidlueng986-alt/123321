#!/usr/bin/env python3
"""Independent exact checker for mutually orthogonal Latin squares."""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

def analyze(squares, n):
    if not isinstance(squares, list) or not squares:
        raise ValueError("squares must be a nonempty array")
    symbols = set(range(n))
    for sidx, square in enumerate(squares):
        if not isinstance(square, list) or len(square) != n:
            raise ValueError(f"square {sidx}: expected {n} rows")
        for i, row in enumerate(square):
            if not isinstance(row, list) or len(row) != n:
                raise ValueError(f"square {sidx}, row {i}: expected {n} entries")
            if any(type(v) is not int for v in row) or set(row) != symbols:
                raise ValueError(f"square {sidx}, row {i} is not a permutation of 0..{n-1}")
        for j in range(n):
            if {square[i][j] for i in range(n)} != symbols:
                raise ValueError(f"square {sidx}, column {j} is not a permutation of 0..{n-1}")
    overlays = []
    for a, b in itertools.combinations(range(len(squares)), 2):
        mult = Counter((squares[a][i][j], squares[b][i][j])
                       for i in range(n) for j in range(n))
        missing = sorted(p for p in itertools.product(range(n), repeat=2) if p not in mult)
        repeated = sorted((p, count) for p, count in mult.items() if count > 1)
        overlays.append({"squares": [a,b], "unique": len(mult),
                         "orthogonal": len(mult) == n*n, "missing": missing,
                         "repeated": repeated})
    return overlays

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("json_file", type=Path)
    ap.add_argument("--target", type=int, default=10)
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--diagnostic", action="store_true")
    args = ap.parse_args()
    if args.target < 2 or args.count < 2:
        ap.error("target and count must be >= 2")
    squares = json.loads(args.json_file.read_text(encoding="utf-8"))["squares"]
    if len(squares) != args.count:
        raise ValueError(f"Expected {args.count} squares, received {len(squares)}")
    overlays = analyze(squares, args.target)
    solved = all(q["orthogonal"] for q in overlays)
    print(json.dumps({"order": args.target, "all_latin": True,
                      "overlays": overlays, "valid_mols_witness": solved}, indent=2))
    if not solved and not args.diagnostic:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
