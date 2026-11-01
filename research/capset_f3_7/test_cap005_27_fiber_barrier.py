import json, subprocess, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
class TestCap005A(unittest.TestCase):
    def test_four_fiber_exact_replay(self):
        run=subprocess.run([sys.executable,str(HERE/"cap005_27_fiber_barrier.py")],
            check=True,capture_output=True,text=True,timeout=60)
        x=json.loads(run.stdout)
        self.assertEqual(x["status"],"NO_IMPROVEMENT_WITH_AT_MOST_FOUR_RELEASED_FIBERS")
        self.assertEqual(x["max_admissible_outsiders"],{"1":0,"2":1,"3":4,"4":6})
        self.assertEqual(x["histograms"]["4"],{"0":12510,"1":4320,"2":408,"4":160,"5":96,"6":56})
    def test_five_fiber_gate_does_not_exclude_improvement(self):
        run=subprocess.run([sys.executable,str(HERE/"cap005_27_fiber_barrier.py"),"--max-k","5"],
            check=True,capture_output=True,text=True,timeout=60)
        x=json.loads(run.stdout)
        self.assertEqual(x["max_admissible_outsiders"]["5"],22)
        self.assertEqual(sum(x["histograms"]["5"].values()),80730)
        self.assertEqual(x["histograms"]["5"]["22"],8)
if __name__=="__main__": unittest.main()
