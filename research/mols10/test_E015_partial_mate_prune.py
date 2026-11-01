import unittest
from E014_symbol_obstruction import load_pairs
from E015_partial_mate_prune import setup,check_partial,minimum_exact_once

def gf4_mul(a,b):
    z=0
    for _ in range(2):
        if b&1:z^=a
        b>>=1
        a<<=1
        if a&4:a^=7
    return z

class TestE015PartialPruning(unittest.TestCase):
    def test_positive_GF4_complete_triple_never_rejected(self):
        a=[[i^j for j in range(4)] for i in range(4)]
        b=[[gf4_mul(2,i)^j for j in range(4)] for i in range(4)]
        trans,masks,by_cell,compat=setup(a)
        ids=[]
        for symbol in range(4):
            p=tuple(next(j for j in range(4) if b[i][j]==symbol)
                    for i in range(4))
            ids.append(trans.index(p))
        for k in range(5):
            ok,blocked,count=check_partial(by_cell,compat,ids[:k])
            self.assertTrue(ok)
            self.assertEqual(blocked,[])
            self.assertGreaterEqual(count,4)

    def test_exact_minimum_partial_class_obstructions(self):
        pairs=load_pairs()
        expected={"Egan_AB":3,"Egan_AC":3,"Parker_AB":2,
                  "trade_12":3,"trade_20":2}
        for name,k in expected.items():
            with self.subTest(name=name):
                a,b=pairs[name]
                result=minimum_exact_once(a,b)
                self.assertEqual(result["minimum"],k)
                self.assertTrue(all(
                    row["blocking"]==0
                    for i,row in result["counts"].items() if int(i)<k))

    def test_known_Parker_two_class_blocker(self):
        a,b=load_pairs()["Parker_AB"]
        result=minimum_exact_once(a,b)
        self.assertEqual(result["first_certificate"]["symbols"],[7,8])
        self.assertEqual(result["first_certificate"]["first_blocked_cell"],[7,7])

if __name__=="__main__":
    unittest.main()
