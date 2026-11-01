import json
import unittest
from pathlib import Path
from transversals import transversals_by_dfs, transversals_by_permutations
from exact_cover import exact_cover, build_third
from verify import analyze

class TestCover(unittest.TestCase):
    def test_parker_pair_no_common_transversal(self):
        a,b=json.loads(Path("parker_pair.json").read_text())["squares"]
        self.assertEqual([q["unique"] for q in analyze([a,b],10)], [100])
        t=transversals_by_dfs(a,b)
        self.assertEqual(t,transversals_by_permutations(a,b))
        self.assertEqual(len(t),0)
        s=exact_cover(t,10)
        self.assertEqual(s["status"],"UNSAT_FIXED_PAIR_EXACT")
        self.assertEqual(s["nodes"],0)

    def test_egan_pairs_unextendible(self):
        a,b,c=json.loads(Path("near_triple.json").read_text())["squares"]
        for second,num in [(b,14),(c,7)]:
            t=transversals_by_dfs(a,second)
            self.assertEqual(len(t),num)
            self.assertEqual(exact_cover(t,10)["status"],"UNSAT_FIXED_PAIR_EXACT")

    def test_order_four_mate_exists(self):
        def mul4(a,b):
            z=0
            for _ in range(2):
                if b&1:z^=a
                b>>=1;a<<=1
                if a&4:a^=7
            return z
        a=[[i^j for j in range(4)] for i in range(4)]
        b=[[mul4(2,i)^j for j in range(4)] for i in range(4)]
        t=transversals_by_dfs(a,b)
        r=exact_cover(t,4)
        self.assertEqual(r["status"],"SAT_EXACT")
        c=build_third(a,b,t,r)
        self.assertEqual([q["unique"] for q in analyze([a,b,c],4)],[16,16,16])

    def test_budget_exhaustion_unknown(self):
        from itertools import permutations
        r=exact_cover(list(permutations(range(3))),3,max_nodes=1)
        self.assertEqual(r["status"],"UNKNOWN_BUDGET")

    def test_invalid_transversal_rejected(self):
        with self.assertRaises(ValueError):
            exact_cover([[0,0,2]],3)

if __name__=="__main__": unittest.main()
