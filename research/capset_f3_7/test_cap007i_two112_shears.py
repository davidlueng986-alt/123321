"""Independent source arithmetic and reproduced bounded exact C++ census."""
import unittest,json,subprocess,tempfile
from pathlib import Path
from itertools import combinations,product
from cap006_projection_audit import read_cap
P=Path(__file__).resolve().parent
def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
class TwoSliceAudit(unittest.TestCase):
    def test_independent_identity_holes(self):
        B=set(read_cap());X={p[1:] for p in B if p[0]==0};Y={p[1:] for p in B if p[0]==1}
        self.assertEqual((len(X),len(Y)),(112,112))
        holes=set(product(range(3),repeat=6))-{third(x,y) for x in X for y in Y}
        expected={tuple(s if i==pos else 0 for i in range(6))
                  for pos in range(6) for s in (1,2)}
        self.assertEqual(holes,expected)
        self.assertTrue(all(third(a,b) not in holes for a,b in combinations(sorted(holes),2)))
    def test_cpp_exact_5922(self):
        import shutil
        if not shutil.which('g++'):self.skipTest('C++ compiler not present')
        with tempfile.TemporaryDirectory() as d:
            binary=str(Path(d)/'two_slice')
            subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra','-pedantic',
                            str(P/'cap007i_two112_shears.cpp'),'-o',binary],check=True)
            proc=subprocess.run([binary,str(P/'candidates'/'calderbank_fishburn_236.txt')],
                                capture_output=True,text=True,check=True,timeout=30)
            result=json.loads(proc.stdout)
            self.assertEqual(result['tested_unique_linear_maps'],5922)
            self.assertEqual(result['max_holes'],12)
            self.assertEqual(result['maps_with_at_least_13_holes'],0)
            self.assertEqual(result['holes_histogram'],{'0':5732,'1':127,'4':61,'12':2})
            self.assertEqual(sum(result['holes_histogram'].values()),5922)
if __name__=='__main__':unittest.main()
