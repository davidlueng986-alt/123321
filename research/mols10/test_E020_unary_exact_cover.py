#!/usr/bin/env python3
"""E020 stdlib regression: independent n! transversal enumeration and full audit."""
import itertools
import unittest
from E020_unary_exact_cover import PARKER_A, transversals, prepare, audit

SURVIVORS=[26,29,50,55,165,167,195,202,380,395,438,453,512,531,
 547,563,577,643,663,727,844,850,853,915,924,950,963,1060]
UNCOVERED=[2,13,24,35,46,50,61,77,78,79,88,97,98]

class TestE020(unittest.TestCase):
 def test_parker_full_exact_unary_audit(self):
  a=PARKER_A
  # Different enumeration mechanism: all 10! permutations, not DFS.
  independent=[]
  for p in itertools.permutations(range(10)):
   if len({a[r][p[r]] for r in range(10)})==10:
    independent.append(sum(1<<(10*r+p[r]) for r in range(10)))
  self.assertEqual(independent,transversals(a))
  self.assertEqual(len(independent),1104)
  r=audit(a,seconds=2,max_nodes=100000)
  self.assertEqual(r['roots_tested'],1104)
  self.assertEqual(r['status_counts'],{'SAT':28,'UNSAT_EXHAUSTIVE':1076,'UNKNOWN_BUDGET':0})
  self.assertEqual(r['surviving_roots'],SURVIVORS)
  self.assertEqual(r['uncovered_cells'],UNCOVERED)
  self.assertEqual(r['input_sha256'],'1694eda37452b6709d8f8d77d8dfcddae08e18c6a94e4aabc102bec6323c1c77')
 def test_gf4_positive_control(self):
  a=[[i^j for j in range(4)] for i in range(4)]
  r=audit(a,seconds=2)
  self.assertEqual(r['transversals'],8)
  self.assertEqual(r['status_counts'],{'SAT':8,'UNSAT_EXHAUSTIVE':0,'UNKNOWN_BUDGET':0})
  self.assertEqual(r['uncovered_cells'],[])
if __name__=='__main__':unittest.main()
