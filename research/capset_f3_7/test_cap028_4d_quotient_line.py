#!/usr/bin/env python3
"""CAP-028: independently check local 4D quotient-line lifts; stdlib only."""
from itertools import product,combinations
from collections import Counter
import unittest,json,subprocess,shutil
from pathlib import Path
P=tuple(product(range(3),repeat=4))
N=tuple(u for u in P if any(u) and next(z for z in u if z)==1)
W774=[[0,0,1,0],[0,0,1,2],[0,0,2,1],[0,1,0,1],[0,2,0,2],[0,2,1,2],[0,2,2,1],[1,0,1,0],[1,0,1,1],[1,0,2,2],[1,2,1,0],[1,2,1,2],[1,2,2,1],[1,2,2,2],[2,0,0,0],[2,0,2,1],[2,1,2,2],[2,2,0,1]]
W766=[[0,0,0,1],[0,0,2,2],[0,1,0,1],[0,1,2,0],[0,1,2,1],[0,2,0,0],[0,2,2,2],[1,1,1,0],[1,1,1,2],[1,2,0,2],[1,2,1,0],[1,2,1,2],[2,1,1,0],[2,1,1,1],[2,2,0,0],[2,2,1,0],[2,2,1,1],[1,1,2,0],[2,1,2,1]]
def check(points,n):
 p=[tuple(x) for x in points];s=set(p)
 assert len(s)==len(p) and all(len(x)==n and set(x)<={0,1,2} for x in p)
 for a,b in combinations(p,2):assert tuple((-x-y)%3 for x,y in zip(a,b)) not in s
 return len(p)
def fibers():
 chosen={P[7*i%81] for i in range(11)}
 return {t:3+int(t[0]==t[1]==0)+3*int(t in chosen) for t in P}
def lines():
 out=set()
 for u in N:
  for x in P:out.add(frozenset(tuple((x[i]+k*u[i])%3 for i in range(4)) for k in range(3)))
 assert len(out)==1080
 return tuple(out)
def profiles():
 f=fibers()
 return Counter(tuple(sorted((f[x] for x in line),reverse=True)) for line in lines())
def lift(p):
 a,b,c=sorted(p,reverse=True)
 if a<=7 and b<=6 and c<=6:source=W766
 else:
  assert a<=7 and b<=7 and c<=4
  source=W774
 quota=[a,b,c];selected=[]
 for x in source:
  if quota[x[0]]:selected.append(x);quota[x[0]]-=1
 assert quota==[0,0,0] and check(selected,4)==a+b+c
 return selected
def certificate():
 f=fibers();h=profiles();ls=lines()
 assert len(f)==81 and sum(f.values())==285 and len(h)==12
 assert check(W774,4)==18 and check(W766,4)==19
 for p in h:lift(p)
 assert sum(h.values())==1080 and max(map(sum,h))==19
 m1=sum(sum(f[x] for x in line) for line in ls)
 m2=sum((sum(f[x] for x in line))*(sum(f[x] for x in line)-1)//2 for line in ls)
 same=sum(v*(v-1)//2 for v in f.values())
 assert m1==11400==40*285
 assert same==408 and m2==56382==285*284//2+39*same
 return dict(profiles={str(k):v for k,v in sorted(h.items())},lines=1080,max_total=19,m1=m1,m2=m2,locally_liftable=len(h),global_285_cap=False)
def known236():
 def shift(t,k):return tuple(sorted(0 if x==0 else (x-1+k)%5+1 for x in t))
 b0={shift(t,k) for t in ((0,1,2),(1,2,4)) for k in range(5)}
 b1=set(combinations(range(6),3))-b0
 shell={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
 def make(blocks):
  out=set(shell)
  for block in blocks:
   for signs in product((1,2),repeat=3):
    v=[0]*6
    for i,x in zip(block,signs):v[i]=x
    out.add(tuple(v))
  assert len(out)==112
  return out
 axes={tuple(v if j==i else 0 for j in range(6)) for i in range(6) for v in (1,2)}
 pts={(0,)+v for v in make(b0)}|{(1,)+v for v in make(b1)}|{(2,)+v for v in axes}
 return check(pts,7)
class TestCAP028(unittest.TestCase):
 def test_recovered_19_cap_extension_census(self):
  seed=W766[:-2]
  self.assertEqual([sum(x[0]==k for x in seed) for k in range(3)],[7,5,5])
  self.assertEqual(check(seed,4),17)
  def admissible(points):
   try:
    return check(points,4)==len(points)
   except AssertionError:
    return False
  possible=[x for x in P if tuple(x) not in set(map(tuple,seed)) and admissible(seed+[x])]
  pairs=[(a,b) for a,b in combinations(possible,2) if admissible(seed+[a,b])]
  self.assertEqual(len(possible),5)
  self.assertEqual(len(pairs),3)
  balanced=[(a,b) for a,b in pairs if [sum(x[0]==k for x in seed+[a,b]) for k in range(3)]==[7,6,6]]
  self.assertEqual(balanced,[((1,1,2,0),(2,1,2,1))])
  self.assertEqual(check(W766,4),19)
 def test_local_witnesses(self):
  self.assertEqual(check(W774,4),18);self.assertEqual(check(W766,4),19)
 def test_line_counts(self):
  self.assertEqual(len(lines()),1080);self.assertEqual(max(map(sum,profiles())),19)
 def test_all_profiles_lift(self):self.assertEqual(certificate()['locally_liftable'],12)
 def test_moments(self):
  self.assertEqual(certificate()['m1'],11400);self.assertEqual(certificate()['m2'],56382)
 def test_known236(self):self.assertEqual(known236(),236)
 def test_independent_node(self):
  if not shutil.which('node'):self.skipTest('node unavailable')
  data=json.loads(subprocess.check_output(['node',str(Path(__file__).with_name('cap028_4d_line_independent.js'))],text=True,timeout=15))
  self.assertEqual((data['witnesses'],data['lines'],data['profiles'],data['max'],data['m1'],data['m2']),([18,19],1080,12,19,11400,56382))
if __name__=='__main__':
 print(json.dumps(certificate(),sort_keys=True));unittest.main(verbosity=2)
