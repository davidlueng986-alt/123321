"""Reproduce published DeepMind n8 512 cap (google-deepmind/funsearch notebook),
and independently test all dimension-7 affine hyperplane slices.
This does not claim a new cap record, its purpose is an independent NONLOCAL
constructive branch for the open n7 target237. Exact final arithmetic checks.
"""
import numpy as np
from itertools import product
from collections import Counter
from pathlib import Path

def priority(el,n):
    score=n;in_el=0;el_count=el.count(0)
    if el_count==0:
        score+=n**2
        if el[1]==el[-1]:score*=1.5
        if el[2]==el[-2]:score*=1.5
        if el[3]==el[-3]:score*=1.5
    else:
        if el[1]==el[-1]:score*=.5
        if el[2]==el[-2]:score*=.5
    for e in el:
        if e==0:
            if in_el==0:score*=n*.5
            elif in_el==el_count-1:score*=.5
            else:score*=n*.5**in_el
            in_el+=1
        else:score+=1
    if el[1]==el[-1]:score*=1.5
    if el[2]==el[-2]:score*=1.5
    return score

def make512():
    n=8
    V=np.array(list(product(range(3),repeat=n)),dtype=np.int16)
    pow3=3**np.arange(n-1,-1,-1,dtype=np.int32)
    scores=np.array([priority(tuple(map(int,p)),n) for p in V])
    x=[]
    while np.any(scores!=-np.inf):
        i=int(np.argmax(scores));p=V[i]
        for a in x:
            b=(-a-p)%3;scores[int(b@pow3)]=-np.inf
        scores[i]=-np.inf
        x.append(p)
    cap=np.array(x,dtype=np.int16)
    assert cap.shape==(512,8),len(cap)
    S={tuple(map(int,p)) for p in cap}
    assert len(S)==512
    for i in range(512):
        for j in range(i+1,512):
            z=tuple(map(int,(-cap[i]-cap[j])%3))
            assert z not in S,(i,j)
    return cap

def hyperplanes(cap):
    # Select one representative of every projective normal +/-.
    normals=[]
    for p in product(range(3),repeat=8):
        if all(x==0 for x in p):continue
        if next(x for x in p if x)!=1:continue
        normals.append(p)
    assert len(normals)==3280
    H=[];maxsize=0;top=[]
    for normal in normals:
        counts=np.bincount((cap@np.array(normal,dtype=np.int16))%3,minlength=3)
        sizes=tuple(map(int,counts))
        H.append(sizes)
        mx=max(sizes)
        if mx>maxsize:maxsize=mx;top=[(normal,sizes)]
        elif mx==maxsize:top.append((normal,sizes))
    return {'projective_normal_count':3280,'max_7D_hyperplane_cap':maxsize,
            'max_attaining_hyperplanes':len(top),'first_five_top':top[:5],
            'all_slice_max_histogram':dict(sorted(Counter(max(t) for t in H).items()))}

if __name__=='__main__':
    import json
    B=make512()
    result=hyperplanes(B)
    print(json.dumps(result,sort_keys=True))
    with open('/mnt/data/capset_047/FUNSEARCH_512_SOURCE_POINTS.txt','w') as f:
        f.write('n: 8\n')
        for p in B:f.write(''.join(map(str,p))+'\n')