"""CAP050 rigorous finite certificate regression, independently compiled C++17."""
import json,subprocess,tempfile,unittest
from pathlib import Path
from cap050_global290_integer_certificate import main
HERE=Path(__file__).resolve().parent
class CAP050ExactGlobal(unittest.TestCase):
 def test_independently_integer_certify_candidate290(self):
  x=main()
  self.assertEqual(x['directions']['at_least_112_slice_directions'],69)
  self.assertEqual(x['center_cost']['coplanar4_stronger_global_lower'],451776)
  self.assertEqual(x['fourth_dual']['P_upper_floor'],451523)
  self.assertEqual(x['exact_P_contradiction'],'307268/1215')
  self.assertEqual(x['root_exact_status'],'OPEN')
 def test_cpp_exact_certificate_and_scope(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'cap050'
   subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',
                   str(HERE/'cap050_global290_independent.cpp'),'-o',str(path)],check=True)
   out=subprocess.check_output([str(path)],text=True,timeout=8)
  self.assertIn('CAP050_CERT_PASS',out)
  self.assertIn('exact_contradiction_over1215=307268',out)
  self.assertIn('global_bound_candidate=290',out)
if __name__=='__main__':unittest.main()
