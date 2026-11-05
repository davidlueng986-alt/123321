"""CAP049 root proof: exact 184-profile global <=291 dual (known bound).
Independent stdlib vs C++17 integers; no floating point or optimizer for proof.
"""
import subprocess,tempfile,unittest
from pathlib import Path
from cap049_global_fourth_moment_certificate import prove_no_292,check_291_gap
HERE=Path(__file__).resolve().parent
class CAP049GlobalTest(unittest.TestCase):
 def test_exact_global_292_excluded(self):
  a=prove_no_292()
  self.assertEqual(a['profiles'],184)
  self.assertEqual(a['contradiction_times_45'],48384)
  self.assertEqual(a['global_bound'],'r3(7)<=291 (already known)')
 def test_exact_291_gap_quantified(self):
  a=check_291_gap()
  self.assertEqual(a['P_min'],448602)
  self.assertEqual(a['P_min_needed'],451524)
  self.assertEqual(a['additional_coplanar_quadruples_needed'],2922)
 def test_independent_cpp_184_case_dual(self):
  with tempfile.TemporaryDirectory() as d:
   exe=str(Path(d)/'cap049dual')
   subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',
                  str(HERE/'cap049_independent_fourth_dual.cpp'),'-o',exe],check=True)
   s=subprocess.check_output([exe],text=True,timeout=5)
  self.assertIn('CAP049_GLOBAL_CERT_PASS',s)
  self.assertIn('integer_contradiction_times45=48384',s)
if __name__=='__main__':unittest.main()
