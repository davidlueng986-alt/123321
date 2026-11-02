#!/usr/bin/env python3
"""CAP-005F: exact pair-conflict clique-cover certificates for six-fiber edits.
Restricted to the fixed 236-point baseline and first-three-coordinate fibers.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from verify_capset import read_points, verify

HERE=Path(__file__).resolve().parent
def fiber(p): return 9*p[0]+3*p[1]+p[2]
def third(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))

def eligible_outsiders(points):
    members=set(points)
    outsiders=sorted(set(itertools.product(range(3),repeat=7))-members)
    secants={x:set() for x in outsiders}
    for a,b in itertools.combinations(points,2):
        x=third(a,b)
        if x in secants:
            secants[x].add((1<<fiber(a))|(1<<fiber(b)))
    by=[[] for _ in range(27)]
    for x in outsiders:
        f=fiber(x)
        required=tuple(sorted(e for e in secants[x] if not(e&(1<<f))))
        if len(required)<=5: by[f].append((x,required))
    return by

def dsatur_cover(candidates,released,members):
    """Proper coloring of the compatibility graph partitions into conflict cliques."""
    n=len(candidates)
    fixed={p for p in members if fiber(p) not in released}
    incompatible=[set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if third(candidates[i],candidates[j]) in fixed:
                incompatible[i].add(j)
                incompatible[j].add(i)
    compatible=[set(range(n))-{i}-incompatible[i] for i in range(n)]
    colors=[-1]*n
    while -1 in colors:
        uncolored=(i for i in range(n) if colors[i]<0)
        def score(i):
            return (len({colors[j] for j in compatible[i] if colors[j]>=0}),
                    len(compatible[i]),-i)
        i=max(uncolored,key=score)
        used={colors[j] for j in compatible[i] if colors[j]>=0}
        c=0
        while c in used: c+=1
        colors[i]=c
    classes=[[] for _ in range(max(colors)+1)]
    for p,c in zip(candidates,colors):
        classes[c].append(''.join(map(str,p)))
    return classes

def generate(points):
    assert verify(points)==236
    by=eligible_outsiders(points)
    hist=Counter()
    certs=[]
    members=set(points)
    for group in itertools.combinations(range(27),6):
        mask=sum(1<<j for j in group)
        candidates=[x for f in group for x,req in by[f] if all(mask&e for e in req)]
        n=len(candidates)
        hist[n]+=1
        if n>=17:
            classes=dsatur_cover(candidates,set(group),members)
            if len(classes)<=16:
                certs.append({'fibers':list(group),'classes':classes})
    assert sum(hist.values())==296010
    assert sum(v for n,v in hist.items() if n<=16)==294394
    assert sum(v for n,v in hist.items() if n>=17)==1616
    assert len(certs)==680, len(certs)
    return {'scope':'fixed classical 236 cap; exactly six released first-three-coordinate fibers',
            'method':'partition all admissible outsiders into <=16 fixed-original-point conflict cliques',
            'baseline_size':236,'required_insertions_for_improvement':17,
            'release_sets':296010,'previously_excluded':294394,
            'new_certificates':len(certs),'total_excluded':294394+len(certs),
            'unresolved':1616-len(certs),'seed':None,'gpu':False,'certificates':certs}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    P=read_points(HERE/'candidates'/'calderbank_fishburn_236.txt')
    result=generate(P)
    args.out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='certificates'},sort_keys=True))
if __name__=='__main__': main()
