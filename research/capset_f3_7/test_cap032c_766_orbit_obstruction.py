"""CAP-032C independent exact orbit-type and 19-cap regression."""
import unittest
from cap032c_766_orbit_obstruction import audit
class Cap032CProofTest(unittest.TestCase):
    def test_766_orbit_force_and_two_9_extensions(self):
        r=audit()
        a,b=r['first_7cap_types']
        self.assertEqual([a['orbit_size'],b['orbit_size']],[50544,75816])
        self.assertEqual([a['second_6caps_with_feasible_6cap_third'],b['second_6caps_with_feasible_6cap_third']],[27,0])
        self.assertEqual([a['feasible_second_third_pairs'],b['feasible_second_third_pairs']],[27,0])
        self.assertEqual([a['nine_cap_completions'],b['nine_cap_completions']],[0,1])
        self.assertTrue(r['sharp_7_6_6_19cap_verified'])
        self.assertTrue(r['universal_if_7_6_6_then_7cap_not_extendable_to9'])
if __name__=='__main__':unittest.main()
