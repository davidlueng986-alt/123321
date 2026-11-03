"""CAP047 rigorous negative theorem and adversarial falsification regression."""
import unittest
from cap047_spectral_112 import verify_sample,counterexample_to_naive_C_subset

class Spectral112Audit(unittest.TestCase):
    def test_sample_convolution_and_exact_correlations(self):
        r=verify_sample(trials=12,seed=2026110405)
        self.assertTrue(r['all_729_correlations_exact'])
        self.assertEqual(r['fingerprint']['fourier'],
                         {'zero':112,'inside_S':-23,'outside_S_nonzero':4})
        self.assertFalse(r['claim_all_112_112_holes_at_most_12_proven'])
    def test_explicit_false_32cap_shortcut(self):
        c=counterexample_to_naive_C_subset()
        self.assertEqual(len(c['C_32_points_as_16_antipodal_representatives']),16)
        self.assertEqual(c['avoiding_normal_count'],14)
        self.assertFalse(14<=12)

if __name__=="__main__":unittest.main()
