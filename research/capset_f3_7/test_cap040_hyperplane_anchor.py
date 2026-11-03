"""CAP-040H: unconditional 237-cap hyperplane anchor, orbit and SAT tests."""
import hashlib,tempfile,unittest
from itertools import permutations
from pathlib import Path
from cap040_hyperplane_anchor import (moment_89_check,h_anchor_orbits,
                                    at_least_clauses,stats,write_cnf,
                                    anchored_ninth_branches,extra_ninth_units)
from cap040_root_orbits import barycentric,vec

class CAP040HTests(unittest.TestCase):
    def test_moment_gate_exact(self):
        d=moment_89_check()
        self.assertEqual((d['local_cases_checked'],d['contradiction_global_moment_sum']),
                         (75,-35076))

    def test_stabilizer_s7_orbits_full_coverage(self):
        cases=h_anchor_orbits()
        self.assertEqual(len(cases),32)
        self.assertEqual(sum(v['size'] for v in cases),2151)
        for x in cases:
            lam=barycentric(vec(x['rep'],7))
            images={tuple(lam[i] for i in perm)+(lam[7],)
                    for perm in permutations(range(7))}
            self.assertEqual(len(images),x['size'])
            self.assertEqual({v[-1] for v in images},{x['tag'][0]})

    def test_ten_complete_high_slice_ninth_branches(self):
        cases=anchored_ninth_branches()
        self.assertEqual(len(cases),10)
        self.assertEqual([q['size'] for q in cases],
                         [7,35,1,105,42,21,210,140,35,105])
        self.assertEqual(sum(q['size'] for q in cases),701)
        self.assertTrue(all(q['tag'][0]==0 for q in cases))
        self.assertEqual(sorted(len(extra_ninth_units(q)) for q in cases),
                         [8]+[9]*9)

    def test_cardinality_counter_truth_table(self):
        V=[1,2,3,4];clauses=list(at_least_clauses(V,2,4))
        self.assertEqual(len(clauses),sum(2*min(i,2)-1 for i in range(1,5))+1)
        for mask in range(16):
            target=mask.bit_count()>=2
            feasible=False
            for z in range(1<<7):
                def val(i):
                    if i<=4:return bool(mask&(1<<(i-1)))
                    return bool(z&(1<<(i-5)))
                if all(any(val(abs(l))==(l>0) for l in c) for c in clauses):
                    feasible=True;break
            self.assertEqual(feasible,target)

    def test_full_cnffile_header_and_hash(self):
        d=stats()
        self.assertEqual((d['total_variables'],d['total_clauses']),(553505,1896555))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'anchored.cnf'
            write_cnf(str(p))
            with p.open('rb') as f:
                self.assertIn(b'p cnf 553505 1896555',f.readline()+f.readline())
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                             'c45a3e74e885b070ab0bc7a4a0d71cdc976dd1c17b442bfd7fedca665e9e37be')
if __name__=='__main__':unittest.main()
