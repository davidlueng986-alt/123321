#!/usr/bin/env python3
"""CAP-020: exact F3 arithmetic verifier for antipodal secant separation.

Only Python stdlib, no solver, GPU, randomness or numerical approximations.
The general lemma is proved in CAP020 report; this file certifies the
canonical 112-cap's uniform 10 secants and tests a linear shear.
"""
from collections import Counter
from itertools import combinations, product
import unittest

ZERO = (0,)*6

def neg(x): return tuple((-a)%3 for a in x)
def third(x,y): return tuple((-a-b)%3 for a,b in zip(x,y))
def canonical():
    def orbit(rep):
        return {tuple(sorted(0 if x==0 else (x-1+s)%5+1 for x in rep)) for s in range(5)}
    blocks = orbit((0,1,2)) | orbit((1,2,4))
    assert len(blocks)==10
    h={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
    for block in blocks:
        for signs in product((1,2),repeat=3):
            x=[0]*6
            for i,s in zip(block,signs):x[i]=s
            h.add(tuple(x))
    return h

def shear(x):
    return ((x[0]+x[1])%3,x[1],(x[2]+x[3])%3,x[3],x[4],x[5])

def secants(h):
    """For every z, list unordered {x,y} with x+y+z=0 and x!=y."""
    out={z:[] for z in product(range(3),repeat=6)}
    for x,y in combinations(sorted(h),2):out[third(x,y)].append((x,y))
    return out

def certify(h):
    assert len(h)==112 and ZERO not in h and {neg(x) for x in h}==h
    assert all(third(x,y) not in h for x,y in combinations(sorted(h),2))
    s=secants(h)
    hist=Counter(len(pairs) for pairs in s.values())
    assert hist=={0:112,10:616,56:1},hist
    assert len(s[ZERO])==56
    orbit_hist=Counter()
    for z,pairs in s.items():
        if z==ZERO:continue
        endpoints=[x for edge in pairs for x in edge]
        # For nonzero z, each secant endpoint lies in a different +/- orbit.
        ids={min(x,neg(x)) for x in endpoints}
        assert len(ids)==len(endpoints)==2*len(pairs),(z,len(ids),len(endpoints))
        orbit_hist[len(ids)]+=1
    assert orbit_hist=={0:112,20:616},orbit_hist
    return {"points":len(h),"secants_by_z":dict(sorted(hist.items())),
            "nonzero_z_distinct_antipodal_orbits":dict(sorted(orbit_hist.items()))}

def high_dual_directions(h):
    """Direct signed ternary Fourier support from 364 projective normals."""
    high=set()
    for u in product(range(3),repeat=6):
        if not any(u) or next(t for t in u if t)!=1:continue
        a=[0,0,0]
        for x in h:a[sum(t*v for t,v in zip(u,x))%3]+=1
        if a==[22,45,45]:high.add(u)
        else:assert a==[40,36,36],(u,a)
    assert len(high)==56
    return high

def improved_bounds():
    # If D1!=D2, 112-point centered symmetric caps have overlap <=92,
    # so their 56 projective high-frequency directions intersect in m<=46.
    out=[]
    for d in range(5):
        old=165*(44+d)//(126-d)
        new=3*46*(44+d)//(2*46+16-d)
        assert new<=old
        out.append((d,old,new))
    assert [row[2] for row in out]==[56,58,59,61,63]
    return out

class CAP020(unittest.TestCase):
    def test_canonical_full_secant_census(self):
        self.assertEqual(certify(canonical())["secants_by_z"],{0:112,10:616,56:1})
    def test_nonorthogonal_linear_shear(self):
        self.assertEqual(certify({shear(x) for x in canonical()})["nonzero_z_distinct_antipodal_orbits"],{0:112,20:616})
    def test_zero_is_exception(self):
        h=canonical(); p=secants(h)[ZERO]
        self.assertEqual(len(p),56)
        self.assertEqual(len({min(x,neg(x)) for edge in p for x in edge}),56)
    def test_fourier_dual_shear_overlap(self):
        h=canonical();g={shear(x) for x in h}
        high_h=high_dual_directions(h);high_g=high_dual_directions(g)
        self.assertEqual(len(high_h&high_g),20)
        self.assertEqual(len(h&g),40)
        self.assertLessEqual(2*len(high_h&high_g),92)
    def test_refined_tangent_bounds(self):
        self.assertEqual([b for _,_,b in improved_bounds()],[56,58,59,61,63])

if __name__=="__main__":
    print("Canonical:",certify(canonical()))
    print("Sheared:",certify({shear(x) for x in canonical()}))
    print("d, old CAP017B, refined:",improved_bounds())
    unittest.main(verbosity=2)
