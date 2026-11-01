import copy
import json
import unittest
from pathlib import Path
from signed_dual import replay, validate_signed

ROOT=Path(__file__).parent

class TestSignedDual(unittest.TestCase):
    def test_E009_parker_upper_77(self):
        r=replay(ROOT/"E009_PARKER_WEIGHTED77.json")
        self.assertTrue(r["verified"])
        self.assertEqual(r["global_integer_upper_bound_for_fixed_pair"],77)
        self.assertEqual(r["A_transversals_checked"],1104)
        self.assertEqual(r["weight_sum_numerators"],45)
        self.assertEqual(r["tight_transversals"],267)
        self.assertNotIn("optimality_proven",r)

    def test_E010_Egan_AB_optimum_91(self):
        r=replay(ROOT/"E010_EGAN_AB_WEIGHTED91.json")
        self.assertTrue(r["verified"])
        self.assertEqual(r["global_integer_upper_bound_for_fixed_pair"],91)
        self.assertEqual(r["attaining_score"],91)
        self.assertTrue(r["optimality_proven"])
        self.assertEqual(r["tight_transversals"],61)

    def test_E009_reject_perturbed_weights(self):
        data=json.loads((ROOT/"parker_pair.json").read_text())["squares"]
        cert=json.loads((ROOT/"E009_PARKER_WEIGHTED77.json").read_text())
        cert["weight_numerators"][0][0] += 1000
        cert["asserted_weight_sum"] += 1000
        with self.assertRaisesRegex(AssertionError, "violating"):
            validate_signed(data[0],data[1],cert)

    def test_E010_reject_fake_optimality(self):
        cert=json.loads((ROOT/"E010_EGAN_AB_WEIGHTED91.json").read_text())
        cert["attaining_overlay"]=92
        data=json.loads((ROOT/"near_triple.json").read_text())["squares"]
        with self.assertRaises(AssertionError):
            validate_signed(data[0],data[1],cert)

if __name__=="__main__":
    unittest.main()
