import json, unittest
from pathlib import Path
from k_symbol_trades import scan_k

class TestKTrades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.egan=json.loads(Path("near_triple.json").read_text())["squares"]
        cls.parker=json.loads(Path("parker_pair.json").read_text())["squares"]
    def test_Egan_AB_k3_isolated(self):
        r=scan_k(self.egan[0],self.egan[1],3)
        self.assertEqual((r["supports_with_alternatives"],r["neighbors_checked"]),(0,0))
        self.assertEqual(r["capped_supports"],0)
    def test_Egan_AB_k4(self):
        r=scan_k(self.egan[0],self.egan[1],4)
        self.assertEqual((r["supports_with_alternatives"],r["neighbors_checked"]),(3,6))
        self.assertEqual(max(x["count"] for x in r["results"]),4)
        self.assertEqual(r["capped_supports"],0)
    def test_Egan_AB_k5(self):
        r=scan_k(self.egan[0],self.egan[1],5)
        self.assertEqual((r["supports_with_alternatives"],r["neighbors_checked"]),(18,36))
        self.assertEqual(max(x["count"] for x in r["results"]),4)
        self.assertEqual(r["capped_supports"],0)
    def test_Egan_AC_k3(self):
        r=scan_k(self.egan[0],self.egan[2],3)
        self.assertEqual((r["supports_with_alternatives"],r["neighbors_checked"]),(24,24))
        self.assertEqual(max(x["count"] for x in r["results"]),1)
        self.assertEqual(r["capped_supports"],0)
    def test_parker_AB_k3(self):
        r=scan_k(*self.parker,3)
        self.assertEqual((r["supports_with_alternatives"],r["neighbors_checked"]),(22,26))
        self.assertEqual(max(x["count"] for x in r["results"]),0)
        self.assertEqual(r["capped_supports"],0)

if __name__=="__main__":unittest.main()
