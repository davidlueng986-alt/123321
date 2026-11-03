"""CAP-032B independent Python and C++17 finite theorem regression tests."""
import csv,io,subprocess,tempfile,unittest
from pathlib import Path
from cap032b_universal_fiber_77 import audit
from cap032b_4d_threshold_cuts import audit as cuts
HERE=Path(__file__).resolve().parent
class CAP032BTests(unittest.TestCase):
    def test_exact_independent_python_7_7(self):
        r=audit()
        self.assertEqual(r['n7caps'],126360)
        self.assertEqual(sorted(r['affine_orbit_sizes']),[50544,75816])
        self.assertEqual(r['pairs_checked'],252720)
        self.assertEqual(r['exceptional_holes_ge5'],189)
        self.assertEqual(r['feasible_5caps'],0)
        self.assertEqual(r['third_slice_exact_max_given_7_7'],4)
        self.assertTrue(r['sharp_18point_witness'])
    def test_complete_independent_cpp_6_through_9(self):
        with tempfile.TemporaryDirectory() as d:
            exe=str(Path(d)/'profile')
            subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra','-pedantic',
                            str(HERE/'cap032b_universal_high_fiber.cpp'),'-o',exe],check=True)
            data=subprocess.check_output([exe],text=True,timeout=30)
        rows=list(csv.DictReader(io.StringIO(data)))
        expected={(6,6):(8,9,322218),(6,7):(6,7,379080),
                  (6,8):(6,7,189540),(6,9):(3,4,6318),
                  (7,7):(4,6,252720),(7,8):(3,4,126360),
                  (7,9):(2,2,4212),(8,8):(2,3,189540),
                  (8,9):(2,2,6318),(9,9):(2,2,2106)}
        self.assertEqual(len(rows),10)
        for row in rows:
            key=int(row['a']),int(row['b'])
            self.assertEqual((int(row['max_third']),int(row['max_holes']),int(row['pairs'])),expected[key])
    def test_redundant_global_threshold_cuts_and_negative_control(self):
        r=cuts()
        self.assertEqual(r['quotient_lines'],1080)
        self.assertTrue(r['formal285_still_feasible_count_model'])
        self.assertTrue(r['invalid_7_7_5_detected'])
if __name__=='__main__':unittest.main()
