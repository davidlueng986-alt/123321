"""E017 replay tests: independent transversal enumeration and new fixed-A exclusions."""
import unittest
from E017_replay import audit, cases, latin, transversals

class TestE017(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.E, cls.P, cls.et, cls.pt, cls.pairs = cases()

    def test_inputs_and_variant_generation(self):
        self.assertTrue(latin(self.E))
        self.assertTrue(latin(self.P))
        self.assertEqual((len(self.et), len(self.pt), len(self.pairs)), (48, 66, 774))
        self.assertEqual((len(transversals(self.E)), len(transversals(self.P))), (1080, 1104))

    def test_order4_positive_control(self):
        a=[[i^j for j in range(4)] for i in range(4)]
        r=audit(a,max_seconds=5)
        self.assertEqual(r['status'],'SAT_SUPPORT_ONLY')

    def test_original_egan_independent_replay(self):
        r=audit(self.E,max_seconds=30)
        self.assertEqual((r['status'],r['nodes'],r['pruned_support']),
                         ('UNSAT_FIXED_A_EXHAUSTIVE',24875,18407))

    def test_original_parker_new_exclusion(self):
        r=audit(self.P,max_seconds=30)
        self.assertEqual((r['status'],r['nodes'],r['pruned_support']),
                         ('UNSAT_FIXED_A_EXHAUSTIVE',49199,37286))

    def test_parker_trade65_new_exclusion(self):
        r=audit(self.pt[65]['square'],max_seconds=30)
        self.assertEqual((r['status'],r['transversals'],r['nodes'],r['pruned_support']),
                         ('UNSAT_FIXED_A_EXHAUSTIVE',1272,186150,140325))

if __name__=='__main__':unittest.main()
