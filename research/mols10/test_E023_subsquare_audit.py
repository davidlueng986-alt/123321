"""E023 regression tests: independent local 4x4 subsquare-compatibility scope only."""
import unittest
from E023_subsquare_audit import audit, OMEGA, compatible

class TestE023(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=audit()
    def test_complete_row_parity(self):
        self.assertEqual(self.r['counts']['Z4']['4']['compatible_partial_rows'],0)
        self.assertEqual(self.r['counts']['V4']['4']['compatible_partial_rows'],8)
    def test_unique_virtual_completion(self):
        self.assertEqual(self.r['counts']['V4']['extension_multiplicities']['2'],{1:48})
        self.assertEqual(self.r['counts']['V4']['extension_multiplicities']['3'],{1:32})
    def test_myrvold_vx_only_local(self):
        self.assertFalse(self.r['residual_type_necessary_local_feasibility']['VX']['Z4_compatible'])
        self.assertTrue(self.r['residual_type_necessary_local_feasibility']['VX']['V4_compatible'])
        self.assertTrue(compatible(OMEGA['V4'],range(4),[0,2,3,1]))
        self.assertFalse(compatible(OMEGA['Z4'],range(4),[0,2,3,1]))
if __name__=='__main__':
    unittest.main()
