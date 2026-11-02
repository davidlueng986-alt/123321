"""Exact global cap CNF sanity and exhaustive tiny-dimensional truth tests."""
import unittest
from itertools import combinations
from cap007_global_exact_model import (digits,third,lines,basis_ids,forbidden_basis_ids,stats,
                                         verify_candidate_assignment,write_cnf)
import tempfile,os
class GlobalCNFTest(unittest.TestCase):
    def test_lines(self):
        for n in (1,2,3,4):
            L=list(lines(n));N=3**n
            self.assertEqual(len(L),N*(N-1)//6)
            self.assertEqual(len(L),len(set(L)))
            self.assertTrue(all(a<b<c and third(digits(a-1,n),digits(b-1,n))==digits(c-1,n)
                                for a,b,c in L))
    def test_basis(self):
        for n in (2,3,4,7):
            self.assertEqual(len(set(basis_ids(n))),n+1)
            self.assertEqual(len(set(forbidden_basis_ids(n))),n*(n+1)//2)
            self.assertFalse(set(basis_ids(n))&set(forbidden_basis_ids(n)))
    def test_full_n2_truth_table(self):
        n=2;V=[digits(i,n) for i in range(9)];known4=False
        for mask in range(1<<9):
            A=[V[i] for i in range(9) if mask>>i&1]
            S=set(A)
            valid=all(third(a,b) not in S for a,b in combinations(A,2))
            self.assertEqual(verify_candidate_assignment(2,4,A),valid and len(A)>=4)
            self.assertEqual(verify_candidate_assignment(2,5,A),valid and len(A)>=5)
            if valid and len(A)==4:known4=True
            if valid:self.assertLessEqual(len(A),4)
        self.assertTrue(known4)
    def test_known_n3_cap(self):
        A=[tuple(map(int,s)) for s in ('001','002','010','012','102','111','112','121','201')]
        self.assertTrue(verify_candidate_assignment(3,9,A))
        self.assertFalse(verify_candidate_assignment(3,10,A))
    def test_n7_sizes_and_n4_output(self):
        s=stats(7,237,True)
        self.assertEqual((s['line_clauses'],s['variables'],s['clauses']),(796797,492540,1775353))
        with tempfile.TemporaryDirectory() as d:
            p=os.path.join(d,'n4.cnf')
            r=write_cnf(4,21,p,True)
            with open(p) as f:lines_text=f.readlines()
            self.assertEqual(len(lines_text),r['clauses']+2)
            self.assertIn('p cnf 1572 3997',lines_text[1])
if __name__=='__main__':unittest.main()
