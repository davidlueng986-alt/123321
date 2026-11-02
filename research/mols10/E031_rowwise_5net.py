#!/usr/bin/env python3
"""E031 exact row-wise 3-MOLS(n) search, verified independently.
Mathematical symmetry: each square's first row may be independently renamed 0..n-1;
then globally permute rows 1..n-1 so square A's first column is 0..n-1.
Additional safe symmetry: exchange B,C to force B[1][0]<C[1][0].
There are NO unsupported reductions. UNKNOWN_BUDGET is NOT UNSAT.
"""
import json, argparse, time, random

def check(squares):
    n=len(squares[0]); target=set(range(n))
    assert len(squares)==3
    assert all(len(A)==n and all(len(row)==n and set(row)==target for row in A)
        and all({A[r][c] for r in range(n)}==target for c in range(n))
        for A in squares)
    overlays=[]
    for a,b in ((0,1),(0,2),(1,2)):
        overlays.append(len({(squares[a][r][c],squares[b][r][c])
                             for r in range(n) for c in range(n)}))
    assert overlays==[n*n]*3
    return overlays

def solve(n, node_budget=200000, wall_seconds=8., symmetry=True, hall=False, seed=0, triangle=False):
    assert n>=2 and n<=12
    rng=random.Random(seed)
    full=(1<<n)-1
    S=[[[c for c in range(n)]]+[[None]*n for _ in range(n-1)] for _ in range(3)]
    col=[[1<<c for c in range(n)] for _ in range(3)]
    # pair-used[a][b] bitmask of b-values used with a in the corresponding 2-square overlay
    pair=[[(1<<i) for i in range(n)] for _ in range(3)]
    # the diagonal symbols were already used by row 0 in all three pairs
    pairs=((0,1),(0,2),(1,2))
    nodes=0; row_nodes=[0]*n; deepest=0; timeout=False; snapshot=None; hall_checks=0; hall_prunes=0
    triangle_checks=0;triangle_prunes=0;triangle_prunes_by_depth=[0]*n;triangle_samples=[]
    start=time.monotonic()
    def triangle_supported():
        # All three bipartite residual edge graphs must be triangle-supported.
        AB=[full & ~pair[0][a] for a in range(n)]
        AC=[full & ~pair[1][a] for a in range(n)]
        BC=[full & ~pair[2][b] for b in range(n)]
        BCcol=[sum(1<<b for b in range(n) if BC[b]>>c&1) for c in range(n)]
        ABcol=[sum(1<<a for a in range(n) if AB[a]>>b&1) for b in range(n)]
        ACcol=[sum(1<<a for a in range(n) if AC[a]>>c&1) for c in range(n)]
        for a in range(n):
            bb=AB[a]
            while bb:
                bit=bb&-bb;bb-=bit;b=bit.bit_length()-1
                if not (AC[a]&BC[b]):return False
            cc=AC[a]
            while cc:
                bit=cc&-cc;cc-=bit;c=bit.bit_length()-1
                if not (AB[a]&BCcol[c]):return False
        for b in range(n):
            cc=BC[b]
            while cc:
                bit=cc&-cc;cc-=bit;c=bit.bit_length()-1
                if not (ABcol[b]&ACcol[c]):return False
        return True
    def rec_row(r):
        nonlocal nodes,deepest,timeout,snapshot,triangle_checks,triangle_prunes
        if triangle and r<n and r>1:
            triangle_checks+=1
            if not triangle_supported():
                triangle_prunes+=1;triangle_prunes_by_depth[r]+=1;return False
        if r-1>deepest:
            deepest=r-1
            snapshot=[[[int(z) for z in row] for row in A[:r]] for A in S]
        if triangle and r>=5 and len(triangle_samples)<12:
            triangle_samples.append([[[int(z) for z in row] for row in A[:r]] for A in S])
        if r==n:
            check(S)
            return True
        used=[0,0,0]
        def rec_col(remaining):
            nonlocal nodes,timeout,hall_checks,hall_prunes
            nodes+=1;row_nodes[r]+=1
            if nodes>node_budget or (nodes&8191)==0 and time.monotonic()-start>wall_seconds:
                timeout=True;raise TimeoutError
            if not remaining:
                return rec_row(r+1)
            best=None; bestC=None; candidate_by_col={}
            # Find most-constrained column and allowed value triples.
            for c in remaining:
                opts=[[] for _ in range(3)]
                for k in range(3):
                    avail=full & ~(col[k][c] | used[k])
                    if c==0 and k==0:avail &= 1<<r
                    opts[k]=[i for i in range(n) if avail>>i&1]
                cand=[]
                for x in opts[0]:
                    for y in opts[1]:
                        if pair[0][x]>>y&1:continue
                        for z in opts[2]:
                            if pair[1][x]>>z&1 or pair[2][y]>>z&1: continue
                            if symmetry and r==1 and c==0 and y>=z: continue
                            cand.append((x,y,z))
                candidate_by_col[c]=cand
                if best is None or len(cand)<len(best):
                    best=cand;bestC=c
                    if not best:return False
            if hall and len(remaining)>1:
                hall_checks+=1
                # Sound necessary condition: each of the three row permutations
                # must match remaining columns to distinct available symbols.
                for k in range(3):
                    options={c:sum((1<<t[k]) for t in candidate_by_col[c]) for c in remaining}
                    def match(i,visited):
                        if i==len(remaining):return True
                        c=sorted(remaining,key=lambda d:options[d].bit_count())[i]
                        bits=options[c]&~visited
                        while bits:
                            bit=bits&-bits;bits-=bit
                            if match(i+1,visited|bit):return True
                        return False
                    if not match(0,0):
                        hall_prunes+=1;return False
            c=bestC
            if seed: rng.shuffle(best)
            for x,y,z in best:
                xyz=(x,y,z)
                for k,v in enumerate(xyz):
                    S[k][r][c]=v;col[k][c] |= 1<<v;used[k] |= 1<<v
                for t,(a,b) in enumerate(pairs):
                    pair[t][xyz[a]] |= 1<<xyz[b]
                if rec_col(tuple(v for v in remaining if v!=c)):return True
                for t,(a,b) in enumerate(pairs):
                    pair[t][xyz[a]] ^= 1<<xyz[b]
                for k,v in enumerate(xyz):
                    S[k][r][c]=None;col[k][c] ^= 1<<v;used[k] ^= 1<<v
            return False
        return rec_col(tuple(range(n)))
    try:
        sat=rec_row(1)
        return {'n':n,'status':'SAT' if sat else 'UNSAT_EXHAUSTIVE_NORMALIZED','nodes':nodes,
           'row_nodes':row_nodes,'deepest_completed_row':deepest,
           'seconds':round(time.monotonic()-start,5),
           'symmetry':symmetry,'seed':seed,'hall':hall,'triangle':triangle,'triangle_checks':triangle_checks,'triangle_prunes':triangle_prunes,'triangle_prunes_by_depth':triangle_prunes_by_depth,'triangle_survivor_samples':triangle_samples,'hall_checks':hall_checks,'hall_prunes':hall_prunes,'partial_rows':snapshot,'squares':S if sat else None}
    except TimeoutError:
        return {'n':n,'status':'UNKNOWN_BUDGET','nodes':nodes,'row_nodes':row_nodes,
           'deepest_completed_row':deepest,
           'seconds':round(time.monotonic()-start,5),'symmetry':symmetry,'seed':seed,'hall':hall,'triangle':triangle,'triangle_checks':triangle_checks,'triangle_prunes':triangle_prunes,'triangle_prunes_by_depth':triangle_prunes_by_depth,'triangle_survivor_samples':triangle_samples,'hall_checks':hall_checks,'hall_prunes':hall_prunes,'partial_rows':snapshot}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--orders',type=int,nargs='+',default=[3,4,5,6,10])
    ap.add_argument('--budget',type=int,default=100000)
    ap.add_argument('--time',type=float,default=8.0)
    ap.add_argument('--hall',action='store_true')
    ap.add_argument('--triangle',action='store_true')
    ap.add_argument('--seed',type=int,default=0)
    a=ap.parse_args()
    for n in a.orders:
        print(json.dumps(solve(n,a.budget,a.time,hall=a.hall,seed=a.seed,triangle=a.triangle)),flush=True)
