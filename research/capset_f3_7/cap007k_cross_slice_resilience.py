#!/usr/bin/env python3
"""CAP-007K pilot: exact CROSS-SLICE representation multiplicities.
Finite relative GL6 family: identity and elementary products of word length <=2.
No general relative GL6 coverage or full r3(7) result.
"""
from collections import Counter,defaultdict
from pathlib import Path
from cap007j_112_alignment import read_fixture,matrix_family,transform,third,encode
import json
def audit(path=None):
    path=path or Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'
    A,B,_=read_fixture(path)
    hist=Counter();mult=Counter();paired=Counter();examples={}
    for mat in matrix_family():
        C=[0]*729
        for b in B:
            tb=transform(mat,b)
            for a in A:
                C[encode(third(a,tb))]+=1
        holes=C.count(0)
        minimum=min(x for x in C if x)
        hist[holes]+=1
        mult[minimum]+=1
        paired[(holes,minimum)]+=1
        examples.setdefault((holes,minimum),''.join(str(v) for row in mat for v in row))
        assert sum(C)==112*112
    assert hist==Counter({0:3505,1:126,4:60,12:121})
    assert mult==Counter({5:70,6:720,7:15,8:1260,10:1500,11:121,16:126})
    assert paired[(12,11)]==121
    assert all(h!=12 or m==11 for (h,m) in paired)
    return {'matrices':3812,'hole_histogram':dict(sorted(hist.items())),
            'positive_minimum_representation_histogram':dict(sorted(mult.items())),
            'hole_and_minimum_histogram':{f'{h}:{m}':n for (h,m),n in sorted(paired.items())},
            'example_matrices':{f'{h}:{m}':v for (h,m),v in sorted(examples.items())},
            'lemma':'For all 121 matrices with 12 holes, deleting <=10 second-slice points cannot create a new third-slice hole; every blocked location has at least 11 representations.',
            'status':'restricted exact finite enumeration only, global r3(7) OPEN'}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True))
