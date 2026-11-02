#!/usr/bin/env python3
"""Independent standard-library regression for the minimally patched external v5 import.
Verifies construction arithmetic and CAP-011A; not all v5 group-theory claims."""
import ast, json, unittest
from pathlib import Path
from itertools import combinations, product
from collections import Counter

ROOT=Path(__file__).resolve().parent/'external_agent_v5'
SRC=ROOT/'capset_swarm_v5_fixed.py'
DATA=ROOT/'capset_swarm_v5_corrected_evidence.json'
CASES={'F3_6_optimal_112':(6,112),'F3_7_complete_236':(7,236),
       'F3_8_complete_496':(8,496),'F3_8_record_complete_512':(8,512)}

def validate_cap(points,n):
    p=[tuple(map(int,x)) for x in points]
    assert len(p)==len(set(p)) and all(len(x)==n and all(t in (0,1,2) for t in x) for x in p)
    present=set(p)
    for a,b in combinations(p,2):
        assert tuple((-x-y)%3 for x,y in zip(a,b)) not in present
    return len(p)

def residue_counts(points,n):
    p=[tuple(map(int,x)) for x in points];m=len(p)
    bary=tuple(((m%3)*sum(x[i] for x in p))%3 for i in range(n))
    centered=[tuple((x[i]-bary[i])%3 for i in range(n)) for x in p]
    assert all(sum(x[i] for x in centered)%3==0 for i in range(n))
    hist=Counter();count=0
    for d in product(range(3),repeat=n):
        if not any(d) or next(t for t in d if t)!=1:continue
        a=[0,0,0]
        for x in centered:a[sum(t*v for t,v in zip(x,d))%3]+=1
        assert a[1]%3==a[2]%3
        q=(-sum((sum(t*v for t,v in zip(x,d))%3)**2 for x in centered))%3
        assert a[1]%3==q
        hist[q]+=1;count+=1
    assert count==(3**n-1)//2
    return [hist[k] for k in range(3)]

class TestOtherAgentV5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_text(encoding='utf-8'))
    def test_source_syntax_and_minimal_fixes(self):
        code=SRC.read_text(encoding='utf-8');ast.parse(code)
        self.assertIn('Q = (-centered.T @ centered) % 3',code)
        self.assertIn('assert paired_ok and quad_formula_exact',code)
        self.assertIn('FLOATING-POINT DIAGNOSTIC ONLY',code)
        self.assertNotIn('/working_dir/',code)
    def test_point_sets_direct_base_three(self):
        for key,(n,m) in CASES.items():
            with self.subTest(cap=key):
                self.assertEqual(validate_cap(self.data['verified_constructions'][key]['points'],n),m)
    def test_signed_quadric_each_direction(self):
        reports=self.data['cap011abc_universal_quadric_codim2_and_involution_spectra']['cap011a_universal_barycenter_quadric_verifications']
        for key,(n,_) in CASES.items():
            with self.subTest(cap=key):
                observed=residue_counts(self.data['verified_constructions'][key]['points'],n)
                self.assertEqual(observed,reports[key]['majority_residue_counts_N0_N1_N2'])
                self.assertTrue(reports[key]['majority_residue_equals_dT_Q_d'])
    def test_global_codim2_moments(self):
        m=237
        self.assertEqual([99463*m,99463*m+11011*m*(m-1),
                          99463*m+3*11011*m*(m-1)+1210*m*(m-1)*(m-2)],
                         [23572731,639439983,17775438687])
        self.assertTrue(self.data['cap010bc_exact_rational_spectral_and_completion_audit']['spectral_diagnostics_use_float'])

if __name__=='__main__':unittest.main()
