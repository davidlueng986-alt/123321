#!/usr/bin/env python3
"""E016: exhaustive fixed-first-square exclusion using exact-once C-support.

Scope is one specified Latin A, not all order-10 Latin squares.
A B-symbol class is an A-transversal. Any C-symbol class must intersect
every selected B-symbol class exactly once. If the compatible C-classes
fail to cover some cell, this B-prefix cannot occur in a triple.
"""
import argparse, json, random, time
from pathlib import Path
from E015_partial_mate_prune import setup
from first_square_trades import first_square_trades
from verify import analyze

ROOT=Path(__file__).resolve().parent

def run(a, seed=0, max_nodes=250000, max_seconds=7):
    n=len(a)
    if not all(set(row)==set(range(n)) for row in a) or not all(
            {a[i][j] for i in range(n)}==set(range(n)) for j in range(n)):
        raise ValueError('not Latin')
    trans,masks,by_cell,compat=setup(a)
    full=(1<<len(trans))-1
    all_cells=(1<<(n*n))-1
    disjoint=[]
    for mask in masks:
        bad=0
        while mask:
            bit=mask&-mask
            bad |= by_cell[bit.bit_length()-1]
            mask-=bit
        disjoint.append(full&~bad)
    order=list(range(len(trans)))
    random.Random(seed).shuffle(order)
    rank={k:i for i,k in enumerate(order)}
    nodes=prunes=0
    chosen=[]
    witness=None
    start=time.monotonic()
    class Budget(Exception): pass

    def dfs(used, compatible, eligible):
        nonlocal nodes,prunes,witness
        if nodes>=max_nodes or time.monotonic()-start>max_seconds:
            raise Budget
        nodes+=1
        if any(not (compatible&refs) for refs in by_cell):
            prunes+=1
            return False
        if used==all_cells:
            b=[[-1]*n for _ in range(n)]
            for s,k in enumerate(chosen):
                for i,j in enumerate(trans[k]):
                    b[i][j]=s
            assert all(x['orthogonal'] for x in analyze([a,b],n))
            witness={'B':b,'compatible_C_transversals':compatible.bit_count()}
            return True
        remainder=all_cells&~used
        best=None
        while remainder:
            bit=remainder&-remainder
            c=bit.bit_length()-1
            avail=by_cell[c]&eligible
            if not avail:return False
            if best is None or avail.bit_count()<best.bit_count():
                best=avail
            if best.bit_count()==1:break
            remainder-=bit
        options=[]
        while best:
            bit=best&-best
            options.append(bit.bit_length()-1)
            best-=bit
        options.sort(key=lambda k:rank[k])
        for k in options:
            chosen.append(k)
            if dfs(used|masks[k], compatible&compat[k], eligible&disjoint[k]):
                return True
            chosen.pop()
        return False

    try:
        found=dfs(0,full,full)
        status='SAT_SUPPORT_ONLY' if found else 'UNSAT_FIXED_A_EXHAUSTIVE'
    except Budget:
        status='UNKNOWN_BUDGET'
    return {'status':status,'nodes':nodes,'pruned_prefixes':prunes,
            'A_transversals':len(trans),
            'dfs_seconds':round(time.monotonic()-start,5),
            'witness':witness}

def gf4_positive_control():
    a=[[i^j for j in range(4)] for i in range(4)]
    r=run(a,max_nodes=10000,max_seconds=5)
    assert r['status']=='SAT_SUPPORT_ONLY'
    assert r['witness']['compatible_C_transversals']>=4
    return r

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--indices',type=int,nargs='*',default=list(range(48)))
    ap.add_argument('--original',action='store_true')
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--nodes',type=int,default=250000)
    ap.add_argument('--seconds',type=float,default=7)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    gf4_positive_control()
    a=json.loads((ROOT/'near_triple.json').read_text())['squares'][0]
    variants=first_square_trades(a)
    results=[]
    if args.original:
        r=run(a,args.seed,args.nodes,args.seconds)
        results.append({'trade_index':'original',**r})
        print('original',r['status'],r['nodes'],r['pruned_prefixes'],flush=True)
    for i in args.indices:
        if not 0<=i<len(variants):raise ValueError('bad trade index')
        r=run(variants[i]['square'],args.seed,args.nodes,args.seconds)
        results.append({'trade_index':i,**r})
        print(i,r['status'],r['nodes'],r['pruned_prefixes'],flush=True)
    if args.output:
        args.output.write_text(json.dumps(results,indent=2)+'\n')
