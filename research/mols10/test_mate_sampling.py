import json,unittest
from pathlib import Path
from sample_mates import transversals_single,transversals_pair,make_mate
from verify import analyze

class TestMateSampling(unittest.TestCase):
    def test_deterministic_single_A_baseline(self):
        a=json.loads(Path("near_triple.json").read_text())["squares"][0]
        t=transversals_single(a)
        self.assertEqual(len(t),1080)
        for seed,expected in [(0,0),(2,1),(14,14)]:
            b,result=make_mate(a,t,seed)
            self.assertIsNotNone(b)
            self.assertTrue(analyze([a,b],10)[0]["orthogonal"])
            trans,support=transversals_pair(a,b)
            self.assertEqual(len(trans),expected)
            self.assertGreater(sum(x==0 for x in support),0)

if __name__=="__main__":unittest.main()
