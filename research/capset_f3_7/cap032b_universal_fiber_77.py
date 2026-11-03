#!/usr/bin/env python3
"""CAP-032B exact AG(4,3) parallel 7+7 slice obstruction.
All 126360 7-caps in F3^3, explicit AGL3 orbit coverage, all second caps,
all potential 5-point subsets of third-slice holes. Pure stdlib CPU.
Universal finite theorem, NOT global r3(7) numerical bound/novelty claim.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
V=[tuple((i//3**j)%3 for j in range(3)) for i in range(27)]
def enc(p):return sum(x*3**j for j,x in enumerate(p))
third=[[enc(tuple((-x-y)%3 for x,y in zip(a,b))) for b in V] for a in V]
def members(mask):
    while mask:
        v=mask&-mask;yield v.bit_length()-1;mask-=v
def caps7():
    ans=[]
    for c in combinations(range(27),7):
        m=sum(1<<p for p in c)
        if all(not(m>>third[a][b]&1) for a,b in combinations(c,2)):ans.append(m)
    assert len(ans)==126360
    return ans
def affine_maps():
    def gen(a):
        for i in range(3):
            b=list(a);b[i]=(b[i]+1)%3;yield tuple(b)
        b=list(a);b[0],b[1]=b[1],b[0];yield tuple(b)
        b=list(a);b[1],b[2]=b[2],b[1];yield tuple(b)
        b=list(a);b[0]=2*b[0]%3;yield tuple(b)
        for i in range(3):
            for j in range(3):
                if i!=j:
                    b=list(a);b[i]=(a[i]+a[j])%3;yield tuple(b)
    maps=[[] for _ in range(12)]
    for p in V:
        for j,q in enumerate(gen(p)):maps[j].append(enc(q))
    assert all(len(set(g))==27 for g in maps)
    return maps
def apply(m,g):
    out=0
    for p in members(m):out|=1<<g[p]
    return out
def reps(all_caps):
    transforms=affine_maps();S=set(all_caps);seen=set();r=[];sizes=[]
    for a in all_caps:
        if a in seen:continue
        todo=[a];seen.add(a)
        for x in todo:
            for g in transforms:
                y=apply(x,g)
                assert y in S
                if y not in seen:seen.add(y);todo.append(y)
        r.append(a);sizes.append(len(todo))
    assert len(seen)==126360 and sorted(sizes)==[50544,75816]
    return r,sizes
def cap5(five):
    m=sum(1<<p for p in five)
    return all(not(m>>third[a][b]&1) for a,b in combinations(five,2))
def audit():
    all_caps=caps7();R,sizes=reps(all_caps);hists=[];exceptional=0
    for A in R:
        rows=[[1<<third[a][b] for b in range(27)] for a in members(A)]
        hist=Counter()
        for B in all_caps:
            blocked=0;bp=tuple(members(B))
            for row in rows:
                for b in bp:blocked|=row[b]
            H=((1<<27)-1)^blocked;h=H.bit_count();hist[h]+=1
            if h>=5:
                exceptional+=1;points=list(members(H))
                assert not any(cap5(c) for c in combinations(points,5)),(A,B,points)
        hists.append(dict(sorted(hist.items())))
    assert hists==[{0:2916,1:15471,2:72036,3:29457,4:6399,5:81},
                   {0:1728,1:18090,2:69471,3:31860,4:5103,5:81,6:27}]
    assert exceptional==189
    record=json.loads((Path(__file__).resolve().parent/'CAP028_4d_quotient_line_certificate.json').read_text())
    W=[tuple(x) for x in record['witness_774']]
    assert len(W)==18 and [sum(x[0]==i for x in W) for i in range(3)]==[7,7,4]
    S=set(W);assert len(S)==18
    assert all(tuple((-a-b)%3 for a,b in zip(p,q)) not in S for p,q in combinations(W,2))
    return {'n7caps':126360,'affine_orbit_sizes':sizes,'representatives':R,
            'pairs_checked':252720,'exceptional_holes_ge5':189,'feasible_5caps':0,
            'third_slice_exact_max_given_7_7':4,'sharp_18point_witness':True,
            'global_r3_7_bound_improved':False,'literature_novelty_established':False}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True))
