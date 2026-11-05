"""CAP052 exact normal-form finite geometry tests. Never treat as SAT/UNSAT."""
import unittest
from cap052_root_center_normal_forms import verify,pg2_arc_max4_check
class CAP052RootTests(unittest.TestCase):
    def test_all_finite_geometric_prerequisites(self):
        self.assertTrue(pg2_arc_max4_check())
        r=verify()
        self.assertEqual(r['status'],'ONLY_NORMAL_FORM_PROOFS_NOT_ROOT_CLOSURE')
        self.assertEqual(r['dense_89_secant_center_min_pairs'],7)
        self.assertEqual(r['global_237_secant_center_min_pairs'],15)
    def test_11_anchor_dense_root(self):
        x=verify()['dense_single_case']
        self.assertEqual((x['mandatory_selected'],x['forced_zero'],x['free_points']),(11,52,2124))
        self.assertEqual((x['selected_H'],x['forced_zero_H'],x['free_H']),(10,42,677))
    def test_12_anchor_global_root(self):
        x=verify()['global_single_case']
        self.assertEqual((x['mandatory_selected'],x['forced_zero'],x['free_points']),(12,62,2113))
if __name__=='__main__':unittest.main()
