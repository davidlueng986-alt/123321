import unittest,tempfile,os
from cap007h_extremal_6slice_cnf import fixed_slice,stats,check_witness,write
from cap006b_partition_pilot import baseline
class AnchoredSlice(unittest.TestCase):
    def test_fixed_112_and_counter_replay(self):
        B=baseline()
        self.assertEqual(len(fixed_slice()),112)
        self.assertTrue(check_witness(B,236))
        self.assertFalse(check_witness(B,237))
    def test_clause_counts(self):
        s=stats(237)
        self.assertEqual(s['variable_points_in_two_other_slices'],1458)
        self.assertEqual(s['cross_fixed_slice_pair_clauses'],81648)
        self.assertEqual(s['within_6d_line_clauses'],176904)
        self.assertEqual((s['total_variables'],s['total_clauses']),(175958,606095))
if __name__=='__main__':unittest.main()
