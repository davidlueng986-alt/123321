#!/usr/bin/env python3
"""Exact exhaustive 7-row-anchored 3MOLS10 extension to full ten rows.
Given a 7x10 triple (obtained by deleting 2 rows from a published 9x10
MOLR), enumerate every legal row 8, every two-row Latin completion,
then check all three 100-pair overlays. NO symmetry pruning.
"""
import itertools,json,time,argparse,functools,sys
N=10; PAIRS=((0,1),(0,2),(1,2))

def bitpair(row,other):
    b=0
    for a,c in zip(row,other):
        k=10*a+c
        if b>>k&1:return None
        b |= 1<<k
    return b

def latin_rows(A):
    n=10
    missing=[[v for v in range(n) if v not in {row[c] for row in A}] for c in range(n)]
    assert all(len(x)==n-len(A) for x in missing)
    out=[];p=[0]*10
    def dfs(col,seen):
        if col==10:out.append(tuple(p));return
        for v in missing[col]:
            if not(seen>>v&1):p[col]=v;dfs(col+1,seen|(1<<v))
    dfs(0,0);return out

@functools.lru_cache(maxsize=None)
def last2(W, x):
    rows=list(W)+[x]
    last=latin_rows(rows)
    assert len(rows)==8
    missing=[[v for v in range(10) if v not in {r[c] for r in rows}] for c in range(10)]
    assert all(len(z)==2 for z in missing)
    return [(p,tuple(next(v for v in missing[c] if v!=p[c]) for c in range(10))) for p in last]

def check_full(S):
    assert len(S)==3
    for Q in S:
        assert len(Q)==10
        assert all(set(row)==set(range(10)) for row in Q)
        assert all({Q[r][c] for r in range(10)}==set(range(10)) for c in range(10))
    counts=[len({(S[a][r][c],S[b][r][c]) for r in range(10) for c in range(10)}) for a,b in PAIRS]
    assert counts==[100]*3,counts
    return counts

def solve(source, omitted, sec_budget=30):
    t0=time.monotonic();W=[[tuple(row) for i,row in enumerate(Q) if i not in omitted] for Q in source]
    assert all(len(Q)==7 for Q in W)
    S=[latin_rows(Q) for Q in W]
    counts=dict(omitted=list(omitted),row8_options=list(map(len,S)),row8_triples=0,row9_triples=0,row10_completed=0,status='UNKNOWN_BUDGET')
    used=[]
    for a,b in PAIRS:
        u={10*W[a][r][c]+W[b][r][c] for r in range(7) for c in range(10)}
        assert len(u)==70
        used.append(sum(1<<i for i in u))
    pair_cache={}
    for pairindex,(a,b) in enumerate(PAIRS):
        opts=[]
        for ra in S[a]:
            v=[]
            for rb in S[b]:
                m=bitpair(ra,rb)
                v.append(m if m is not None and m & used[pairindex]==0 else 0)
            opts.append(v)
        pair_cache[pairindex]=opts
    for ia,ra in enumerate(S[0]):
        viable_b=[ib for ib in range(len(S[1])) if pair_cache[0][ia][ib]]
        for ib in viable_b:
            rb=S[1][ib]
            for ic,rc in enumerate(S[2]):
                mab=pair_cache[0][ia][ib];mac=pair_cache[1][ia][ic];mbc=pair_cache[2][ib][ic]
                if not(mac and mbc): continue
                counts['row8_triples']+=1
                if time.monotonic()-t0>sec_budget:
                    counts['seconds']=round(time.monotonic()-t0,4);return counts
                temp=[W[a]+[row] for a,row in enumerate((ra,rb,rc))]
                used8=[mab|used[0],mac|used[1],mbc|used[2]]
                options=[last2(tuple(W[a]),v) for a,v in enumerate((ra,rb,rc))]
                for r9a,r10a in options[0]:
                    for r9b,r10b in options[1]:
                        b9=bitpair(r9a,r9b);b10=bitpair(r10a,r10b)
                        if b9 is None or b10 is None or (b9|b10).bit_count()!=20 or (b9|b10)&used8[0]:continue
                        for r9c,r10c in options[2]:
                            c9=bitpair(r9a,r9c);c10=bitpair(r10a,r10c)
                            if c9 is None or c10 is None or (c9|c10).bit_count()!=20 or (c9|c10)&used8[1]:continue
                            d9=bitpair(r9b,r9c);d10=bitpair(r10b,r10c)
                            if d9 is None or d10 is None or (d9|d10).bit_count()!=20 or (d9|d10)&used8[2]:continue
                            sol=[temp[0]+[r9a,r10a],temp[1]+[r9b,r10b],temp[2]+[r9c,r10c]]
                            counts['status']='SAT';counts['witness']=sol
                            check_full(sol)
                            counts['seconds']=round(time.monotonic()-t0,4)
                            return counts
                        counts['row9_triples']+=len(options[2])
    counts['status']='UNSAT_FIXED_SEVEN_ROWS';counts['seconds']=round(time.monotonic()-t0,4)
    return counts

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',default=str(Path(__file__).with_name('E059_2024_9x10_analysed.json')));ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--output',default=str(Path(__file__).with_name('E060_seven_row_results.json')));args=ap.parse_args()
    source=json.load(open(args.source))['published_9x10_rectangles'];results=[]
    for om in itertools.combinations(range(9),2):
        R=solve(source,om,args.seconds);results.append(R);print(json.dumps({k:v for k,v in R.items() if k!='witness'}),flush=True)
        if R['status']=='SAT': break
    summary={'origin':'Jäger et al 2024 Figure 3 one nine-row triple','method':'exhaustive two missing published rows then all 3 new rows; no symmetry pruning','total_cases':len(results),'fixed_seven_row_unsat':sum(x['status']=='UNSAT_FIXED_SEVEN_ROWS' for x in results),'unknown':sum(x['status']=='UNKNOWN_BUDGET' for x in results),'sat':sum(x['status']=='SAT' for x in results),'results':results}
    json.dump(summary,open(args.output,'w'),indent=2)
    print('SUMMARY',json.dumps({k:v for k,v in summary.items() if k!='results'}),flush=True)