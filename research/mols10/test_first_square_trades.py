import json
import unittest
from collections import Counter
from pathlib import Path
from first_square_trades import first_square_trades
from sample_mates import transversals_single
from verify import analyze

class TestFirstSquareTrades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a,cls.b,cls.c=json.loads(
            Path("near_triple.json").read_text())["squares"]
        cls.trades=first_square_trades(cls.a)

    def test_all_components_and_latin(self):
        self.assertEqual(len(self.trades),48)
        self.assertEqual(dict(Counter(t["size"] for t in self.trades)),
                         {8:7,4:11,16:3,14:3,10:6,6:15,12:3})
        for t in self.trades:
            self.assertEqual({len(set(row)) for row in t["square"]},{10})

    def test_not_same_transversal_number_as_source(self):
        self.assertEqual(len(transversals_single(self.a)),1080)
        counts=Counter(len(transversals_single(t["square"]))
                       for t in self.trades)
        self.assertEqual(dict(counts),{
            840:6,872:3,892:6,904:10,912:3,
            924:3,928:3,948:5,952:3,1000:6
        })
        self.assertNotIn(1080,counts)

    def test_previously_fixed_mates_no_longer_orthogonal(self):
        self.assertTrue(all(
            not analyze([t["square"],self.b],10)[0]["orthogonal"]
            and not analyze([t["square"],self.c],10)[0]["orthogonal"]
            for t in self.trades))

if __name__=="__main__":
    unittest.main()
