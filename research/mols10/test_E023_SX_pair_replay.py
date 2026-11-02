"""E023 published SX pair: exact Latin/orthogonality and common-transversal regression."""
import itertools,unittest
from E023_SX_pair_replay import P,Q,latin,overlay,replay

class TestE023SX(unittest.TestCase):
    def test_source_pair_and_composition(self):
        x=replay()
        self.assertTrue(latin(P) and latin(Q) and latin(x['Z']))
        self.assertEqual(overlay(x['Z'],Q),100)
        self.assertTrue(all(P[x['Z'][r][c]][c]==Q[r][c]
            for r in range(10) for c in range(10)))
    def test_no_common_transversal_independent_permutations(self):
        Z=replay()['Z']
        found=0
        for p in itertools.permutations(range(10)):
            a=b=0
            for r,c in enumerate(p):
                a|=1<<Z[r][c]; b|=1<<Q[r][c]
                if a.bit_count()!=r+1 or b.bit_count()!=r+1:
                    break
            else:found+=1
        self.assertEqual(found,0)
if __name__=='__main__':unittest.main()
