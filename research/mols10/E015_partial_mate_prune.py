#!/usr/bin/env python3
"""E015: sound partial-mate pruning for fixed first Latin square A.

For every chosen B-symbol class T (an A-transversal), any hypothetical
C-symbol class U must meet T exactly once. Maintain the bitset of
A-transversals U satisfying ALL chosen classes. If some cell belongs to
none of these U, no completion of this B prefix can form 3-MOLS.

Necessary only; a surviving B partition does NOT prove a triple.
Budget exhaustion is UNKNOWN. No unproved symmetry normalization.
"""
import argparse
import json
import random
import time
from pathlib import Path
from first_square_trades import first_square_trades
from sample_mates import transversals_single, transversals_pair
from exact_cover import exact_cover, build_third
from verify import analyze

ROOT=Path(__file__).resolve().parent

def setup(a):
    n=len(a);trans=transversals_single(a)
    masks=[sum(1<<(n*i+j) for i,j in enumerate(p)) for p in trans]
    by_cell=[0]*(n*n)
    for k,p in enumerate(trans):
        for i,j in enumerate(p):by_cell[n*i+j]|=1<<k
    compatibility=[]
    for m in masks:
        bits=0
        for k,u in enumerate(masks):
            if (m&u).bit_count()==1:bits|=1<<k
        compatibility.append(bits)
    return trans,masks,by_cell,compatibility

def check_partial(by_cell,compatibility,selected):
    possible=(1<<len(compatibility))-1
    for k in selected:possible&=compatibility[k]
    blocked=[c for c,refs in enumerate(by_cell) if not (refs&possible)]
    return not blocked,blocked,possible.bit_count()

def bounded_search(a,seed=0,seconds=4.0,max_nodes=100000):
    n=len(a);full=(1<<(n*n))-1
    trans,masks,by_cell,comp=setup(a)
    rng=random.Random(seed)
    order=list(range(len(trans)));rng.shuffle(order)
    rank={k:i for i,k in enumerate(order)}
    nodes=0;prunes=0;selected=[];start=time.monotonic();witness=None
    class Budget(Exception):pass
    def dfs(used,possible):
        nonlocal nodes,prunes,witness
        if nodes>=max_nodes or time.monotonic()-start>seconds:raise Budget
        nodes+=1
        if any((possible&refs)==0 for refs in by_cell):
            prunes+=1
            return False
        if used==full:
            b=[[-1]*n for _ in range(n)]
            for symbol,k in enumerate(selected):
                for i,j in enumerate(trans[k]):b[i][j]=symbol
            assert all(q["orthogonal"] for q in analyze([a,b],n))
            joint,support=transversals_pair(a,b)
            assert len(joint)==possible.bit_count() and all(support)
            witness={"A":a,"B":b,"common_transversals":len(joint)}
            r=exact_cover(joint,n,max_nodes=10000,max_seconds=1.0)
            witness["third_search_status"]=r["status"]
            if r["status"]=="SAT_EXACT":
                witness["C"]=build_third(a,b,joint,r)
            return True
        remainder=full&~used;best=None
        while remainder:
            bit=remainder&-remainder;c=bit.bit_length()-1
            avail=[k for k in range(len(trans))
                   if (by_cell[c]>>k)&1 and not (masks[k]&used)]
            if not avail:return False
            if best is None or len(avail)<len(best):best=avail
            if len(best)==1:break
            remainder-=bit
        best.sort(key=lambda k:rank[k])
        for k in best:
            selected.append(k)
            if dfs(used|masks[k],possible&comp[k]):return True
            selected.pop()
        return False
    try:
        found=dfs(0,(1<<len(trans))-1)
        status="SAT_COVERAGE_SCREEN" if found else "UNSAT_EXHAUSTIVE_FIXED_A"
    except Budget:
        status="UNKNOWN_BUDGET"
    return {"status":status,"nodes":nodes,
            "pruned_by_partial_support":prunes,
            "A_transversals":len(trans),
            "elapsed_seconds":round(time.monotonic()-start,3),
            "witness":witness}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--seconds",type=float,default=4.0)
    parser.add_argument("--indices",type=int,nargs="+",default=[12,20,30])
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args()
    original=json.loads((ROOT/"near_triple.json").read_text())["squares"][0]
    variants=first_square_trades(original)
    results=[]
    for index in args.indices:
        result=bounded_search(variants[index]["square"],seed=args.seed,
                              seconds=args.seconds)
        results.append({"trade_index":index,**result})
        print(index,result["status"],result["nodes"],
              result["pruned_by_partial_support"],flush=True)
    (ROOT/"E015_bounded_results.json").write_text(json.dumps(results,indent=2)+"\n")
