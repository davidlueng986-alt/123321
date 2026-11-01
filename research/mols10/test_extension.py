import unittest
from extend_fixed_pair import extend_pair
from verify import analyze

def mul_gf4(a,b):
    result = 0
    for _ in range(2):
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return result

class TestPairExtension(unittest.TestCase):
    def test_order_three_fixed_pair_unextendible(self):
        a = [[(i+j)%3 for j in range(3)] for i in range(3)]
        b = [[(i+2*j)%3 for j in range(3)] for i in range(3)]
        out = extend_pair(a,b,max_nodes=10000,max_seconds=3)
        self.assertEqual(out["status"], "UNSAT_FIXED_PAIR")

    def test_order_four_fixed_pair_extendible(self):
        a = [[i^j for j in range(4)] for i in range(4)]
        b = [[mul_gf4(2,i)^j for j in range(4)] for i in range(4)]
        out = extend_pair(a,b,max_nodes=100000,max_seconds=5)
        self.assertEqual(out["status"], "SAT")
        self.assertEqual([q["unique"] for q in analyze([a,b,out["solution"]],4)],
                         [16,16,16])

    def test_invalid_input_pair_rejected(self):
        a = [[(i+j)%3 for j in range(3)] for i in range(3)]
        with self.assertRaises(ValueError):
            extend_pair(a,a)

if __name__ == "__main__":
    unittest.main()
