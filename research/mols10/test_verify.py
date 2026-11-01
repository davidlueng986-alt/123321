import unittest
from verify import analyze

class TestVerifier(unittest.TestCase):
    def test_two_orthogonal_order_three(self):
        a = [[(i+j)%3 for j in range(3)] for i in range(3)]
        b = [[(i+2*j)%3 for j in range(3)] for i in range(3)]
        self.assertTrue(analyze([a,b],3)[0]["orthogonal"])

    def test_reject_duplicate_square_as_third(self):
        a = [[(i+j)%3 for j in range(3)] for i in range(3)]
        b = [[(i+2*j)%3 for j in range(3)] for i in range(3)]
        self.assertEqual([q["unique"] for q in analyze([a,b,a],3)], [9,3,9])

    def test_reject_non_latin(self):
        with self.assertRaises(ValueError):
            analyze([[[0,1],[0,1]]],2)

    def test_reject_out_of_range(self):
        with self.assertRaises(ValueError):
            analyze([[[0,2],[1,0]]],2)

    def test_reject_boolean_as_symbol(self):
        with self.assertRaises(ValueError):
            analyze([[[True,1],[1,0]]],2)

    def test_near_triple(self):
        import json
        from pathlib import Path
        squares = json.loads(Path("near_triple.json").read_text())["squares"]
        self.assertEqual([q["unique"] for q in analyze(squares,10)], [100,100,91])

if __name__ == "__main__":
    unittest.main()
