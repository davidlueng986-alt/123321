import copy
import json
import unittest
from pathlib import Path

from forced_prefix import certificate, model, normalized_cut
from verify_forced_prefix import verify

HERE = Path(__file__).parent


class ForcedPrefixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prefix = json.loads((HERE / "row_cover_fixture.json").read_text())["prefix"]
        cls.proof = json.loads((HERE / "forced_prefix_certificate.json").read_text())

    def test_all_legal_options_are_forced(self):
        n, k, options, support = model(self.prefix)
        self.assertEqual((n, k, len(options), len(support)), (10, 7, 30, 180))
        self.assertTrue(all(len(ids) == 1 for ids in support.values()))

    def test_independent_full_prefix_certificate(self):
        self.assertTrue(verify(self.prefix, self.proof))
        self.assertEqual(certificate(self.prefix), self.proof)

    def test_wrong_forcing_demand_rejected(self):
        bad = copy.deepcopy(self.proof)
        bad["units"][0]["demand"] = bad["units"][1]["demand"]
        with self.assertRaises(AssertionError):
            verify(self.prefix, bad)

    def test_dropped_color_branch_rejected(self):
        bad = copy.deepcopy(self.proof)
        bad["color_proof"]["children"] = []
        with self.assertRaises(AssertionError):
            verify(self.prefix, bad)

    def test_changed_prefix_cannot_reuse_certificate(self):
        changed = copy.deepcopy(self.prefix)
        changed[0][0][0], changed[0][0][1] = changed[0][0][1], changed[0][0][0]
        with self.assertRaises(AssertionError):
            verify(changed, self.proof)

    def test_affine_order5_positive_prefix_not_rejected(self):
        full = [[[(r+a*c) % 5 for c in range(5)] for r in range(5)] for a in (1, 2, 3)]
        for k in (1, 2, 3, 4):
            self.assertEqual(certificate([Q[:k] for Q in full])["status"], "NO_FORCED_OBSTRUCTION")

    def test_small_zero_support_proof(self):
        prefix = [[[0, 1, 2]] for _ in range(3)]
        proof = certificate(prefix)
        self.assertEqual(proof["kind"], "zero_support")
        self.assertTrue(verify(prefix, proof))

    def test_legal_relabelings_preserve_obstruction(self):
        n, k = 10, 7
        for shift in (1, 3, 7):
            # Common column permutation, independent symbol permutations, common row reversal.
            col = [(c+shift) % n for c in range(n)]
            transformed = [[[(self.prefix[s][k-1-r][col[c]]+shift*(s+1)) % n
                             for c in range(n)] for r in range(k)] for s in range(3)]
            proof = certificate(transformed)
            self.assertEqual(proof["status"], "NO_COMPLETION_OF_THIS_PREFIX")
            self.assertTrue(verify(transformed, proof))

    def test_generated_cut_is_pinned(self):
        expected = json.loads((HERE / "normalized_oa_cut.json").read_text())
        self.assertEqual(normalized_cut(self.prefix, self.proof), expected)
        self.assertEqual(len(expected["clause"]), 60)
        self.assertTrue(all(x < 0 for x in expected["clause"]))


if __name__ == "__main__":
    unittest.main()
