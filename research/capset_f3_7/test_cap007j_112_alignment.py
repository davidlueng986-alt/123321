"""Independent arithmetic assertions, additive-energy cross-check, translations."""
import unittest
from collections import Counter
from itertools import combinations
from pathlib import Path
from cap007j_112_alignment import (read_fixture,third,encode,V,unit_ops,transform,make_third_table,holes,
                                   power_mask,additive_energy_formula,calc)

class AlignmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=Path(__file__).resolve().parent / 'candidates' / 'calderbank_fishburn_236.txt'
        cls.B0,cls.B1,cls.B2=read_fixture(cls.fixture)
        cls.ops=list(unit_ops())
    def test_direct_energy_vs_Fourier(self):
        H0=power_mask(self.B0);H1=power_mask(self.B1)
        for name,M in [self.ops[0],self.ops[1],self.ops[7],self.ops[22],self.ops[27]]:
            B=[transform(M,p) for p in self.B1]
            conv=Counter(encode(third(a,b)) for a in self.B0 for b in B)
            energy=sum(x*x for x in conv.values())
            mt=tuple(tuple(M[j][i] for j in range(6)) for i in range(6))
            k=sum(encode(transform(mt,V[u])) in H1 for u in H0)
            self.assertEqual(energy,additive_energy_formula(k),name)
    def test_translation_covariance(self):
        I=self.ops[0][1]
        table=make_third_table(self.B0)
        origin={V[z] for z in holes(self.B1,I,table)}
        self.assertEqual(origin,set(self.B2))
        for t in [(0,0,0,0,0,0),(1,0,0,0,0,0),(0,2,1,0,2,1),(1,1,1,1,1,1)]:
            shifted=[tuple((a+b)%3 for a,b in zip(p,t)) for p in self.B1]
            E={V[z] for z in holes(shifted,I,table)}
            self.assertEqual(E,{tuple((a-b)%3 for a,b in zip(z,t)) for z in origin})
    def test_finite_two_step_certificate(self):
        result=calc(self.fixture)
        self.assertEqual(result['matrices'],3812)
        self.assertEqual(result['max_eligible_third_slice'],12)
        self.assertEqual(result['holes_histogram'],{0:3505,1:126,4:60,12:121})

if __name__=='__main__':unittest.main()
