import unittest
from cap005_k6_secant_matching_gate import census

class TestSixFiberGate(unittest.TestCase):
    def test_exact_census(self):
        r=census()
        self.assertEqual(r['release_sets'],296010)
        self.assertEqual(r['excluded_by_ten_deletion_gate'],288878)
        self.assertEqual(r['unresolved'],7132)
        self.assertEqual(r['max_admissible_outsiders'],92)
        self.assertEqual(len(r['max_groups']),16)
        self.assertEqual(r['histograms']['6']['92'],16)
        self.assertEqual(r['at_least_20_outsiders'],1072)

if __name__=='__main__': unittest.main()
