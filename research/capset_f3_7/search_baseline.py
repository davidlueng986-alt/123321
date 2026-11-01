#!/usr/bin/env python3
"""Minimal CPU-only reproducible baseline; not a record-seeking solver."""
import argparse
import itertools
import random
from pathlib import Path
from verify_capset import verify

def greedy(order):
    selected = []
    forbidden = set()
    for p in order:
        if p in forbidden:
            continue
        for q in selected:
            forbidden.add(tuple((-x-y)%3 for x,y in zip(p,q)))
        selected.append(p)
    verify(selected)
    return selected

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=7)
    parser.add_argument("--rounds",type=int,default=4)
    parser.add_argument("--out",default="/tmp/capset_f3_7.txt")
    args = parser.parse_args()
    if args.rounds <= 0:
        raise ValueError("rounds must be positive")
    rng = random.Random(args.seed)
    pool = list(itertools.product(range(3),repeat=7))
    best = []
    for i in range(args.rounds):
        order = pool.copy()
        rng.shuffle(order)
        candidate = greedy(order)
        if len(candidate) > len(best):
            best = candidate
            print(f"round={i+1} seed={args.seed} best={len(best)}",flush=True)
    verify(best)
    Path(args.out).write_text("n: 7\n" + "\n".join("".join(map(str,p)) for p in best) + "\n", encoding="utf-8")
    print(f"wrote {len(best)}-point cap to {args.out}")

if __name__ == "__main__":
    main()
