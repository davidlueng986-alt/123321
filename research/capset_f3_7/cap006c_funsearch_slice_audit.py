#!/usr/bin/env python3
"""CAP-006C: independently check FunSearch published n8 512-cap, all 3280
7D hyperplane-direction sections, and bounded 24-direction greedy projections.
The 512 data comes from google-deepmind/funsearch (Apache-2.0) and is known,
NOT a discovery by this campaign. A greedy negative result is NOT optimality.
"""
from pathlib import Path
from itertools import combinations,product
import argparse,json

DATA=Path(__file__).resolve().parent/'reference'/'funsearch_n8_size512.txt'
MASK32=(1<<32)-1

def read():
    pts=[tuple(json.loads(s)) for s in DATA.read_text().splitlines() if s.strip()]
    assert len(pts)==512 and len(set(pts))==512
    assert all(len(p)==8 and all(x in (0,1,2) for x in p) for p in pts)
    return pts

def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
def check_cap(pts):
    S=set(pts)
    return len(pts)==len(S) and all(third(a,b) not in S for a,b in combinations(pts,2))

def normals():
    # 3^8-1 nonzero vectors modulo v~-v, unique first nonzero=1.
    return [a for a in product(range(3),repeat=8)
            if any(a) and next(x for x in a if x)!=2]

def spectrum(pts):
    assert check_cap(pts)
    hist={}
    best=[]
    for v in normals():
        counts=[0,0,0]
        for p in pts:counts[sum(x*y for x,y in zip(v,p))%3]+=1
        mx=max(counts)
        hist[mx]=hist.get(mx,0)+1
        if mx>=208:best.append({'normal':''.join(map(str,v)),'slice_counts':counts})
    assert sum(hist.values())==3280
    assert max(hist)==208 and hist[208]==8
    return {'verified_512_cap':True,'directions':3280,'max_7D_section':max(hist),
            'directions_attaining_208':hist[208],
            'max_section_illustrations':best,'direction_max_histogram':hist}

def xorshift(seed):
    while True:
        seed ^= (seed << 13) & MASK32
        seed ^= seed >> 17
        seed ^= (seed << 5) & MASK32
        seed &= MASK32
        yield seed

def projection_images(pts,v):
    pivot=next(i for i,x in enumerate(v) if x)
    assert v[pivot]==1
    # Quotient by span(v): choose representative with pivot coordinate zero.
    seen={}
    for p in pts:
        t=tuple((p[i]-p[pivot]*v[i])%3 for i in range(8) if i!=pivot)
        seen.setdefault(t,None)
    return list(seen)

def greedy(pts,seed):
    arr=list(pts);r=xorshift(seed)
    for i in range(len(arr)-1,0,-1):
        j=next(r)%(i+1)
        arr[i],arr[j]=arr[j],arr[i]
    chosen=[];blocked=set()
    for p in arr:
        if p in blocked:continue
        for q in chosen:blocked.add(third(p,q))
        chosen.append(p)
    assert check_cap(chosen)
    return chosen

def pilot(pts):
    dirs=[]
    for i in range(8):
        a=[0]*8;a[i]=1;dirs.append(tuple(a))
    r=xorshift(20261102)
    while len(dirs)<24:
        v=tuple(next(r)%3 for _ in range(8))
        if not any(v):continue
        if next(x for x in v if x)==2:v=tuple(2*x%3 for x in v)
        if v not in dirs:dirs.append(v)
    out=[]
    for v in dirs:
        V=projection_images(pts,v)
        key=sum(x*3**i for i,x in enumerate(v))
        best=0
        for t in range(12):
            selected=greedy(V,20261102+t*1009+key)
            best=max(best,len(selected))
        out.append({'direction':''.join(map(str,v)),'projection_image_size':len(V),
                    'best_of_12_greedy':best})
    assert len(out)==24
    # The numerical score is reproducible, but is not a cap record.
    return {'directions':24,'trials':288,'seed':20261102,
            'best':max(x['best_of_12_greedy'] for x in out),
            'scores':out,'search_scope':'randomly ordered greedy extractions only'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pilot',action='store_true')
    a=p.parse_args()
    P=read();out={'source':'google-deepmind/funsearch cap_set/n8_size512.txt',
                  'upstream_blob_sha':'c3223715044c50da299e9fd68ef2324bdf3784d5',
                  'hyperplane_spectrum':spectrum(P)}
    if a.pilot:out['projection_pilot']=pilot(P)
    print(json.dumps(out,sort_keys=True))
