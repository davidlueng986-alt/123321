import json,unittest
from pathlib import Path
from two_symbol_trades import trade_neighborhood
from sample_mates import transversals_pair

class TestTrades(unittest.TestCase):
    def test_egan_b_isolated_under_two_symbol_flips(self):
        a,b,_=json.loads(Path("near_triple.json").read_text())["squares"]
        self.assertEqual(len(trade_neighborhood(a,b)),0)
    def test_egan_c_has_three_nontrivial_trades(self):
        a,_,c=json.loads(Path("near_triple.json").read_text())["squares"]
        trades=trade_neighborhood(a,c)
        self.assertEqual([t["symbols"] for t in trades],[[1,8],[2,9],[3,7]])
        self.assertTrue(all(t["component_sizes"]==[14,6] for t in trades))
        self.assertEqual([len(transversals_pair(a,t["neighbor"])[0]) for t in trades],[1,1,1])
    def test_parker_b_has_three_nontrivial_trades(self):
        a,b=json.loads(Path("parker_pair.json").read_text())["squares"]
        trades=trade_neighborhood(a,b)
        self.assertEqual([t["symbols"] for t in trades],[[7,8],[7,9],[8,9]])
        self.assertTrue(all(t["component_sizes"]==[14,6] for t in trades))
        self.assertEqual([len(transversals_pair(a,t["neighbor"])[0]) for t in trades],[0,0,0])

if __name__=="__main__":unittest.main()
