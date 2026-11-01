#!/usr/bin/env python3
"""CAP-005A: exact <=4 coordinate 4D fiber reconstruction obstruction."""
import itertools, json
from collections import Counter
from pathlib import Path
from verify_capset import read_points, verify
HERE=Path(__file__).resolve().parent
def fiber(p): return 9*p[0]+3*p[1]+p[2]
def analyze():
    P=read_points(HERE/"candidates"/"calderbank_fishburn_236.txt")
    assert verify(P)==236
    S=set(P)
    outsiders=set(itertools.product(range(3),repeat=7))-S
    assert len(outsiders)==1951
    edges={x:set() for x in outsiders}
    counts=Counter()
    for a,b in itertools.combinations(P,2):
        x=tuple((-a[i]-b[i])%3 for i in range(7))
        if x in edges:
            edges[x].add((1<<fiber(a))|(1<<fiber(b)))
            counts[x]+=1
    assert len(counts)==1951 and (min(counts.values()),max(counts.values()))==(10,56)
    by=[[] for _ in range(27)]
    for x,es in edges.items(): by[fiber(x)].append(tuple(es))
    hist={}; maxima={}
    for k in range(1,5):
        dist=Counter()
        for group in itertools.combinations(range(27),k):
            mask=sum(1<<j for j in group)
            n=sum(all(e&mask for e in es) for j in group for es in by[j])
            dist[n]+=1
        assert sum(dist.values())==(27,351,2925,17550)[k-1]
        hist[str(k)]={str(n):dist[n] for n in sorted(dist)}
        maxima[str(k)]=max(dist)
    assert hist=={
        "1":{"0":27},
        "2":{"0":335,"1":16},
        "3":{"0":2501,"1":408,"2":8,"4":8},
        "4":{"0":12510,"1":4320,"2":408,"4":160,"5":96,"6":56},
    }
    assert maxima=={"1":0,"2":1,"3":4,"4":6}
    return {"status":"NO_IMPROVEMENT_WITH_AT_MOST_FOUR_RELEASED_FIBERS",
            "baseline_size":236,"outsiders":1951,"min_secants":10,"max_secants":56,
            "histograms":hist,"max_admissible_outsiders":maxima,
            "scope":"Only first-three-coordinate fibers; <=4 editable","seed":None,"gpu":False}
if __name__=="__main__": print(json.dumps(analyze(),sort_keys=True))
