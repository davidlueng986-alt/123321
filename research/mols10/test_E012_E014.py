import unittest
from E014_symbol_obstruction import (
    load_pairs, minimal_obstruction, independent_permutation_replay
)
from sample_mates import transversals_pair
from verify import analyze

class TestE012E014(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pairs=load_pairs()

    def test_new_first_square_pairs_valid_but_nonextendable(self):
        for name in ("trade_12","trade_20"):
            a,b=self.pairs[name]
            self.assertTrue(all(p["orthogonal"] for p in analyze([a,b],10)))
            common,support=transversals_pair(a,b)
            self.assertEqual(len(common),0)
            self.assertEqual(sum(v==0 for v in support),100)

    def test_exact_minimal_symbol_obstructions(self):
        expected={"Egan_AB":6,"Egan_AC":5,"Parker_AB":3,
                  "trade_12":5,"trade_20":5}
        for name,k in expected.items():
            with self.subTest(name=name):
                a,b=self.pairs[name]
                r=minimal_obstruction(a,b)
                self.assertEqual(r["minimum_B_symbol_subset"],k)
                self.assertTrue(r["smaller_subsets_all_nonblocking"])

    def test_independent_permutation_replay_parker(self):
        a,b=self.pairs["Parker_AB"]
        r=minimal_obstruction(a,b)
        self.assertEqual(r["first_certificate"]["B_symbols"],[7,8,9])
        self.assertEqual(r["first_certificate"]["blocked_cell"],[7,7])
        check=independent_permutation_replay(a,b,r["first_certificate"])
        self.assertEqual(check["permutations_checked"],3628800)
        self.assertEqual(check["A_transversals"],1104)
        self.assertEqual(check["eligible_through_blocked_cell"],0)

if __name__=="__main__":
    unittest.main()
