#!/usr/bin/env python3
"""CAP-027: exact affine Radon p-rank and count-only 285 negative control.
Pure stdlib, deterministic; NOT a cap witness. No solver or GPU.
"""
from itertools import product
from collections import Counter
import unittest, subprocess, shutil, json
from pathlib import Path
P=tuple(product(range(3),repeat=4))
P2=tuple(product(range(3),repeat=2))
N=tuple(u for u in P if any(u) and next(v for v in u if v)==1)
assert len(P)==81 and len(N)==40
def dot(u,x):return sum(a*b for a,b in zip(u,x))%3
def rank(A):
    a=[list(x) for x in A];r=0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        if a[r][j]==2:a[r]=[(2*x)%3 for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                c=a[i][j];a[i]=[(x-c*y)%3 for x,y in zip(a[i],a[r])]
        r+=1
    return r
def radon(k):
    pts=tuple(product(range(3),repeat=k))
    normals=[u for u in pts if any(u) and next(z for z in u if z)==1]
    return [[int(dot(u,x)==s) for x in pts] for u in normals for s in range(3)]
def polynomial_rows(k):
    pts=tuple(product(range(3),repeat=k))
    exps=[(0,)*k]
    for i in range(k):
        e=[0]*k;e[i]=1;exps.append(tuple(e))
    for i in range(k):
        for j in range(i,k):
            e=[0]*k;e[i]+=1;e[j]+=1;exps.append(tuple(e))
    return [[__import__('math').prod(x[i]**e[i] for i in range(k))%3 for x in pts] for e in exps]
def normal_planes():
    seen={}
    for u in N:
        for v in N:
            space=frozenset(tuple((a*x+b*y)%3 for x,y in zip(u,v)) for a,b in P2)
            if len(space)==9 and space not in seen:seen[space]=(u,v)
    return tuple(seen.values())
def fibers():
    chosen={P[(7*i)%81] for i in range(11)}
    return {x:3+int(x[0]==0 and x[1]==0)+3*int(x in chosen) for x in P}
def grid(f,u,v):
    return {(i,j):sum(f[x] for x in P if dot(u,x)==i and dot(v,x)==j) for i,j in P2}
def affine_grid(g):
    a=g[0,0]%3;b=(g[1,0]-g[0,0])%3;c=(g[0,1]-g[0,0])%3
    return all(g[i,j]%3==(a+b*i+c*j)%3 for i,j in P2)
def certificate():
    assert tuple(rank(radon(k)) for k in (2,3,4))==(6,10,15)
    pol=polynomial_rows(4)
    assert len(pol)==rank(pol)==rank(pol+radon(4))==15
    planes=normal_planes();assert len(planes)==130
    f=fibers();assert len(f)==81 and sum(f.values())==285 and max(f.values())==7
    slices=[sum(f[x] for x in P if dot(u,x)==s) for u in N for s in range(3)]
    assert len(slices)==120 and all(v%3==0 and v<=109 for v in slices)
    grids=[grid(f,u,v) for u,v in planes]
    cells=[g[i,j] for g in grids for i,j in P2]
    assert len(cells)==1170 and max(cells)<=45 and all(affine_grid(g) for g in grids)
    assert any(v%3 for v in f.values())
    return dict(ranks=[6,10,15],fibers=81,total=285,
                fiber_histogram=dict(sorted(Counter(f.values()).items())),
                normal_planes=130,affine_6d_sections=120,
                six_dim_range=[min(slices),max(slices)],
                affine_5d_sections=1170,five_dim_range=[min(cells),max(cells)],
                all_130_grids_affine_mod3=True,cap_witness=False)
class TestCAP027(unittest.TestCase):
    def test_radon_ranks(self):
        self.assertEqual([rank(radon(k)) for k in (2,3,4)],[6,10,15])
    def test_polynomial_span(self):
        pol=polynomial_rows(4);self.assertEqual(rank(pol),15)
        self.assertEqual(rank(pol+radon(4)),15)
    def test_normal_planes(self):self.assertEqual(len(normal_planes()),130)
    def test_fiber_relaxation(self):
        c=certificate()
        self.assertEqual(c['six_dim_range'],[84,108])
        self.assertEqual(c['five_dim_range'],[27,45])
    def test_grid_kernel(self):
        for a,b,c in product(range(3),repeat=3):
            g={(i,j):(a+b*i+c*j)%3 for i,j in P2}
            self.assertTrue(affine_grid(g))
            for u in (v for v in P2 if any(v) and next(z for z in v if z)==1):
                for s in range(3):
                    self.assertEqual(sum(g[i,j] for i,j in P2 if dot(u,(i,j))==s)%3,0)
        self.assertEqual(rank(radon(2)),6)
    def test_independent_js(self):
        if not shutil.which('node'):self.skipTest('node unavailable')
        path=Path(__file__).with_name('cap027_radon_independent.js')
        data=json.loads(subprocess.check_output(['node',str(path)],text=True,timeout=20))
        self.assertEqual((data['radon_rank'],data['planes'],data['grids'],data['max5'],data['max6']),
                         (15,130,1170,45,108))
if __name__=='__main__':
    print('CAP027',certificate())
    unittest.main(verbosity=2)
