"""CAP041 root-equivalent dense-H SAT presolve and witness-mapping regression."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from cap041_root_presolve import configure,audit
from cap040_root_orbits import pack,frame,third
from itertools import combinations

class CAP041RootPresolveTest(unittest.TestCase):
    def test_fixed_units_and_global_remnant(self):
        case,one,zero,free,label,H=configure(0)
        self.assertEqual((len(one),len(zero),len(free),len(H)),(9,36,2142,693))
        self.assertFalse(one&zero)
        self.assertEqual(one|zero|set(free),set(range(1,2188)))
        self.assertEqual(len(label),len(free))
        self.assertTrue(all(i%3==1 for i in (free[j-1] for j in H)))

    def test_exceptional_branch_zero_secant_overlap(self):
        case,one,zero,free,label,H=configure(9)
        self.assertEqual((len(one),len(zero),len(free),len(H)),(9,35,2143,694))

    def test_complete_reduced_dimacs_sha256(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cap041_B0.cnf'
            result=audit(0,str(p))
            self.assertEqual((result['variables'],result['clauses']),(517533,1786028))
            self.assertEqual(result['line_counts'],
                             {'dropped':38718,'binary':9513,'ternary':748566})
            self.assertEqual((result['allpoint_counter_aux'],result['H_counter_aux']),
                             (462498,52893))
            with p.open('rb') as f:
                self.assertIn(b'p cnf 517533 1786028',f.readline()+f.readline())
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                             'b59faca48cdd649e1574c06f36dd1ff2dab982cdac05b22b8d306e0f76b276c4')
            m=json.loads(Path(str(p)+'.mapping.json').read_text())
            self.assertEqual(len(m['free_id_to_point_code']),2142)
            self.assertEqual(len(m['selected_point_codes_sorted']),9)
            self.assertTrue(set(m['selected_point_codes_sorted']).isdisjoint(m['free_id_to_point_code']))
            self.assertTrue(all(0<=x<2187 for x in m['free_id_to_point_code']))
if __name__=='__main__':unittest.main()
