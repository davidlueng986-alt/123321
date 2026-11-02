import unittest
from pathlib import Path
from cap007j_hyperplane_moment_gate import (
    coefficients, predicted_moments, affine_normal_representatives,
    is_cap, measured_moments, gate_237)

class HyperplaneMomentGate(unittest.TestCase):
    def test_exact_237_contradiction_and_75_profiles(self):
        r=gate_237()
        self.assertEqual(r['required_exact_value'],-35076)
        self.assertEqual(r['sorted_profiles_checked'],75)
    def test_normal_counts_and_9_cap_direct_moments(self):
        # Anisotropic quadratic graph in F3^3; 9 points, no 3-collinear.
        cap=[(x,y,(x*x+y*y)%3) for x in range(3) for y in range(3)]
        self.assertTrue(is_cap(cap))
        self.assertEqual(coefficients(3),(13,4,1))
        self.assertEqual(len(list(affine_normal_representatives(3))),13)
        self.assertEqual(measured_moments(cap,3)[:2],predicted_moments(3,9))
    def test_known_236_regression_direct_moments(self):
        f=Path(__file__).resolve().parent / "candidates" / "calderbank_fishburn_236.txt"
        if not f.exists():
            self.skipTest("Repository fixture unavailable in local scratch workspace")
        pts=[tuple(map(int,line.strip())) for line in f.read_text().splitlines() if line.strip()]
        self.assertEqual(len(pts),236)
        self.assertTrue(is_cap(pts))
        self.assertEqual(measured_moments(pts,7),(20445388,1631114708,112))
        self.assertEqual(predicted_moments(7,236),(20445388,1631114708))
    def test_reject_collinear_triple(self):
        self.assertFalse(is_cap([(0,0),(1,0),(2,0)]))

if __name__=='__main__':
    unittest.main()
