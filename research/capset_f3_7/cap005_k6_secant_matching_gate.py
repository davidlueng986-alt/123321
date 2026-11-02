#!/usr/bin/env python3
"""CAP-005D: exact necessary six-fiber secant-cover census (NOT a global bound)."""
import itertools, json, math, argparse
from collections import Counter
from pathlib import Path
from verify_capset import read_points, verify

def fiber(p): return 9*p[0]+3*p[1]+p[2]

def census():
    P=read_points(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt')
    assert verify(P)==236
    outsiders=set(itertools.product(range(3),repeat=7))-set(P)
    assert len(outsiders)==1951
    edges={x:set() for x in outsiders}
    pairs={x:set() for x in outsiders}
    for a,b in itertools.combinations(P,2):
        x=tuple((-u-v)%3 for u,v in zip(a,b))
        if x in edges:
            fa,fb=fiber(a),fiber(b)
            edges[x].add((1<<fa)|(1<<fb))
            if fa!=fb:pairs[x].add(tuple(sorted((fa,fb))))
    by=[[] for _ in range(27)]
    active=Counter()
    for x in sorted(outsiders):
        f=fiber(x); pp=pairs[x]; active[len(pp)]+=1
        assert edges[x] and len({v for a,b in pp for v in (a,b)})==2*len(pp)
        assert all(a!=f and b!=f for a,b in pp)
        if len(pp)<=5:by[f].append((x,tuple((1<<a)|(1<<b) for a,b in pp)))
    hist={}; maxgroups=[]
    for k in (5,6):
        counts=Counter(); maximum=-1
        for group in itertools.combinations(range(27),k):
            mask=sum(1<<j for j in group)
            n=sum(all(mask&e for e in ee) for j in group for _,ee in by[j])
            counts[n]+=1
            if k==6:
                if n>maximum:maximum=n;maxgroups=[list(group)]
                elif n==maximum:maxgroups.append(list(group))
        assert sum(counts.values())==math.comb(27,k)
        hist[str(k)]={str(n):v for n,v in sorted(counts.items())}
    assert hist['5']=={'0':44392,'1':25872,'2':5384,'3':344,'4':1434,
       '5':1576,'6':1136,'7':152,'9':128,'10':152,'11':32,'12':16,
       '13':32,'14':40,'15':16,'18':8,'20':8,'22':8}
    h6=hist['6']; excluded=sum(v for n,v in h6.items() if int(n)<10)
    assert (excluded,296010-excluded,maximum,len(maxgroups))==(288878,7132,92,16)
    for group in maxgroups:
        mask=sum(1<<j for j in group)
        # Independently replay original secant-edge condition, without matching shortcut.
        assert sum(bool(mask&(1<<fiber(x))) and all(mask&e for e in edges[x])
                   for x in outsiders)==92
    return {'status':'NECESSARY_ONLY_NOT_GLOBAL','baseline':236,'release_sets':296010,
            'excluded_by_ten_deletion_gate':excluded,'unresolved':7132,
            'at_least_20_outsiders':sum(v for n,v in h6.items() if int(n)>=20),
            'max_admissible_outsiders':maximum,'max_groups':maxgroups,
            'active_pair_histogram':{str(k):v for k,v in sorted(active.items())},
            'histograms':hist,'seed':None,'gpu':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);a=p.parse_args()
    result=census();data=json.dumps(result,sort_keys=True)
    if a.out:a.out.write_text(data+'\n',encoding='utf-8')
    print(data)
