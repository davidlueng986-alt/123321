import json,unittest
from pathlib import Path
from parker_frontier import prefix_certificate

class TestParkerFrontier(unittest.TestCase):
    def test_exact_profile_and_last_row_blocked(self):
        a,b=json.loads(Path("parker_pair.json").read_text())["squares"]
        result=prefix_certificate(a,b)
        self.assertEqual(result["depth_profile"],[1,10,70,329,1046,1983,2233,1471,318,21,0])
        self.assertEqual(len(result["depth_n_minus_1_frontier"]),21)
        self.assertTrue(all(p["blocked_A"] and p["blocked_B"]
                            for p in result["depth_n_minus_1_frontier"]))

if __name__=="__main__":unittest.main()
