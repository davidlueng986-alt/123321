#!/usr/bin/env python3
"""E013 necessary but empirically vacuous one-transversal compatibility screen.

If T is a B-symbol class in a hypothetical triple with fixed A, each
C-symbol class U must intersect T in exactly one cell. Hence the union of
all A-transversals U with |U intersect T|=1 must cover the whole grid.
If not, T is forbidden. This condition alone was non-discriminating for
all 49 tested A (original Egan A plus 48 exact two-symbol trades).
"""
import collections
import json
from pathlib import Path
from first_square_trades import first_square_trades
from sample_mates import transversals_single

ROOT=Path(__file__).resolve().parent

def screen(a):
    n=len(a)
    trans=transversals_single(a)
    masks=[sum(1 << (n*i+j) for i,j in enumerate(t)) for t in trans]
    full=(1 << (n*n))-1
    excluded=0
    survivor_cover=0
    degrees=[]
    for t in masks:
        union=0
        degree=0
        for u in masks:
            if (t&u).bit_count()==1:
                union|=u
                degree+=1
        degrees.append(degree)
        if union==full:survivor_cover|=t
        else:excluded+=1
    return {"A_transversals":len(trans),"excluded":excluded,
            "min_degree":min(degrees),"max_degree":max(degrees),
            "uncovered_cells_after_filter":(full&~survivor_cover).bit_count()}

if __name__=="__main__":
    original=json.loads((ROOT/"near_triple.json").read_text())["squares"][0]
    variants=[original]+[x["square"] for x in first_square_trades(original)]
    results=[screen(a) for a in variants]
    assert len(results)==49
    print(json.dumps({"A_variants":49,
        "total_excluded":sum(x["excluded"] for x in results),
        "min_degree":min(x["min_degree"] for x in results),
        "max_degree":max(x["max_degree"] for x in results),
        "results":results},indent=2))
