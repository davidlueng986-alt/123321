"""E022 regression tests: fixed Egan A, not unrestricted 3-MOLS(10)."""
import unittest
from E022_replay import prepare,cover

class TestE022(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.T,cls.cells,cls.disjoint=prepare()
 def test_transversals(self):
  self.assertEqual(len(self.T),1080)
 def test_sat_pair(self):
  s,n,w=cover(self.T,self.cells,self.disjoint,(69,632),20000)
  self.assertEqual(s,'SAT')
  self.assertEqual(len(w),10)
  self.assertEqual(sum(self.T[i] for i in w),(1<<100)-1)
 def test_unsat_pair(self):
  s,n,w=cover(self.T,self.cells,self.disjoint,(30,714),20000)
  self.assertEqual(s,'UNSAT_EXHAUSTIVE')
  self.assertEqual(w,[])
 def test_unknown_not_unsat(self):
  s,n,w=cover(self.T,self.cells,self.disjoint,(30,714),0)
  self.assertEqual(s,'UNKNOWN_BUDGET')

if __name__=='__main__':unittest.main()
