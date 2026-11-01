#!/usr/bin/env python3
"""Exact finite cap set verifier: no heuristic or floating-point arithmetic."""
import argparse
from pathlib import Path

def read_points(file_path, dimension=7):
    rows = Path(file_path).read_text(encoding="utf-8").splitlines()
    points = []
    for line_number, raw in enumerate(rows, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("n:"):
            if points or int(line.split(":", 1)[1]) != dimension:
                raise ValueError("Incorrect or misplaced dimension header")
            continue
        if len(line) != dimension or any(v not in "012" for v in line):
            raise ValueError(f"Invalid coordinate line {line_number}")
        points.append(tuple(int(d) for d in line))
    return points

def verify(points, dimension=7):
    points = [tuple(p) for p in points]
    if any(len(p) != dimension or any(x not in (0, 1, 2) for x in p) for p in points):
        raise ValueError("Malformed vector")
    members = set(points)
    if len(members) != len(points):
        raise ValueError("Duplicate vector")
    for i, p in enumerate(points):
        for q in points[i + 1:]:
            third = tuple((-a-b) % 3 for a, b in zip(p, q))
            if third in members:
                raise ValueError(f"Forbidden triple: {p}, {q}, {third}")
    return len(points)

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("path")
    cli.add_argument("--dimension", type=int, default=7)
    args = cli.parse_args()
    size = verify(read_points(args.path, args.dimension), args.dimension)
    print(f"VERIFIED cap dimension={args.dimension} size={size}")
    if size >= 237 and args.dimension == 7:
        print("Possible new lower bound: independently audit and compare against latest literature.")
