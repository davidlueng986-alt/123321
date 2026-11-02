#!/usr/bin/env python3
"""CAP-026: exact 285-point max109-slice quadratic rigidity certificate.
No solver, RNG, GPU or non-stdlib dependency. Necessary condition only."""
from collections import Counter
from itertools import product, combinations
from pathlib import Path
import unittest

M=285
N=(3**7-1)//2
S2=364*M*M+729*M
S3=121*M*(M-1)*(M-2)+1092*M*(M-1)+1093*M
FORMAL={(109,109,67):152,(100,95,90):1,(99,98,88):1,
        (99,94,92):1,(99,93,93):1,(98,95,92):1,
        (97,94,94):10,(96,96,93):39,(96,95,94):726,
        (95,95,95):161}

def category(t):
    r={x%3 for x in t}
    if len(r)==1:return 'Q'+str(next(iter(r)))
    assert r=={0,1,2}
    return 'T'

def profiles():
    for a in range(109,-1,-1):
        for b in range(min(a,M-a),-1,-1):
            c=M-a-b
            if 0<=c<=b:yield (a,b,c)

def powers(t):
    return sum(x*x for x in t),sum(x*x*x for x in t)

def slacks(t):
    a,b=powers(t);typ=category(t)
    # First two inequalities apply to Type-0 directions only.
    f2=1176*(typ=='Q2')+71449749-4064*a+15*b
    f1=1176*(typ=='Q1')+4792275-272*a+b
    # Third applies to every sorted profile, Type-0 or Type-1.
    f0=b-271*a+4765200-28*(typ=='T')-78*(typ=='Q0')
    return f2,f1,f0

def spectrum_dp(k,rank,last):
    diag=([1]*(rank-1)+[last] if rank else [])+[0]*(k-rank)
    counts=[1,0,0]
    for d in diag:
        nxt=[0,0,0]
        for r in range(3):
            nxt[r]+=counts[r];nxt[(r+d)%3]+=2*counts[r]
        counts=nxt
    return ((counts[0]-1)//2,counts[1]//2,counts[2]//2)

def spectrum_brute(k,rank,last):
    diag=([1]*(rank-1)+[last] if rank else [])+[0]*(k-rank)
    counts=[0,0,0]
    for v in product(range(3),repeat=k):
        if not any(v) or next(z for z in v if z)!=1:continue
        counts[sum(d*x*x for d,x in zip(diag,v))%3]+=1
    return tuple(counts)

def certificate():
    ps=list(profiles())
    assert len(ps)==169 and (S2,S3)==(29773665,2860326405)
    for t in ps:
        f2,f1,f0=slacks(t)
        assert f0>=0,(t,f0)
        if category(t)!='T':assert f1>=0 and f2>=0,(t,f1,f2)
    # b=0 => 1093 Type-0 normals, with Q1>=131, Q2>=598.
    n1=272*S2-S3-4792275*N
    n2=4064*S2-15*S3-71449749*N
    assert (n1,n2)==(153900,702828)
    for rank,last in [(0,1)]+[(r,t) for r in range(1,8) for t in (1,2)]:
        n0,nq1,nq2=spectrum_dp(7,rank,last)
        assert 1176*nq1<n1 or 1176*nq2<n2
    # b !=0 => 729 Type-1, 364 Type-0; Q0<=81.
    n0_upper=S3-271*S2+4765200*N-28*729
    assert n0_upper==6378
    survivors=[]
    for rank,last in [(0,1)]+[(r,t) for r in range(1,7) for t in (1,2)]:
        vals=spectrum_dp(6,rank,last)
        if 78*vals[0]<=n0_upper:survivors.append((rank,last,vals))
    assert survivors==[(2,1,(40,162,162))]
    return dict(profiles=len(ps),moments=[N,S2,S3],
                zero_barycenter_quadratic_cases_excluded=15,
                nonzero_barycenter_cases_examined=13,
                only_surviving_class=survivors[0],
                exact_numerators={'1176*N_Q1_lower':n1,
                                  '1176*N_Q2_lower':n2,
                                  '78*N_Q0_upper':n0_upper})

def formal_negative_control():
    # Formal integer histogram: NOT an actual cap or direction assignment.
    assert set(FORMAL)<=set(profiles()) and sum(FORMAL.values())==N
    assert sum(n*powers(t)[0] for t,n in FORMAL.items())==S2
    assert sum(n*powers(t)[1] for t,n in FORMAL.items())==S3
    c=Counter()
    for t,n in FORMAL.items():c[category(t)]+=n
    assert c==Counter({'Q0':40,'Q1':162,'Q2':162,'T':729})
    return c

def verify_known_236():
    # Independent construction from two 10-block designs and 12 axes.
    def shift(t,k):
        return tuple(sorted(0 if x==0 else (x-1+k)%5+1 for x in t))
    b0={shift(t,k) for t in ((0,1,2),(1,2,4)) for k in range(5)}
    b1=set(combinations(range(6),3))-b0
    shell={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
    def make(blocks):
        pts=set(shell)
        for block in blocks:
            for signs in product((1,2),repeat=3):
                v=[0]*6
                for i,x in zip(block,signs):v[i]=x
                pts.add(tuple(v))
        assert len(pts)==112
        return pts
    e={tuple(v if j==i else 0 for j in range(6)) for i in range(6) for v in (1,2)}
    pts={(0,)+v for v in make(b0)}|{(1,)+v for v in make(b1)}|{(2,)+v for v in e}
    assert len(pts)==236
    for x,y in combinations(sorted(pts),2):
        assert tuple((-a-b)%3 for a,b in zip(x,y)) not in pts
    saved=Path(__file__).resolve().parent/'candidates/calderbank_fishburn_236.txt'
    if saved.exists():
        ls=saved.read_text().splitlines()
        assert ls[0].strip()=='n: 7'
        assert {tuple(int(x) for x in s.strip()) for s in ls[1:] if s.strip()}==pts
    return len(pts)

class TestCAP026(unittest.TestCase):
    def test_169_profiles_and_integer_duals(self):
        self.assertEqual(certificate()['profiles'],169)
    def test_all_28_quadric_spectra_independent_brute(self):
        for k in (6,7):
            for rank,last in [(0,1)]+[(r,t) for r in range(1,k+1) for t in (1,2)]:
                with self.subTest(k=k,rank=rank,last=last):
                    self.assertEqual(spectrum_dp(k,rank,last),
                                     spectrum_brute(k,rank,last))
    def test_exact_formal_negative_control(self):
        self.assertEqual(formal_negative_control()['Q0'],40)
    def test_independent_known_236_witness(self):
        self.assertEqual(verify_known_236(),236)

if __name__=='__main__':
    print(certificate())
    print('formal non-geometric histogram',dict(formal_negative_control()))
    unittest.main(verbosity=2)
