"""E016 regression: bitset invariants, positive control, and two fixed-A exhaustive cases."""
import json
import unittest
from pathlib import Path
from E015_partial_mate_prune import setup
from E016_bitset_search import run, gf4_positive_control
from first_square_trades import first_square_trades

ROOT=Path(__file__).resolve().parent

class TestE016(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads((ROOT/'near_triple.json').read_text())['squares'][0]

    def test_gf4_known_positive(self):
        self.assertEqual(gf4_positive_control()['status'],'SAT_SUPPORT_ONLY')

    def test_bitset_compatibility_and_disjoint_invariants(self):
        trans,masks,by,compat=setup(self.a)
        self.assertEqual(len(trans),1080)
        for k in [0,1,17,101,500,1079]:
            for j in [0,7,23,101,555,1079]:
                self.assertEqual(bool((compat[k]>>j)&1),
                                 (masks[k]&masks[j]).bit_count()==1)
                bad=0
                for cell in range(100):
                    if (masks[k]>>cell)&1:bad|=by[cell]
                self.assertEqual(bool((bad>>j)&1),
                                 bool(masks[k]&masks[j]))

    def test_original_first_square_exhaustive(self):
        r=run(self.a,max_nodes=250000,max_seconds=30)
        self.assertEqual(r['status'],'UNSAT_FIXED_A_EXHAUSTIVE')
        self.assertEqual((r['nodes'],r['pruned_prefixes']),(24875,18407))

    def test_trade12_first_square_exhaustive(self):
        a=first_square_trades(self.a)[12]['square']
        r=run(a,max_nodes=250000,max_seconds=30)
        self.assertEqual(r['status'],'UNSAT_FIXED_A_EXHAUSTIVE')
        self.assertEqual((r['nodes'],r['pruned_prefixes']),(17377,13324))

if __name__=='__main__':
    unittest.main()
