#!/usr/bin/env python3
"""CAP-022: exact codimension-two fingerprints of 111/110 sections in F_3^6.

Self-contained stdlib arithmetic. Enumeration proves fingerprints for the
canonical 112-cap and ALL 112 one-point / 6216 two-point deletions.
Extending to arbitrary 110/111 caps uses external classification theorems
(Potechin 2008, Thackeray 2022), not this computation alone.
No random seed, external solver, GPU, or floating point.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import unittest

F112 = {(40,36,36):308,(45,45,22):56}
F111 = {(39,36,36):110,(40,36,35):198,
        (45,44,22):45,(45,45,21):11}
F110_ANTIPODAL = {(38,36,36):110,(40,35,35):198,
                 (44,44,22):45,(45,45,20):11}
F110_OTHER = {(38,36,36):38,(39,36,35):144,(40,35,35):63,
              (40,36,34):63,(44,44,22):18,(45,43,22):18,
              (45,44,21):18,(45,45,20):2}


def canonical_112():
    def orbit(rep):
        return {tuple(sorted(0 if x==0 else (x-1+s)%5+1 for x in rep))
                for s in range(5)}
    blocks = orbit((0,1,2)) | orbit((1,2,4))
    assert len(blocks)==10
    h={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
    for block in blocks:
        for signs in product((1,2),repeat=3):
            x=[0]*6
            for i,s in zip(block,signs):x[i]=s
            h.add(tuple(x))
    return tuple(sorted(h))


def projective_normals():
    return tuple(u for u in product(range(3),repeat=6)
                 if any(u) and next(v for v in u if v)!=2)


def counts(base_counts, deletions=()):
    c=list(base_counts)
    for v in deletions:c[v]-=1
    assert min(c)>=0
    return tuple(sorted(c,reverse=True))


def census():
    h=canonical_112();u=projective_normals()
    assert len(h)==112 and len(u)==364
    s=set(h)
    assert len(s)==112
    for x,y in combinations(h,2):
        assert tuple((-a-b)%3 for a,b in zip(x,y)) not in s
    rows=tuple(tuple(sum(a*b for a,b in zip(v,x))%3 for x in h) for v in u)
    base=tuple(tuple(row.count(t) for t in range(3)) for row in rows)
    baseline=Counter(counts(cs) for cs in base)
    assert baseline==F112,baseline
    one=Counter(); two=Counter(); observed_one=Counter(); observed_two=Counter()
    for i in range(112):
        hist=Counter(counts(cs,(row[i],)) for cs,row in zip(base,rows))
        assert hist==F111,(i,hist)
        one[tuple(sorted(hist.items()))]+=1
        observed_one[sum(t.count(45)*n for t,n in hist.items())]+=1
    for i in range(112):
        for j in range(i+1,112):
            hist=Counter(counts(cs,(row[i],row[j])) for cs,row in zip(base,rows))
            antipodal=all((a+b)%3==0 for a,b in zip(h[i],h[j]))
            expected=F110_ANTIPODAL if antipodal else F110_OTHER
            assert hist==expected,(i,j,antipodal,hist)
            two['antipodal' if antipodal else 'other']+=1
            observed_two[(antipodal,sum(t.count(45)*n for t,n in hist.items()))]+=1
    assert two=={'antipodal':56,'other':6160}
    assert observed_one=={67:112}
    assert observed_two=={(True,22):56,(False,40):6160}
    return {'dimension':6,'canonical_size':112,'projective_normals':364,
            'all_one_point_deletions':sum(one.values()),
            'all_two_point_deletions':sum(two.values()),
            'two_point_type_counts':dict(two),
            'F112':encode(F112),'F111':encode(F111),
            'F110_antipodal':encode(F110_ANTIPODAL),
            'F110_nonantipodal':encode(F110_OTHER),
            'five_dimensional_45_cell_counts':{'112':112,'111':67,
                                              '110_antipodal':22,
                                              '110_nonantipodal':40}}


def encode(h):
    return [[list(t),n] for t,n in sorted(h.items())]


@lru_cache(maxsize=1)
def cached():return census()


class CAP022(unittest.TestCase):
    def test_all_112_single_deletions(self):
        self.assertEqual(cached()['all_one_point_deletions'],112)
    def test_all_6216_pair_deletions(self):
        r=cached();self.assertEqual(r['all_two_point_deletions'],6216)
        self.assertEqual(r['two_point_type_counts'],{'antipodal':56,'other':6160})
    def test_fingerprint_is_exact(self):
        r=cached();self.assertEqual(sum(n for _,n in r['F111']),364)
        self.assertEqual(sum(n for _,n in r['F110_antipodal']),364)
        self.assertEqual(sum(n for _,n in r['F110_nonantipodal']),364)
    def test_45_cell_signature(self):
        self.assertEqual(cached()['five_dimensional_45_cell_counts'],
                         {'112':112,'111':67,'110_antipodal':22,'110_nonantipodal':40})

if __name__=='__main__':
    import json
    print(json.dumps(cached(),sort_keys=True,indent=2))
    unittest.main(verbosity=2)
