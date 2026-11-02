#!/usr/bin/env python3
"""CAP-024 exact, deterministic anchored-111 graph/cut certificate (stdlib only)."""
from collections import Counter
from itertools import product,combinations
from math import comb
import unittest
B=((0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),
   (1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5))
def add(x,y):return tuple((a+b)%3 for a,b in zip(x,y))
def sub(x,y):return tuple((a-b)%3 for a,b in zip(x,y))
def neg(x):return tuple(-a%3 for a in x)
def H112():
 h={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
 for b in B:
  for signs in product((1,2),repeat=3):
   v=[0]*6
   for i,s in zip(b,signs):v[i]=s
   h.add(tuple(v))
 assert len(h)==112 and h=={neg(v) for v in h}
 return h
def census():
 h=H112();p=min(h);a=h-{p};hist112=Counter();hist111=Counter();k={}
 for t in product(range(3),repeat=6):
  if not any(t):continue
  old=sum(add(v,t) in h for v in h)
  new=sum(add(v,t) in a for v in a)
  lost=int(add(p,t) in h)+int(sub(p,t) in h)
  assert lost<=1 and old-new==lost
  hist112[old]+=1;hist111[new]+=1;k[t]=new
 return h,p,a,hist112,hist111,k
def cycles(hist):
 s=sum(n*comb(k,2) for k,n in hist.items());assert s%2==0
 return 729*s//2
def deficit_limit(b,c):
 assert 0<=b<=729 and 0<=c<729
 d=111*b;required=(d*d+729-c-1)//(729-c)
 return (d+40*comb(b,2)-required)//2
def forbidden(a,x):return {neg(add(p,x)) for p in a}
class CAP024(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.h,cls.p,cls.a,cls.old,cls.new,cls.k=census()
 def test_cap_and_hist(self):
  for x,y in combinations(self.h,2):self.assertNotIn(neg(add(x,y)),self.h)
  self.assertEqual(self.old,Counter({1:112,20:616}))
  self.assertEqual(self.new,Counter({0:2,1:110,19:220,20:396}))
 def test_direct_neighborhood_intersections_all_differences(self):
  base=forbidden(self.a,(0,)*6)
  for t,k in self.k.items():self.assertEqual(len(base&forbidden(self.a,t)),k)
 def test_four_cycles(self):
  self.assertEqual(cycles(self.old),42661080)
  self.assertEqual(cycles(self.new),41137470)
 def test_cauchy_287_necessary_cuts(self):
  self.assertEqual(deficit_limit(88,88),7018)
  self.assertEqual(deficit_limit(88,88)//19,369)
  self.assertEqual([deficit_limit(b,176-b)//19 for b in (64,70,80,88,96,104,112)],
                   [156,196,281,369,476,603,754])
 def test_known235_crossfree_control(self):
  from itertools import product
  complement=set(combinations(range(6),3))-set(B)
  h1={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
  for b in complement:
   for signs in product((1,2),repeat=3):
    v=[0]*6
    for i,s in zip(b,signs):v[i]=s
    h1.add(tuple(v))
  axes={tuple(s if j==i else 0 for j in range(6)) for i in range(6) for s in (1,2)}
  self.assertEqual((len(h1),len(axes)),(112,12))
  self.assertTrue(all(not(forbidden(self.a,x)&axes) for x in h1))
  deficit=sum(20-self.k[sub(x,y)] for x,y in combinations(sorted(h1),2))
  self.assertLessEqual(deficit,deficit_limit(112,12))
  self.assertEqual(deficit,17420)
if __name__=='__main__':unittest.main(verbosity=2)
