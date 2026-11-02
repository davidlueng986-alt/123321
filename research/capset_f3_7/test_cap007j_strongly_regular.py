import unittest
from pathlib import Path
from cap007j_strongly_regular import certify,cross_energy_any_second_slice
from cap007j_112_alignment import read_fixture
class SRG112Test(unittest.TestCase):
    def test_both_canonical_caps(self):
        a,b,_=read_fixture(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt')
        for S in [a,b]:
            r=certify(S)
            self.assertEqual(r['cayley_graph'],{'v':729,'k':112,'lambda':1,'mu':20})
            self.assertEqual(r['fourier_eigenvalues'],{-23:112,4:616,112:1})
    def test_arbitrary_second_slice_exact_energy(self):
        from collections import Counter
        a,b,_=read_fixture(Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt')
        for length in (32,80,100,110,111,112):
            T=b[:length]
            conv=Counter(tuple((x+y)%3 for x,y in zip(s,t)) for s in a for t in T)
            energy=sum(z*z for z in conv.values())
            self.assertEqual(energy,cross_energy_any_second_slice(a,T))
if __name__=='__main__':unittest.main()
