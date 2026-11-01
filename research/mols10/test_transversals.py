"""E002 regression tests: independent exact enumeration on small orders and both published pairs."""
import json
import unittest
from pathlib import Path
from transversals import analyze_fixed_pair
from verify import analyze


def gf4mul(a, b):
    out = 0
    for _ in range(2):
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


class TestTransversalCertificates(unittest.TestCase):
    def test_order_three_nonextension(self):
        a = [[(i+j)%3 for j in range(3)] for i in range(3)]
        b = [[(i+2*j)%3 for j in range(3)] for i in range(3)]
        result = analyze_fixed_pair(a, b)
        self.assertEqual(result["common_transversal_count"], 0)
        self.assertEqual(result["extension_status"], "UNSAT_FIXED_PAIR_CERTIFIED")

    def test_order_four_positive(self):
        a = [[i^j for j in range(4)] for i in range(4)]
        b = [[gf4mul(2,i)^j for j in range(4)] for i in range(4)]
        result = analyze_fixed_pair(a, b)
        self.assertEqual(result["common_transversal_count"], 4)
        self.assertEqual(result["packing"]["max_disjoint"], 4)
        self.assertEqual(result["extension_status"], "SAT_VERIFIED")
        self.assertEqual([x["unique"] for x in analyze([a,b,result["third_square_witness"]],4)],
                         [16,16,16])

    def test_published_pair_ab(self):
        s = json.loads(Path("near_triple.json").read_text())["squares"]
        result = analyze_fixed_pair(s[0],s[1])
        self.assertEqual(result["common_transversal_count"], 14)
        self.assertEqual(result["packing"]["max_disjoint"], 7)
        self.assertEqual(len(result["unsupported_cells_zero_based"]), 12)
        self.assertEqual(result["extension_status"], "UNSAT_FIXED_PAIR_CERTIFIED")

    def test_published_pair_ac(self):
        s = json.loads(Path("near_triple.json").read_text())["squares"]
        result = analyze_fixed_pair(s[0],s[2])
        self.assertEqual(result["common_transversal_count"], 7)
        self.assertEqual(result["packing"]["max_disjoint"], 1)
        self.assertEqual(len(result["unsupported_cells_zero_based"]), 36)
        self.assertEqual(result["extension_status"], "UNSAT_FIXED_PAIR_CERTIFIED")


if __name__ == "__main__":
    unittest.main()
