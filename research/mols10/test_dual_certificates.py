import copy
import json
import unittest
from pathlib import Path
from dual_certificates import is_latin, pair_count, replay, validate

ROOT = Path(__file__).parent

class TestExactDualCertificates(unittest.TestCase):
    def test_E008_conditional_optimality_91(self):
        result = replay(ROOT / "E008_DUAL_CERTIFICATE.json", independent=True)
        self.assertEqual(result["transversal_count"],1080)
        self.assertEqual(result["permutations_checked_independently"],3628800)
        self.assertEqual(result["upper_bound"],91)
        self.assertEqual(result["attaining_score"],91)
        self.assertTrue(result["attained"])
        self.assertEqual(result["tight_transversals"],30)

    def test_E009_parker_conditional_upper_bound_78(self):
        result = replay(ROOT / "E009_PARKER_DUAL_CERTIFICATE.json", independent=True)
        self.assertEqual(result["transversal_count"],1104)
        self.assertEqual(result["permutations_checked_independently"],3628800)
        self.assertEqual(result["upper_bound"],78)
        self.assertFalse(result["attained"])
        self.assertEqual(result["tight_transversals"],266)

    def test_reject_tampered_egan_certificate(self):
        base = json.loads((ROOT / "near_triple.json").read_text())["squares"]
        cert = json.loads((ROOT / "E008_DUAL_CERTIFICATE.json").read_text())
        cert["removed_cells_zero_based"].append([0,0])
        with self.assertRaisesRegex(AssertionError, "dual certificate fails"):
            validate(base[0],base[2],cert,base[1])

    def test_reject_duplicate_cell(self):
        base = json.loads((ROOT / "near_triple.json").read_text())["squares"]
        cert = json.loads((ROOT / "E008_DUAL_CERTIFICATE.json").read_text())
        cert["removed_cells_zero_based"].append([0,1])
        with self.assertRaisesRegex(AssertionError, "duplicate"):
            validate(base[0],base[2],cert,base[1])

    def test_reject_nonlatin_fixed_square(self):
        base = json.loads((ROOT / "near_triple.json").read_text())["squares"]
        cert = json.loads((ROOT / "E008_DUAL_CERTIFICATE.json").read_text())
        base[0][0][0] = -1
        with self.assertRaisesRegex(AssertionError, "Latin"):
            validate(base[0],base[2],cert,base[1])

if __name__ == "__main__":
    unittest.main()
